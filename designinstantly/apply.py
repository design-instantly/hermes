"""Render the DesignInstantly template for one agent and lay it down in HERMES_HOME. Idempotent.

Called by bootstrap.sh via `uv run --no-project --with pyyaml python3 apply.py <template_dir> <agent.json>`,
where <template_dir> is this fork's designinstantly/ directory.

Template-owned files are (re)written on every run: SOUL.md (rendered from the fork's root SOUL.md),
hindsight/config.json, and the config.yaml keys in config.overlay.yaml. The cron provider is bundled
in the fork (plugins/cron_providers/designinstantly), not copied. Everything else in HERMES_HOME —
.env secrets, skills, sessions, jobs — is left alone.
"""

import json
import os
import re
import shutil
import sys
from pathlib import Path

import yaml

PLACEHOLDER = re.compile(r"\{\{([A-Z_]+)\}\}")


def render(text: str, values: dict) -> str:
    def sub(m: re.Match) -> str:
        key = m.group(1)
        if key not in values:
            raise SystemExit(f"apply.py: no value for placeholder {key}")
        return str(values[key])

    return PLACEHOLDER.sub(sub, text)


def deep_merge(base: dict, overlay: dict) -> dict:
    """Overlay wins for scalars and lists; nested dicts merge key by key."""
    for key, value in overlay.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            deep_merge(base[key], value)
        else:
            base[key] = value
    return base


def write_text(path: Path, text: str, mode: int | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)
    if mode is not None:
        path.chmod(mode)


def main() -> None:
    template = Path(sys.argv[1]).resolve()
    values = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    home = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))

    # Persona (the fork's root SOUL.md, Otto) and memory wiring.
    write_text(home / "SOUL.md", render((template.parent / "SOUL.md").read_text(encoding="utf-8"), values))
    write_text(home / "hindsight" / "config.json", render((template / "hindsight.json").read_text(encoding="utf-8"), values))

    # The cron provider used to be copied here; it is bundled in the fork now, and a stale user
    # copy would shadow the bundled one.
    old_plugin = home / "plugins" / "designinstantly"
    if old_plugin.exists():
        shutil.rmtree(old_plugin)

    # config.yaml: deep-merge the rendered overlay (keeps Hermes' own keys, e.g. _config_version).
    config_path = home / "config.yaml"
    config = yaml.safe_load(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
    overlay = yaml.safe_load(render((template / "config.overlay.yaml").read_text(encoding="utf-8"), values))
    write_text(config_path, yaml.safe_dump(deep_merge(config or {}, overlay), sort_keys=False, allow_unicode=True))

    print(f"apply.py: template applied to {home}")


if __name__ == "__main__":
    main()
