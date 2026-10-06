# DesignInstantly co-worker (Otto)

DesignInstantly's fork of Hermes. Every brand gets a co-worker, Otto, running this fork on its own
Fly Sprite, with a Hindsight memory bank and DesignInstantly's MCP tools. What makes Hermes into Otto
lives here; the DesignInstantly app creates the Sprite and the brand's memory bank, mints the brand's
keys, and runs `bootstrap.sh`.

## What's ours

| Path | What |
|---|---|
| `SOUL.md` (repo root) | Otto's persona, rendered per brand into `~/.hermes/SOUL.md` |
| `hermes_cli/default_soul.py` | Hermes' built-in fallback persona, also Otto |
| `plugins/cron_providers/designinstantly/` | Cron provider backed by agent-cron, so idle Sprites can sleep |
| `designinstantly/bootstrap.sh` | Commissions or updates a Sprite (idempotent) |
| `designinstantly/apply.py` | Renders SOUL and the Hindsight plugin config; merges our config.yaml keys |
| `designinstantly/config.overlay.yaml` | Our config.yaml keys: model preset, disabled toolsets, memory, MCP, cron |
| `designinstantly/hindsight.json` | Hindsight plugin config on the Sprite (server, the brand's bank, recall/retain) |
| `designinstantly/hindsight-bank.json` | The brand's bank profile; the app creates the bank from it |
| `designinstantly/manifest.json` | Template version, placeholders and secrets the app provides |

`SOUL.md` and `hermes_cli/default_soul.py` are marked `-merge` in `.gitattributes`: any upstream
change to them stops a sync so an engineer reviews it against Otto's version.

## Branch

`main` is what every co-worker runs: `bootstrap.sh` installs and updates from it, and the app
downloads `bootstrap.sh` and `hindsight-bank.json` from it. A push to `main` reaches each Sprite the
next time its bootstrap runs.

**Syncing upstream:** always with git, never GitHub's "Sync fork" button (it ignores `.gitattributes`):

```bash
git fetch upstream && git checkout -b sync/upstream main && git merge upstream/main
# resolve the conflicts on our owned files, then open a PR into main
```

## Running it

```bash
bootstrap.sh --base        # a spare: Hermes + plugins only, no brand or secrets (the app keeps 5 ready)
bootstrap.sh <input_dir>   # commissioning: agent.json, secrets.env, fire-public.pem
bootstrap.sh               # update in place, reusing the values kept from commissioning
```

The app commissions a brand by claiming a spare and running `bootstrap.sh <input_dir>` on it, which
skips the install when the spare is on `main`'s current commit.

Run a copy outside the checkout (the DesignInstantly app downloads it to `/tmp`): the update step
rewrites the checkout. A fresh Sprite takes ~6 minutes (Hermes install); updates take seconds when
`main` hasn't moved.
