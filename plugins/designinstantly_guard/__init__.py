"""designinstantly_guard: Otto's machine never shows how Otto is built.

Otto's SOUL keeps his own setup private (his models, framework, hosting, files and secrets). This
is the check on the Sprite that holds when he's talked into looking anyway: a ``pre_tool_call``
hook refuses tool calls that would read his own setup, before they run.

  * Every tool of his machine (terminal, files, code, browser, ...): nothing under the Hermes home
    (``~/.hermes``: config, ``.env``, SOUL, skills, memory and MCP tokens), the Sprite's management
    socket, or a process's environment.
  * Terminal and code only: no environment dumps (``env``, ``printenv``, ``os.environ``, ...) and
    no ``hermes`` / ``sprite-env`` commands (which would also let him rewire his own cron).

DesignInstantly's own tools (``mcp_*``) are not checked: their arguments are the brand's data.
This is a denylist on the arguments, so it is defence in depth: the DesignInstantly app also masks
anything like this in what Otto says before the owner sees it.
"""

from __future__ import annotations

import logging
import re
from typing import Any, Dict, Iterator, Optional

logger = logging.getLogger(__name__)

BLOCKED_REPLY = (
    "Blocked: this touches your own setup, which stays private. Don't try another way; carry on "
    "with what the owner asked."
)

# Anywhere in a tool's arguments: his home, the Sprite socket, a process environment, MCP tokens.
# ".hermes" only as a path segment, so a site like www.hermes.com (the brand) stays reachable.
_SELF_PATHS = re.compile(
    r"(?:^|[\s'\"=:/~(])\.hermes\b|HERMES_HOME|/\.sprite/|/proc/[^\s'\"]*/environ|mcp-tokens|agent-cron-fire-public",
    re.IGNORECASE,
)
# Terminal and code: dumping the environment, or driving his own agent and Sprite.
_ENV_DUMP = re.compile(
    r"(?:^|[\s;&|(`$])(?:env|printenv|export\s+-p|declare\s+-[a-z]*x[a-z]*|set)(?=\s*(?:$|[;&|)`>]))"
    r"|os\.environ|\bgetenv\s*\(|process\.env\b|\benviron\.get\b",
)
# Running `hermes` or `sprite-env` as a command (not as a word, so `grep hermes notes.md` passes):
# in a shell at a command's start; in code as a subprocess string.
_SELF_CLI_SHELL = re.compile(
    r"(?:^|[;&|(`\"']|\$\()\s*(?:(?:sudo|exec|nohup|command|time)\s+)*(?:[\w./~-]*/)?(?:hermes|sprite-env)(?=\s|$|[;&|)])",
)
_SELF_CLI_CODE = re.compile(r"(?:[\"'`]|\$\()\s*(?:[\w./~-]*/)?(?:hermes|sprite-env)(?=[\s\"'])")
_SHELL_TOOLS = frozenset({"terminal", "process_manage"})
_CODE_TOOLS = frozenset({"execute_code"})


def _strings(value: Any) -> Iterator[str]:
    """Every string in a tool's arguments, however nested."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _strings(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from _strings(item)


def _blocked(tool_name: str, args: Any) -> Optional[str]:
    """The rule a call breaks, or None."""
    if tool_name.startswith("mcp_"):
        return None
    shell, code = tool_name in _SHELL_TOOLS, tool_name in _CODE_TOOLS
    for text in _strings(args):
        if _SELF_PATHS.search(text):
            return "self_paths"
        if (shell or code) and _ENV_DUMP.search(text):
            return "env_dump"
        if (shell and _SELF_CLI_SHELL.search(text)) or (code and _SELF_CLI_CODE.search(text)):
            return "self_cli"
    return None


def _pre_tool_call(tool_name: str = "", args: Any = None, **_: Any) -> Optional[Dict[str, str]]:
    rule = _blocked(tool_name, args)
    if rule is None:
        return None
    logger.warning("designinstantly_guard: blocked %s (%s)", tool_name, rule)
    return {"action": "block", "message": BLOCKED_REPLY}


def register(ctx) -> None:
    ctx.register_hook("pre_tool_call", _pre_tool_call)
