"""Experiment 1: Persistent Workspace.

This experiment writes deterministic workflow state from inside Sandbox A to a
mounted Tensorlake Cloud Volume, then verifies the same bytes through the
host-side Filesystem API.
"""

from __future__ import annotations

import contextlib
import base64
import hashlib
import importlib.metadata
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

from tensorlake.filesystem import FilesystemAPIError, FilesystemClient, FilesystemNotFoundError
from tensorlake.sandbox import FileSystemMount, Sandbox


EXPERIMENT_NAME = "01-persistent-workspace"
FILESYSTEM_NAME = "article3-stateful-agent-workspace"
SANDBOX_NAME = "article3-persistent-workspace-sandbox-a"
MOUNT_PATH = "/workspace"
EVIDENCE_PATH = "state/stage1.json"
OUTPUT_FILE = Path(__file__).with_name("output.txt")
RESULT_FILE = Path(__file__).with_name("result.json")
POLL_TIMEOUT_SECONDS = 60.0
POLL_INTERVAL_SECONDS = 2.0


class OutputLogger:
    """Mirror experiment output to console and output.txt during real execution."""

    def __init__(self, output_path: Path) -> None:
        self.output_path = output_path
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self._handle = self.output_path.open("w", encoding="utf-8")

    def close(self) -> None:
        self._handle.close()

    def line(self, text: str = "") -> None:
        print(text)
        self._handle.write(f"{text}\n")
        self._handle.flush()


def find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / ".env").exists() and (candidate / ".git").exists():
            return candidate
    raise RuntimeError("Could not locate repository root containing .env and .git")


def load_tensorlake_api_key(repo_root: Path) -> None:
    env_path = repo_root / ".env"
    if not env_path.exists():
        raise RuntimeError("Repository root .env was not found")

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key != "TENSORLAKE_API_KEY":
            continue
        value = value.strip().strip("\"'")
        if not value:
            break
        os.environ[key] = value
        return

    if not os.getenv("TENSORLAKE_API_KEY"):
        raise RuntimeError("TENSORLAKE_API_KEY is not configured in the repository root .env")


def canonical_evidence_bytes() -> bytes:
    payload = {
        "experiment": EXPERIMENT_NAME,
        "stage": 1,
        "status": "completed",
        "processed_records": [
            "doc-001",
            "doc-002",
            "doc-003",
        ],
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sandbox_write_command(expected_bytes: bytes) -> str:
    encoded_expected = base64.b64encode(expected_bytes).decode("ascii")
    script = f"""
import base64
import pathlib

mount_path = pathlib.Path({MOUNT_PATH!r})
evidence_path = mount_path / {EVIDENCE_PATH!r}
expected = base64.b64decode({encoded_expected!r})

evidence_path.parent.mkdir(parents=True, exist_ok=True)
with evidence_path.open("wb") as handle:
    handle.write(expected)
    handle.flush()

readback = evidence_path.read_bytes()
if readback != expected:
    raise SystemExit("same-sandbox readback mismatch")

print(base64.b64encode(readback).decode("ascii"))
"""
    return "python - <<'PY'\n" + script.strip() + "\nPY\nsync\n"


def log_status(logger: OutputLogger, fs: Any, label: str) -> None:
    logger.line(f"{label}:")
    with contextlib.suppress(Exception):
        status = fs.status()
        logger.line(f"  filesystem status type : {type(status).__name__}")
        for attr in ("name", "default_branch", "version", "latest_version", "head", "snapshot_count"):
            if hasattr(status, attr):
                logger.line(f"  {attr:22}: {getattr(status, attr)}")
        return
    logger.line("  filesystem status      : unavailable")


def get_or_create_filesystem(client: FilesystemClient, logger: OutputLogger) -> tuple[Any, str]:
    logger.line(f"cloud volume/filesystem : {FILESYSTEM_NAME}")
    try:
        fs = client.get(FILESYSTEM_NAME)
        logger.line("filesystem lookup       : existing filesystem found")
        logger.line("filesystem action       : reused")
        return fs, "reused"
    except FilesystemNotFoundError:
        logger.line("filesystem lookup       : filesystem not found; creating it")
    except FilesystemAPIError as exc:
        raise RuntimeError(
            "Filesystem lookup failed with a Tensorlake API error; refusing to create "
            f"{FILESYSTEM_NAME!r} after status {exc.status_code}"
        ) from exc
    except Exception as exc:
        raise RuntimeError(
            "Filesystem lookup failed unexpectedly; refusing to create "
            f"{FILESYSTEM_NAME!r}"
        ) from exc

    fs = client.create(FILESYSTEM_NAME)
    logger.line("filesystem action       : created")
    return fs, "created"


def poll_external_read(
    fs: Any,
    expected_bytes: bytes,
    expected_hash: str,
    logger: OutputLogger,
) -> tuple[bytes, str, int, float]:
    deadline = time.monotonic() + POLL_TIMEOUT_SECONDS
    attempts = 0
    last_error = "none"
    started = time.monotonic()

    while time.monotonic() < deadline:
        attempts += 1
        elapsed = time.monotonic() - started
        try:
            observed = fs.read_file(EVIDENCE_PATH)
            observed_hash = sha256_hex(observed)
            logger.line(
                f"external read attempt {attempts}: elapsed={elapsed:.2f}s bytes={len(observed)} hash={observed_hash}"
            )
            if observed == expected_bytes and observed_hash == expected_hash:
                return observed, observed_hash, attempts, time.monotonic() - started
            last_error = "content/hash mismatch"
        except Exception as exc:
            last_error = f"{type(exc).__name__}: {exc}"
            logger.line(f"external read attempt {attempts}: elapsed={elapsed:.2f}s pending ({type(exc).__name__})")

        time.sleep(POLL_INTERVAL_SECONDS)

    raise RuntimeError(
        "external Filesystem.read_file() did not observe the expected evidence "
        f"within {POLL_TIMEOUT_SECONDS:.0f}s; last result: {last_error}"
    )


def main() -> int:
    logger = OutputLogger(OUTPUT_FILE)
    sandbox = None
    try:
        repo_root = find_repo_root(Path(__file__).resolve())
        load_tensorlake_api_key(repo_root)

        sdk_version = importlib.metadata.version("tensorlake")
        expected_bytes = canonical_evidence_bytes()
        expected_hash = sha256_hex(expected_bytes)

        logger.line("Experiment 1: Persistent Workspace")
        logger.line("=" * 42)
        logger.line(f"tensorlake sdk          : {sdk_version}")
        logger.line(f"experiment              : {EXPERIMENT_NAME}")
        logger.line(f"evidence path           : {EVIDENCE_PATH}")
        logger.line(f"expected sha256         : {expected_hash}")
        logger.line("api key                 : configured (redacted)")
        logger.line()

        client = FilesystemClient()
        fs, filesystem_action = get_or_create_filesystem(client, logger)
        log_status(logger, fs, "filesystem status before sandbox")
        logger.line()

        logger.line("Creating Sandbox A with writable Cloud Volume mount")
        sandbox = Sandbox.create(
            name=SANDBOX_NAME,
            file_systems=[
                FileSystemMount(
                    file_system_id=FILESYSTEM_NAME,
                    mount_path=MOUNT_PATH,
                    read_only=False,
                )
            ],
        )
        sandbox_id = getattr(sandbox, "sandbox_id", None) or getattr(sandbox, "id", None) or "unknown"
        logger.line(f"sandbox name            : {SANDBOX_NAME}")
        logger.line(f"sandbox id              : {sandbox_id}")
        logger.line(f"mount path              : {MOUNT_PATH}")
        logger.line()

        logger.line("Writing deterministic evidence from inside Sandbox A")
        result = sandbox.run("sh", ["-lc", sandbox_write_command(expected_bytes)])
        stdout = result.stdout or ""
        stderr = result.stderr or ""
        exit_code = getattr(result, "exit_code", None)
        logger.line(f"sandbox write exit code : {exit_code}")
        if stderr.strip():
            logger.line(f"sandbox stderr          : {stderr.strip()}")
        if exit_code not in (0, None):
            raise RuntimeError(f"sandbox write command failed with exit code {exit_code}")

        try:
            same_sandbox_bytes = base64.b64decode(stdout.strip(), validate=True)
        except Exception as exc:
            raise RuntimeError("same-sandbox readback was not valid base64 bytes") from exc
        same_sandbox_hash = sha256_hex(same_sandbox_bytes)
        logger.line(f"same-sandbox bytes      : {len(same_sandbox_bytes)}")
        logger.line(f"same-sandbox sha256     : {same_sandbox_hash}")
        if same_sandbox_bytes != expected_bytes:
            raise RuntimeError("same-sandbox readback did not match expected evidence bytes")
        logger.line("same-sandbox readback   : PASS (local sanity check only)")
        logger.line()

        log_status(logger, fs, "filesystem status before external polling")
        logger.line()

        logger.line("Polling host-side Filesystem.read_file() for published shared state")
        observed_bytes, observed_hash, attempts, elapsed = poll_external_read(
            fs=fs,
            expected_bytes=expected_bytes,
            expected_hash=expected_hash,
            logger=logger,
        )
        logger.line("external read           : PASS")
        logger.line(f"external bytes          : {len(observed_bytes)}")
        logger.line(f"external sha256         : {observed_hash}")
        logger.line(f"poll attempts           : {attempts}")
        logger.line(f"poll elapsed seconds    : {elapsed:.2f}")
        logger.line()

        log_status(logger, fs, "filesystem status after external verification")
        logger.line()

        run_result = {
            "experiment": EXPERIMENT_NAME,
            "status": "PASS",
            "sdk_version": sdk_version,
            "filesystem_name": FILESYSTEM_NAME,
            "filesystem_action": filesystem_action,
            "sandbox_name": SANDBOX_NAME,
            "sandbox_id": sandbox_id,
            "mount_path": MOUNT_PATH,
            "evidence_path": EVIDENCE_PATH,
            "expected_sha256": expected_hash,
            "observed_sha256": observed_hash,
            "poll_attempts": attempts,
            "poll_elapsed_seconds": round(elapsed, 3),
        }
        RESULT_FILE.write_text(json.dumps(run_result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        logger.line("PASS criteria")
        logger.line("  sandbox write command       : PASS")
        logger.line("  same-sandbox readback       : PASS")
        logger.line("  host Filesystem.read_file   : PASS")
        logger.line("  SHA-256 content match       : PASS")
        logger.line()
        logger.line("final result            : PASS")
        return 0
    finally:
        if sandbox is not None:
            logger.line()
            logger.line("Terminating Sandbox A")
            with contextlib.suppress(Exception):
                sandbox.terminate()
                logger.line("sandbox termination     : requested")
        logger.close()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise
