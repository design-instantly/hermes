"""designinstantly — Hermes cron provider backed by DesignInstantly's agent-cron (DBOS).

Replaces the built-in 60s ticker so an idle Sprite can sleep. For every enabled job,
agent-cron holds a durable one-shot at the job's ``next_run_at``; at that time it POSTs
``/api/cron/fire`` with an ES256 JWT, which Hermes verifies through the ``cron.chronos.*``
settings (``nas_jwks_url`` = our public key PEM, ``expected_audience``, ``portal_url`` = issuer).

While a fired job runs, the provider holds a Sprite *task* so the VM cannot pause mid-run.

Config (config.yaml):
    cron.provider: designinstantly
    cron.designinstantly.arm_url: https://agent-cron.<domain>/v1
    cron.designinstantly.agent_id: <this Sprite's name>
Secret (.env):
    AGENT_CRON_ARM_KEY=<this agent's arm key: HMAC-SHA256(agent-cron master key, agent_id)>
"""

from __future__ import annotations

import http.client
import json
import logging
import os
import socket
import threading
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, Set

from cron.scheduler_provider import CronScheduler

logger = logging.getLogger("cron.designinstantly")

_ARM_TIMEOUT_SECONDS = 15
_SPRITE_API_SOCKET = "/.sprite/api.sock"
# A Sprite task expires on its own if we die; the heartbeat keeps extending it while a run lasts.
_TASK_TTL = "5m"
_TASK_HEARTBEAT_SECONDS = 60


def _cfg(*keys: str, default: Any = "") -> Any:
    """Read a config value (no network)."""
    try:
        from hermes_cli.config import cfg_get, load_config
        return cfg_get(load_config(), *keys, default=default)
    except Exception:
        return default


def _is_schedulable(job: Dict[str, Any]) -> bool:
    return bool(job.get("enabled") and job.get("next_run_at") and job.get("state") != "paused")


# ── Sprite task API (keeps the VM awake while a job runs) ─────────────────────


class _UnixHTTPConnection(http.client.HTTPConnection):
    def __init__(self, path: str, timeout: float = 5.0) -> None:
        super().__init__("sprite", timeout=timeout)
        self._path = path

    def connect(self) -> None:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        sock.connect(self._path)
        self.sock = sock


def _sprite_task(method: str, path: str, body: Dict[str, Any] | None = None) -> None:
    """Best-effort call to the Sprite management socket; a no-op when not on a Sprite."""
    if not os.path.exists(_SPRITE_API_SOCKET):
        return
    conn = _UnixHTTPConnection(_SPRITE_API_SOCKET)
    try:
        payload = json.dumps(body) if body is not None else None
        headers = {"Content-Type": "application/json"} if payload is not None else {}
        conn.request(method, path, body=payload, headers=headers)
        resp = conn.getresponse()
        resp.read()
        # 409 on POST = the task already exists (claim_fire registered it first) — expected.
        if resp.status >= 400 and not (method == "POST" and resp.status == 409):
            logger.warning("Sprite task %s %s -> HTTP %s", method, path, resp.status)
    except Exception as e:
        logger.warning("Sprite task %s %s failed: %s", method, path, e)
    finally:
        conn.close()


def _task_name(job_id: str) -> str:
    return f"hermes-cron-{job_id}"


def _hold_awake(job_id: str) -> None:
    """Register the Sprite task. Must happen BEFORE the fire webhook answers 202: once the
    request completes, the Sprite may pause before the background run thread is scheduled."""
    _sprite_task("POST", "/v1/tasks", {"name": _task_name(job_id), "expire": _TASK_TTL})


def _release_awake(job_id: str) -> None:
    _sprite_task("DELETE", f"/v1/tasks/{_task_name(job_id)}")


class _Heartbeat:
    """Context manager: keep extending an already-registered Sprite task while a run lasts."""

    def __init__(self, job_id: str) -> None:
        self._job_id = job_id
        self._stop = threading.Event()

    def __enter__(self) -> "_Heartbeat":
        def beat() -> None:
            while not self._stop.wait(_TASK_HEARTBEAT_SECONDS):
                _sprite_task("PUT", f"/v1/tasks/{_task_name(self._job_id)}", {"expire": _TASK_TTL})

        threading.Thread(target=beat, name=f"sprite-task-{self._job_id}", daemon=True).start()
        return self

    def __exit__(self, *exc: Any) -> None:
        self._stop.set()
        _release_awake(self._job_id)


# ── Provider ──────────────────────────────────────────────────────────────────


class DesignInstantlyCronScheduler(CronScheduler):
    """agent-cron-backed external cron provider (scale-to-zero)."""

    def __init__(self) -> None:
        self._lock = threading.Lock()

    @property
    def name(self) -> str:
        return "designinstantly"

    def is_available(self) -> bool:
        """Config presence only — no network. Unavailable -> built-in ticker takes over."""
        return bool(
            _cfg("cron", "designinstantly", "arm_url")
            and _cfg("cron", "designinstantly", "agent_id")
            and os.environ.get("AGENT_CRON_ARM_KEY")
        )

    def start(self, stop_event, *, adapters=None, loop=None, interval=60):
        """Converge agent-cron with jobs.json, then RETURN — no loop, no periodic wake."""
        self.recover_interrupted()
        self._reconcile_logged("start()")

    def stop(self) -> None:
        pass

    def on_jobs_changed(self) -> None:
        self._reconcile_logged("on_jobs_changed")

    def register_job(self, job: Dict[str, Any]) -> None:
        """Arm a newly created job; raises so creation can report a failed arm."""
        if _is_schedulable(job):
            self._arm(job)

    def reconcile(self) -> None:
        """Arm every schedulable job at its current next_run_at (idempotent server-side) and
        disarm jobs we armed before that are gone, paused or finished."""
        from cron.jobs import load_jobs

        desired = {j["id"]: j for j in load_jobs() if _is_schedulable(j)}
        with self._lock:
            previously_armed = self._load_armed()
            for job in desired.values():
                try:
                    self._arm(job)
                except Exception as e:
                    logger.warning("designinstantly: arm %s failed: %s", job["id"], e)
            for job_id in previously_armed - desired.keys():
                try:
                    self._post("disarm", {"agentId": self._agent_id(), "jobId": job_id})
                except Exception as e:
                    logger.warning("designinstantly: disarm %s failed: %s", job_id, e)
            self._save_armed(set(desired.keys()))

    # No ``fire_due`` override: keep the split claim/fire contract (see Chronos).

    def claim_fire(self, job_id: str, *, force: bool = False, manual: bool = False) -> dict | None:
        """Runs synchronously inside the fire webhook, before it answers — so the Sprite task is
        in place before the request completes and the VM is allowed to pause."""
        _hold_awake(job_id)
        claimed = super().claim_fire(job_id, force=force, manual=manual)
        if claimed is None:
            _release_awake(job_id)  # duplicate / lost claim: nothing will run
        return claimed

    def fire_claimed(self, claimed_job: dict, *, adapters: Any = None, loop: Any = None, cancel_event: Any = None) -> bool:
        job_id = claimed_job["id"]
        _hold_awake(job_id)  # idempotent re-register: covers callers that skipped claim_fire
        with _Heartbeat(job_id):
            ran = super().fire_claimed(claimed_job, adapters=adapters, loop=loop, cancel_event=cancel_event)
        if ran:
            from cron.jobs import get_job
            job = get_job(job_id)
            if job and _is_schedulable(job):
                try:
                    self._arm(job)
                except Exception as e:
                    logger.warning("designinstantly: re-arm %s after fire failed: %s", job_id, e)
        return ran

    # ── internals ──

    def _reconcile_logged(self, what: str) -> None:
        try:
            self.reconcile()
        except Exception as e:
            logger.warning("designinstantly %s reconcile failed: %s", what, e)

    def _arm(self, job: Dict[str, Any]) -> None:
        self._post("arm", {"agentId": self._agent_id(), "jobId": job["id"], "fireAt": job["next_run_at"]})

    @staticmethod
    def _agent_id() -> str:
        return str(_cfg("cron", "designinstantly", "agent_id"))

    def _post(self, action: str, body: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{str(_cfg('cron', 'designinstantly', 'arm_url')).rstrip('/')}/{action}"
        req = urllib.request.Request(
            url,
            data=json.dumps(body).encode(),
            method="POST",
            headers={
                "Authorization": f"Bearer {os.environ.get('AGENT_CRON_ARM_KEY', '')}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=_ARM_TIMEOUT_SECONDS) as resp:
                return json.loads(resp.read() or b"{}")
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"agent-cron {action} -> HTTP {e.code}: {e.read()[:300]!r}") from e

    @staticmethod
    def _armed_file() -> Path:
        from hermes_constants import get_hermes_home
        return Path(get_hermes_home()) / "cron" / "designinstantly_armed.json"

    def _load_armed(self) -> Set[str]:
        try:
            return set(json.loads(self._armed_file().read_text(encoding="utf-8")))
        except Exception:
            return set()

    def _save_armed(self, ids: Set[str]) -> None:
        path = self._armed_file()
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(sorted(ids)), encoding="utf-8")
        tmp.replace(path)


def register(ctx) -> None:
    """Plugin entrypoint — cron provider discovery collects the provider here."""
    ctx.register_cron_scheduler(DesignInstantlyCronScheduler())
