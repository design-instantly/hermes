"""A2UI surfaces for API-server clients — DesignInstantly's interim patch.

OWNED BY DESIGNINSTANTLY, NOT UPSTREAM. Upstream Hermes hands a /v1/runs client no UI from a
tool call: ``tool.completed`` carries a text preview cut at 500 characters, nothing else.
  - NousResearch/hermes-agent#61095  "Support MCP apps" (tracking issue)
  - NousResearch/hermes-agent#132426 server side of an MCP Apps host (gateway methods)
  - NousResearch/hermes-agent#65845  AG-UI adapter for the API server (AG-UI can carry A2UI)
DesignInstantly's MCP server returns the interfaces its co-workers build (its render_ui tool) as
A2UI messages in an embedded resource of mimeType ``application/a2ui+json``. This lifts them out
of the tool's result and onto its ``tool.completed`` event as ``a2ui``, a list of A2UI messages,
which the DesignInstantly app renders natively:

  1. ``remember()`` — the MCP tool handler records a result's A2UI messages
     (tools/mcp_tool_handlers.py).
  2. ``take()`` — the runs API attaches them to the call's ``tool.completed`` event
     (gateway/platforms/api_server_runs.py).

WHEN SYNCING UPSTREAM: check whether Hermes now hands tool UI to runs clients (the issues/PRs
above, or A2UI / AG-UI support in the API server). If it does, move the DesignInstantly app onto
it, then delete this module and every line marked "DESIGNINSTANTLY: A2UI".
"""

import json
import logging
import threading
import time
from collections import deque
from typing import Any, Deque, Dict, List, Optional, Tuple

from tools.mcp_tool_common import mcp_field
from tools.mcp_tool_schema import mcp_prefixed_tool_name

logger = logging.getLogger(__name__)

A2UI_MIME_TYPE = "application/a2ui+json"
# Messages not picked up by their ``tool.completed`` within this long are dropped.
_RECORD_TTL_SEC = 600
# A surface above this is not forwarded (the model still gets the tool's text).
_MAX_BYTES = 256_000

_lock = threading.Lock()
# Registry tool name -> messages in call order. A tool's ``tool.completed`` takes the oldest:
# calls of one tool finish in order within a run, and a co-worker Sprite serves one brand.
_records: Dict[str, Deque[Tuple[float, List[Any]]]] = {}


def _messages(result: Any) -> List[Any]:
    """The A2UI messages in a ``CallToolResult``'s ``application/a2ui+json`` resources."""
    messages: List[Any] = []
    for block in getattr(result, "content", None) or []:
        resource = getattr(block, "resource", None)
        if resource is None or mcp_field(resource, "mime_type", "mimeType", "") != A2UI_MIME_TYPE:
            continue
        text = getattr(resource, "text", None)
        if not isinstance(text, str) or len(text) > _MAX_BYTES:
            continue
        try:
            parsed = json.loads(text)
        except ValueError:
            logger.warning("A2UI resource %s is not JSON", getattr(resource, "uri", ""))
            continue
        if isinstance(parsed, list):
            messages.extend(parsed)
    return messages


def remember(server_name: str, tool_name: str, result: Any) -> None:
    """Record a finished call's A2UI messages (no-op for a result without any)."""
    if result is None or mcp_field(result, "is_error", "isError", False):
        return
    messages = _messages(result)
    if not messages:
        return
    now = time.monotonic()
    with _lock:
        queue = _records.setdefault(mcp_prefixed_tool_name(server_name, tool_name), deque())
        while queue and now - queue[0][0] > _RECORD_TTL_SEC:
            queue.popleft()
        queue.append((now, messages))


def take(registry_tool_name: Optional[str]) -> Optional[List[Any]]:
    """The oldest recorded messages of this tool, removed; None when it has none."""
    if not registry_tool_name:
        return None
    with _lock:
        queue = _records.get(registry_tool_name)
        return queue.popleft()[1] if queue else None
