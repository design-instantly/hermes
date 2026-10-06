#!/bin/bash
# Bring this Sprite's co-worker (Otto) to the main branch of DesignInstantly's Hermes fork.
# Idempotent: commissioning runs it with inputs; re-running it without inputs updates in place.
#
# Usage: bootstrap.sh [input_dir]
#        bootstrap.sh --base
#   --base                       a spare: install Hermes and plugins only (no brand, no secrets, no
#                                gateway). Commissioning later claims it and runs with an input_dir,
#                                which then takes seconds because the install is already done.
#   <input_dir>/agent.json       non-secret values for the template placeholders (manifest.json "placeholders")
#   <input_dir>/secrets.env      KEY=value lines for manifest.json "secrets" (merged into ~/.hermes/.env)
#   <input_dir>/fire-public.pem  agent-cron's fire-token public key
# Without input_dir it reuses what an earlier run kept: ~/.hermes/di-agent.json, .env and the key.
#
# Always run a copy outside the checkout (e.g. /tmp): the update step rewrites the checkout, and
# bash reads a script as it runs. The exit code is written to $DI_BOOTSTRAP_STATUS (default
# /tmp/di-bootstrap.status) so a provisioner that started this detached can poll for completion.
set -euo pipefail

DI_HERMES_REPO="${DI_HERMES_REPO:-https://github.com/design-instantly/hermes.git}"
DI_HERMES_BRANCH="${DI_HERMES_BRANCH:-main}"
DI_HERMES_RAW="${DI_HERMES_REPO%.git}"
DI_HERMES_RAW="https://raw.githubusercontent.com/${DI_HERMES_RAW#https://github.com/}"

ARGS=("$@")
BASE=0
if [ "${1:-}" = "--base" ]; then BASE=1; shift; fi
INPUT_DIR=""
if [ -n "${1:-}" ]; then INPUT_DIR="$(cd "$1" && pwd)"; fi
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
CHECKOUT="$HERMES_HOME/hermes-agent"
TEMPLATE_DIR="$CHECKOUT/designinstantly"
VALUES="$HERMES_HOME/di-agent.json"
STATUS_FILE="${DI_BOOTSTRAP_STATUS:-/tmp/di-bootstrap.status}"
export PATH="$HOME/.local/bin:/.sprite/bin:$PATH"
log() { echo "[bootstrap] $*"; }

# ── 0. Keep the Sprite awake for the whole run ────────────────────────────────
# A detached process holds no session or request, so without a Sprite task the VM may
# pause mid-install. The task expires on its own if this script dies.
sprite_api() { curl -s --unix-socket /.sprite/api.sock -H 'Content-Type: application/json' "$@" >/dev/null 2>&1 || true; }
HEARTBEAT=""
if [ -S /.sprite/api.sock ]; then
  sprite_api -X POST http://sprite/v1/tasks -d '{"name":"di-bootstrap","expire":"5m"}'
  ( while sleep 60; do sprite_api -X PUT http://sprite/v1/tasks/di-bootstrap -d '{"expire":"5m"}'; done ) &
  HEARTBEAT=$!
fi
stop_heartbeat() { [ -n "$HEARTBEAT" ] && kill "$HEARTBEAT" 2>/dev/null; HEARTBEAT=""; }
finish() {
  code=$?
  stop_heartbeat
  [ -S /.sprite/api.sock ] && sprite_api -X DELETE http://sprite/v1/tasks/di-bootstrap
  echo "$code" > "$STATUS_FILE"
}
if [ "${DI_BOOTSTRAP_REEXEC:-}" != 1 ]; then rm -f "$STATUS_FILE"; fi
trap finish EXIT

# ── 1. Hermes (and this template, which lives in it) at the fork's branch ────
remote_sha=$(git ls-remote "$DI_HERMES_REPO" "refs/heads/$DI_HERMES_BRANCH" | cut -f1)
[ -n "$remote_sha" ] || { log "branch $DI_HERMES_BRANCH not found on $DI_HERMES_REPO"; exit 1; }
current_sha=$(git -C "$CHECKOUT" rev-parse HEAD 2>/dev/null || echo none)
if [ "$current_sha" != "$remote_sha" ]; then
  log "installing $DI_HERMES_BRANCH@${remote_sha:0:10} (was ${current_sha:0:10})"
  curl -fsSL "$DI_HERMES_RAW/$DI_HERMES_BRANCH/scripts/install.sh" -o /tmp/hermes-install.sh
  HERMES_REPO_URL="$DI_HERMES_REPO" bash /tmp/hermes-install.sh --non-interactive --skip-browser --branch "$DI_HERMES_BRANCH" \
    >/tmp/hermes-install.log 2>&1 || { tail -40 /tmp/hermes-install.log; exit 1; }
  rm -f /tmp/hermes-install.sh
else
  log "Hermes already at $DI_HERMES_BRANCH@${remote_sha:0:10}"
fi

# Continue with the checkout's own copy of this script, so every step matches the files it uses.
if [ "${DI_BOOTSTRAP_REEXEC:-}" != 1 ] && ! cmp -s "$0" "$TEMPLATE_DIR/bootstrap.sh"; then
  next="/tmp/di-bootstrap.$$.sh"
  cp "$TEMPLATE_DIR/bootstrap.sh" "$next"
  stop_heartbeat
  trap - EXIT
  exec env DI_BOOTSTRAP_REEXEC=1 DI_BOOTSTRAP_STATUS="$STATUS_FILE" bash "$next" "${ARGS[@]}"
fi

manifest() { python3 -c "import json,sys; d=json.load(open('$TEMPLATE_DIR/manifest.json')); print(eval('d' + sys.argv[1]))" "$1"; }
VERSION=$(manifest "['version']")
HINDSIGHT_PLUGIN=$(manifest "['plugins']['hindsight']['catalog']")

# ── 2. Hermes' bundled skill catalogue stays ──────────────────────────────────
# Undo an earlier opt-out, if any.
if [ -f "$HERMES_HOME/.no-bundled-skills" ]; then
  hermes skills opt-in --sync >/dev/null
fi

if [ "$BASE" = 0 ]; then
# ── 3. Inputs: keep the brand's values; merge secrets (.env is agent-owned) ───
touch "$HERMES_HOME/.env"; chmod 600 "$HERMES_HOME/.env"
set_env() {  # set_env KEY VALUE
  sed -i "/^$1=/d" "$HERMES_HOME/.env"
  printf '%s=%s\n' "$1" "$2" >> "$HERMES_HOME/.env"
}
if [ -n "$INPUT_DIR" ]; then
  cp "$INPUT_DIR/agent.json" "$VALUES"
  while IFS='=' read -r key value; do
    [ -n "$key" ] && [ "${key:0:1}" != "#" ] && set_env "$key" "$value"
  done < <(tr -d '\r' < "$INPUT_DIR/secrets.env")
  tr -d '\r' < "$INPUT_DIR/fire-public.pem" > "$HERMES_HOME/agent-cron-fire-public.pem"
fi
[ -f "$VALUES" ] || { log "no $VALUES: run once with an input_dir (commissioning)"; exit 1; }
grep -q '^API_SERVER_KEY=' "$HERMES_HOME/.env" || set_env API_SERVER_KEY "$(openssl rand -hex 32)"
set_env API_SERVER_ENABLED true
set_env API_SERVER_HOST 0.0.0.0
set_env API_SERVER_PORT 8642
set_env HERMES_TIMEZONE "$(python3 -c "import json; print(json.load(open('$VALUES'))['TIMEZONE'])")"

# ── 4. Template files + config overlay ────────────────────────────────────────
# (The brand's Hindsight bank is created by the DesignInstantly app before this runs.)
uv run --quiet --no-project --with pyyaml python3 "$TEMPLATE_DIR/apply.py" "$TEMPLATE_DIR" "$VALUES"
hermes config set cron.chronos.nas_jwks_url "$(cat "$HERMES_HOME/agent-cron-fire-public.pem")" >/dev/null
fi

# ── 5. Plugins ────────────────────────────────────────────────────────────────
# Hindsight comes from the Hermes catalog. Hermes only installs a plugin's Python deps after a
# y/N answer on a TTY, so answer it inside a pty. The designinstantly cron provider is bundled in
# this fork (plugins/cron_providers/designinstantly); nothing to install.
memory_ready() { hermes memory status 2>/dev/null | grep -Eq "Status: +available"; }
in_pty() {  # in_pty "<hermes args>" — answers "y" to Hermes' dependency prompt; returns when the command does
  # script(1) exits only once its stdin closes, not when the command does, and closing stdin
  # early hangs up the command. So the feeder holds stdin open until hermes has finished
  # (15 minutes at most).
  local done_flag; done_flag=$(mktemp -u /tmp/di-pty.XXXXXX)
  script -qec "hermes $1; touch $done_flag" /dev/null \
    < <(printf 'y\ny\n'; for _ in $(seq 900); do [ -e "$done_flag" ] && break; sleep 1; done) \
    >>/tmp/hindsight-plugin.log 2>&1 || true
  rm -f "$done_flag"
}
# A spare stops here: Hermes and the Hindsight plugin's dependencies are installed; the brand's
# run enables the plugin once its config exists.
if [ "$BASE" = 1 ]; then
  [ -d "$HERMES_HOME/plugins/hindsight" ] || in_pty "plugins install $HINDSIGHT_PLUGIN"
  [ -d "$HERMES_HOME/plugins/hindsight" ] || { log "hindsight plugin did not install"; tail -20 /tmp/hindsight-plugin.log; exit 1; }
  sha=$(git -C "$CHECKOUT" rev-parse HEAD)
  printf '{"version":"%s","branch":"%s","commit":"%s","built_at":"%s"}\n' \
    "$VERSION" "$DI_HERMES_BRANCH" "$sha" "$(date -u +%FT%TZ)" > "$HERMES_HOME/di-base.json"
  log "base done: $DI_HERMES_BRANCH@${sha:0:10}"
  exit 0
fi
if ! memory_ready; then
  if [ -d "$HERMES_HOME/plugins/hindsight" ]; then
    in_pty "plugins enable $HINDSIGHT_PLUGIN"
  else
    in_pty "plugins install $HINDSIGHT_PLUGIN --enable"
  fi
  memory_ready || { log "hindsight plugin not available"; tail -20 /tmp/hindsight-plugin.log; exit 1; }
fi

# ── 6. Gateway as a Sprite service (the Sprite URL routes to it and wakes it) ──
if sprite-env services get hermes-gateway >/dev/null 2>&1; then
  sprite-env services restart hermes-gateway >/dev/null 2>&1
else
  sprite-env services create hermes-gateway --cmd "$HOME/.local/bin/hermes" --args gateway,run \
    --dir "$HOME" --env "HOME=$HOME,PATH=$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin" \
    --http-port 8642 --no-stream >/dev/null
fi
for _ in $(seq 1 60); do curl -sf -o /dev/null localhost:8642/health && break; sleep 2; done
curl -sf -o /dev/null localhost:8642/health || { log "gateway did not become healthy"; exit 1; }

# ── 7. Record what was applied ────────────────────────────────────────────────
sha=$(git -C "$CHECKOUT" rev-parse HEAD)
printf '{"version":"%s","branch":"%s","commit":"%s","applied_at":"%s"}\n' \
  "$VERSION" "$DI_HERMES_BRANCH" "$sha" "$(date -u +%FT%TZ)" > "$HERMES_HOME/di-template.json"
[ -n "$INPUT_DIR" ] && rm -rf "$INPUT_DIR"
log "done: template $VERSION, $DI_HERMES_BRANCH@${sha:0:10}"
