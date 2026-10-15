"""designinstantly_energy: end a run gracefully once the brand owner's Energy is spent.

DesignInstantly runs every co-worker on its brand owner's OpenRouter key, whose spending limit is
the owner's remaining Energy. OpenRouter enforces that limit, so once it is spent every call on
the key is refused. Without this plugin the refusal fails the run; with it, the run ends with
Otto's own reply telling the user how to get more Energy, in chat and cron alike.

  * ``llm_execution`` middleware: a call refused for the key's limit returns that reply as the
    model's final answer instead of raising. For a minute afterwards calls skip OpenRouter and
    return it straight away. Any other error, including our platform account running dry, raises
    as before, so it never reads as "out of Energy".
  * ``pre_tool_call``: while spent, tool calls are blocked, so a turn in flight stops acting.

Hermes' auxiliary calls don't pass through middleware; on a spent key they fail on their own,
which is fine because the main loop ends with the reply. The DesignInstantly app holds the truth
(the owner's Polar meter and the key's limit); this plugin only shapes how a stop looks.
"""

from __future__ import annotations

import logging
import threading
import time
import uuid
from types import SimpleNamespace
from typing import Any, Dict, Iterator, Optional

logger = logging.getLogger(__name__)

OUT_OF_ENERGY_REPLY = (
    "I'm out of Energy for now, so I've stopped here. I'll pick up again when your plan renews, "
    "or you can top up Energy on the Billing page to keep me working now."
)
# How long after a refusal calls skip OpenRouter. Short, so a top-up is picked up quickly.
EXHAUSTED_TTL_SECONDS = 60.0
# OpenRouter's marker on a request refused because the key's own credit limit is spent.
_KEY_LIMIT_SOURCE = "openrouter_key_limit"

_lock = threading.Lock()
_exhausted_until = 0.0


def _exhausted() -> bool:
    with _lock:
        return time.monotonic() < _exhausted_until


def _mark_exhausted() -> None:
    global _exhausted_until
    with _lock:
        _exhausted_until = time.monotonic() + EXHAUSTED_TTL_SECONDS


def _chain(exc: Optional[BaseException]) -> Iterator[BaseException]:
    """The error and what it wraps: middleware hands us ``_DownstreamExecutionError`` (``.original``)."""
    seen = set()
    while exc is not None and id(exc) not in seen:
        seen.add(id(exc))
        yield exc
        exc = getattr(exc, "original", None) or exc.__cause__


def _has_key_limit_source(value: Any, depth: int = 3) -> bool:
    """``limit_source`` sits in the error body, possibly under ``error`` / ``metadata``."""
    if depth < 0 or not isinstance(value, dict):
        return False
    if value.get("limit_source") == _KEY_LIMIT_SOURCE:
        return True
    return any(_has_key_limit_source(child, depth - 1) for child in value.values())


def _is_key_limit(exc: BaseException) -> bool:
    """A refusal for the key's own spending limit (402/403, or a mid-stream error carrying the body)."""
    for error in _chain(exc):
        if _has_key_limit_source(getattr(error, "body", None)):
            return True
        if "key limit exceeded" in str(error).lower():
            return True
    return False


def _reply(model: str) -> SimpleNamespace:
    """A final assistant answer in the shape Hermes reads every provider response in."""
    message = SimpleNamespace(
        role="assistant", content=OUT_OF_ENERGY_REPLY, tool_calls=None, reasoning_content=None, refusal=None
    )
    return SimpleNamespace(
        id=f"energy-{uuid.uuid4()}",
        model=model,
        usage=None,
        choices=[SimpleNamespace(index=0, message=message, finish_reason="stop")],
    )


def _llm_execution(*, next_call: Any, model: str = "", **_: Any) -> Any:
    if _exhausted():
        return _reply(model)
    try:
        return next_call()
    except Exception as exc:
        if not _is_key_limit(exc):
            raise
        logger.info("designinstantly_energy: the owner's Energy key is spent; ending the run with a reply")
        _mark_exhausted()
        return _reply(model)


def _pre_tool_call(tool_name: str = "", **_: Any) -> Optional[Dict[str, str]]:
    if not _exhausted():
        return None
    return {"action": "block", "message": f"Out of Energy, so {tool_name or 'this step'} was skipped."}


def register(ctx) -> None:
    ctx.register_middleware("llm_execution", _llm_execution)
    ctx.register_hook("pre_tool_call", _pre_tool_call)
