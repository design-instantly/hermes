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
| `plugins/designinstantly_energy/` | Ends a run with Otto's own reply once the owner's Energy is spent, instead of failing it |
| `plugins/designinstantly_guard/` | Refuses tool calls that would read Otto's own setup (Hermes home, Sprite socket, environment, `hermes` CLI) |
| `designinstantly/bootstrap.sh` | Commissions or updates a Sprite (idempotent) |
| `designinstantly/apply.py` | Renders SOUL and the Hindsight plugin config; merges our config.yaml keys |
| `designinstantly/config.overlay.yaml` | Our config.yaml keys: model presets, disabled toolsets, turn cap, memory, MCP, cron |
| `designinstantly/hindsight.json` | Hindsight plugin config on the Sprite (server, the brand's bank, recall/retain) |
| `designinstantly/hindsight-bank.json` | The brand's bank profile; the app creates the bank from it |
| `designinstantly/manifest.json` | Template version, placeholders and secrets the app provides |

`SOUL.md` and `hermes_cli/default_soul.py` are marked `-merge` in `.gitattributes`: any upstream
change to them stops a sync so an engineer reviews it against Otto's version.

## Fleet config in OpenRouter presets

Some of Otto's config isn't in this repo: it lives in two OpenRouter presets, and an edit there
reaches every co-worker on its next call, with no push or bootstrap. Treat a preset edit like a deploy.

| Preset | Holds |
|---|---|
| `@preset/agent-hermes` | Otto's model, plus the **Web Search** and **Web Fetch** server tools (OpenRouter runs them inside the request) |
| `@preset/agent-hermes-aux` | The model for Hermes' background calls (compaction, titles, MCP sampling, approvals, the post-turn review). **No tools**, so a background call can never run a paid search |

To switch search engines (Exa, Parallel, ...), change Web Search's engine in `agent-hermes`. Pick an
explicit engine, not Auto: Auto follows the model's own search when the model has one, so swapping
the model would silently change the search vendor and its price. Keep `max_results` /
`max_total_results` (search) and `max_uses` (fetch) set, since one request can search several times.

Everything (the model, both presets' tools) runs on `OPENROUTER_API_KEY`, which is the brand owner's
Energy key: OpenRouter meters it and refuses calls once the owner's Energy is spent. Hermes' own
`web` tools are disabled so nothing searches outside the key.

## Branches

Each DesignInstantly environment runs its own branch of this fork, like the app's own branches,
so a change reaches dev first, then staging, and production last:

| Fork branch | Runs on | Set by |
|---|---|---|
| `feature/agents` (the current feature branch) | dev co-workers | `COWORKER_HERMES_BRANCH` in the app's dev env |
| `integration` | staging co-workers | `COWORKER_HERMES_BRANCH` in the app's staging env |
| `main` | production co-workers | the default when `COWORKER_HERMES_BRANCH` is unset |

The app reads `bootstrap.sh` and `hindsight-bank.json` from its environment's branch and passes it
to `bootstrap.sh` as `DI_HERMES_BRANCH`, which installs and updates from it. A push to a branch
reaches that environment's Sprites the next time their bootstrap runs (`update-coworkers.ts`,
commissioning, a spare refill), and no other environment's.

**Promoting a change:** commit on the feature branch and update dev; merge it into `integration`
for staging; merge `integration` into `main` for production.

**Syncing upstream:** always with git, never GitHub's "Sync fork" button (it ignores `.gitattributes`).
Merge into the feature branch first, so upstream changes take the same dev → staging → production path:

```bash
git fetch upstream && git checkout -b sync/upstream feature/agents && git merge upstream/main
# resolve the conflicts on our owned files, then open a PR into feature/agents
```

## Running it

```bash
bootstrap.sh --base        # a spare: Hermes + plugins only, no brand or secrets (the app keeps 5 ready)
bootstrap.sh <input_dir>   # commissioning: agent.json, secrets.env, fire-public.pem
bootstrap.sh               # update in place, reusing the values kept from commissioning
```

The app commissions a brand by claiming a spare and running `bootstrap.sh <input_dir>` on it, which
skips the install when the spare is on its branch's current commit.

Run a copy outside the checkout (the DesignInstantly app downloads it to `/tmp`): the update step
rewrites the checkout. A fresh Sprite takes ~6 minutes (Hermes install); updates take seconds when
`main` hasn't moved.
