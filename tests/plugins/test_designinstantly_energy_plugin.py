"""Tests for the designinstantly_energy plugin (plugins/designinstantly_energy/).

  * A call refused for the key's spending limit becomes Otto's final reply, in the response shape
    Hermes validates, and later calls short-circuit without reaching the provider.
  * The refusal is recognised through middleware wrapping and in either body shape.
  * Every other error still raises (including a platform-balance 402).
  * ``pre_tool_call`` blocks only while the key is spent.
"""

import importlib.util
import sys
import types
from pathlib import Path

import pytest


def _load_plugin():
    plugin_dir = Path(__file__).resolve().parents[2] / "plugins" / "designinstantly_energy"
    if "hermes_plugins" not in sys.modules:
        ns = types.ModuleType("hermes_plugins")
        ns.__path__ = []
        sys.modules["hermes_plugins"] = ns
    spec = importlib.util.spec_from_file_location(
        "hermes_plugins.designinstantly_energy",
        plugin_dir / "__init__.py",
        submodule_search_locations=[str(plugin_dir)],
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules["hermes_plugins.designinstantly_energy"] = mod
    spec.loader.exec_module(mod)
    return mod


energy = _load_plugin()


@pytest.fixture(autouse=True)
def _fresh_state():
    energy._exhausted_until = 0.0
    yield
    energy._exhausted_until = 0.0


class _StatusError(Exception):
    """Stands in for openai.APIStatusError: ``status_code`` and a parsed ``body``."""

    def __init__(self, status_code, body, message="error"):
        super().__init__(message)
        self.status_code = status_code
        self.body = body


class _Downstream(Exception):
    """Stands in for hermes_cli.middleware._DownstreamExecutionError."""

    def __init__(self, original):
        super().__init__(str(original))
        self.original = original


def _raising(exc):
    def call():
        raise exc

    return call


KEY_LIMIT_BODY = {"error": {"code": 402, "message": "Key limit exceeded", "metadata": {"limit_source": "openrouter_key_limit"}}}


def test_reply_has_the_shape_hermes_validates():
    from agent.transports.chat_completions import ChatCompletionsTransport

    reply = energy._reply("@preset/agent-hermes")
    assert ChatCompletionsTransport().validate_response(reply)
    assert reply.choices[0].message.content == energy.OUT_OF_ENERGY_REPLY
    assert reply.choices[0].finish_reason == "stop"
    assert reply.choices[0].message.tool_calls is None


def test_key_limit_refusal_becomes_the_reply_and_later_calls_short_circuit():
    response = energy._llm_execution(next_call=_raising(_Downstream(_StatusError(402, KEY_LIMIT_BODY))), model="m")
    assert response.choices[0].message.content == energy.OUT_OF_ENERGY_REPLY

    def must_not_run():
        raise AssertionError("the provider was called while the key is spent")

    assert energy._llm_execution(next_call=must_not_run).choices[0].message.content == energy.OUT_OF_ENERGY_REPLY


@pytest.mark.parametrize(
    "error",
    [
        _StatusError(403, {"limit_source": "openrouter_key_limit"}),
        _StatusError(None, {"error": {"metadata": {"limit_source": "openrouter_key_limit"}}}),
        _StatusError(403, {}, message="Key limit exceeded (daily limit)"),
    ],
)
def test_key_limit_is_recognised_in_any_body_shape(error):
    assert energy._is_key_limit(_Downstream(error))


@pytest.mark.parametrize(
    "error",
    [
        _StatusError(402, {"error": {"message": "Insufficient credits", "metadata": {"limit_source": "account_balance"}}}),
        _StatusError(429, {"error": {"message": "Rate limited"}}),
        RuntimeError("connection reset"),
    ],
)
def test_other_errors_still_raise(error):
    with pytest.raises(Exception):
        energy._llm_execution(next_call=_raising(error))
    assert not energy._exhausted()


def test_successful_calls_pass_through():
    sentinel = object()
    assert energy._llm_execution(next_call=lambda: sentinel) is sentinel


def test_tools_are_blocked_only_while_spent():
    assert energy._pre_tool_call(tool_name="terminal") is None
    energy._mark_exhausted()
    blocked = energy._pre_tool_call(tool_name="terminal")
    assert blocked["action"] == "block"
    assert "terminal" in blocked["message"]


def test_register_wires_middleware_and_hook():
    calls = []
    ctx = types.SimpleNamespace(
        register_middleware=lambda kind, cb: calls.append(("middleware", kind)),
        register_hook=lambda name, cb: calls.append(("hook", name)),
    )
    energy.register(ctx)
    assert ("middleware", "llm_execution") in calls
    assert ("hook", "pre_tool_call") in calls
