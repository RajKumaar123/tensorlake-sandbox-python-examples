"""Experiment 2: Replace the Compute.

This experiment proves that workflow state written by Experiment 1 remains
usable after Sandbox A has been terminated, and that a new Sandbox B can mount
the same Tensorlake Cloud Volume, verify Stage 1, and write Stage 2.
"""

from __future__ import annotations

import base64
import contextlib
import hashlib
import importlib.metadata
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

from tensorlake.filesystem import FilesystemClient, FilesystemNotFoundError
from tensorlake.sandbox import FileSystemMount, Sandbox


EXPERIMENT_NAME = "02-replace-the-compute"
FILESYSTEM_NAME = "article3-stateful-agent-workspace"
SANDBOX_B_NAME = "article3-replace-compute-sandbox-b"
MOUNT_PATH = "/workspace"
STAGE1_PATH = "state/stage1.json"
STAGE1_EXPECTED_BYTES = 124
STAGE1_EXPECTED_SHA256 = "d557785c9e71629419e18b2e0f70eba9897dd84b9ede8979288b83929f7d3872"
STAGE2_PATH = "state/stage2.json"
OUTPUT_FILE = Path(__file__).with_name("output.txt")
RESULT_FILE = Path(__file__).with_name("result.json")
POLL_TIMEOUT_SECONDS = 60.0
POLL_INTERVAL_SECONDS = 2.0


class OutputLogger:
    """Mirror real experiment output to console and output.txt."""

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


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_stage2_bytes() -> bytes:
    payload = {
        "continued_from": STAGE1_PATH,
        "experiment": EXPERIMENT_NAME,
        "output_records": [
            "stage2-output-001",
            "stage2-output-002",
            "stage2-output-003",
        ],
        "stage": 2,
        "status": "completed",
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"


def validate_stage1_bytes(data: bytes, context: str) -> None:
    observed_hash = sha256_hex(data)
    if len(data) != STAGE1_EXPECTED_BYTES:
        raise RuntimeError(f"{context} Stage 1 byte count mismatch: {len(data)}")
    if observed_hash != STAGE1_EXPECTED_SHA256:
        raise RuntimeError(f"{context} Stage 1 SHA-256 mismatch: {observed_hash}")


def sandbox_b_command(stage2_bytes: bytes) -> str:
    encoded_stage2 = base64.b64encode(stage2_bytes).decode("ascii")
    script = f"""
import base64
import hashlib
import pathlib

mount_path = pathlib.Path({MOUNT_PATH!r})
stage1_path = mount_path / {STAGE1_PATH!r}
stage2_path = mount_path / {STAGE2_PATH!r}
expected_stage1_len = {STAGE1_EXPECTED_BYTES}
expected_stage1_hash = {STAGE1_EXPECTED_SHA256!r}
expected_stage2 = base64.b64decode({encoded_stage2!r})

stage1_bytes = stage1_path.read_bytes()
stage1_hash = hashlib.sha256(stage1_bytes).hexdigest()
if len(stage1_bytes) != expected_stage1_len:
    raise SystemExit(f"Sandbox B Stage 1 byte count mismatch: {{len(stage1_bytes)}}")
if stage1_hash != expected_stage1_hash:
    raise SystemExit(f"Sandbox B Stage 1 SHA-256 mismatch: {{stage1_hash}}")

stage2_path.parent.mkdir(parents=True, exist_ok=True)
with stage2_path.open("wb") as handle:
    handle.write(expected_stage2)
    handle.flush()

stage2_readback = stage2_path.read_bytes()
if stage2_readback != expected_stage2:
    raise SystemExit("Sandbox B Stage 2 readback mismatch")

result = {{
    "stage1_bytes": len(stage1_bytes),
    "stage1_sha256": stage1_hash,
    "stage2_bytes": len(stage2_readback),
    "stage2_sha256": hashlib.sha256(stage2_readback).hexdigest(),
    "stage2_base64": base64.b64encode(stage2_readback).decode("ascii"),
}}
print(base64.b64encode(__import__("json").dumps(result, sort_keys=True).encode("utf-8")).decode("ascii"))
"""
    return "python - <<'PY'\n" + script.strip() + "\nPY\nsync\n"


def poll_external_stage2(
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
            observed = fs.read_file(STAGE2_PATH)
            observed_hash = sha256_hex(observed)
            logger.line(
                f"external Stage 2 read attempt {attempts}: elapsed={elapsed:.2f}s bytes={len(observed)} hash={observed_hash}"
            )
            if observed == expected_bytes and observed_hash == expected_hash:
                return observed, observed_hash, attempts, time.monotonic() - started
            last_error = "content/hash mismatch"
        except Exception as exc:
            last_error = f"{type(exc).__name__}: {exc}"
            logger.line(f"external Stage 2 read attempt {attempts}: elapsed={elapsed:.2f}s pending ({type(exc).__name__})")

        time.sleep(POLL_INTERVAL_SECONDS)

    raise RuntimeError(
        "external Filesystem.read_file() did not observe expected Stage 2 evidence "
        f"within {POLL_TIMEOUT_SECONDS:.0f}s; last result: {last_error}"
    )


def main() -> int:
    logger = OutputLogger(OUTPUT_FILE)
    sandbox_b = None
    try:
        repo_root = find_repo_root(Path(__file__).resolve())
        load_tensorlake_api_key(repo_root)

        sdk_version = importlib.metadata.version("tensorlake")
        stage2_bytes = canonical_stage2_bytes()
        stage2_expected_hash = sha256_hex(stage2_bytes)

        logger.line("Experiment 2: Replace the Compute")
        logger.line("=" * 41)
        logger.line(f"tensorlake sdk          : {sdk_version}")
        logger.line(f"experiment              : {EXPERIMENT_NAME}")
        logger.line("Experiment 1 Sandbox A : terminated (historical)")
        logger.line(f"cloud volume/filesystem : {FILESYSTEM_NAME}")
        logger.line(f"Stage 1 evidence path   : {STAGE1_PATH}")
        logger.line(f"Stage 2 evidence path   : {STAGE2_PATH}")
        logger.line(f"Stage 2 expected sha256 : {stage2_expected_hash}")
        logger.line("api key                 : configured (redacted)")
        logger.line()

        client = FilesystemClient()
        try:
            fs = client.get(FILESYSTEM_NAME)
        except FilesystemNotFoundError as exc:
            raise RuntimeError(
                f"Required filesystem {FILESYSTEM_NAME!r} is missing; Experiment 2 must not create it"
            ) from exc

        logger.line("Host-side Stage 1 precondition")
        stage1_host_bytes = fs.read_file(STAGE1_PATH)
        stage1_host_hash = sha256_hex(stage1_host_bytes)
        logger.line(f"host Stage 1 bytes      : {len(stage1_host_bytes)}")
        logger.line(f"host Stage 1 sha256     : {stage1_host_hash}")
        validate_stage1_bytes(stage1_host_bytes, "Host-side")
        logger.line("host Stage 1 check      : PASS")
        logger.line()

        logger.line("Creating new Sandbox B with the same writable Cloud Volume mount")
        sandbox_b = Sandbox.create(
            name=SANDBOX_B_NAME,
            file_systems=[
                FileSystemMount(
                    file_system_id=FILESYSTEM_NAME,
                    mount_path=MOUNT_PATH,
                    read_only=False,
                )
            ],
        )
        sandbox_b_id = getattr(sandbox_b, "sandbox_id", None) or getattr(sandbox_b, "id", None) or "unknown"
        logger.line(f"sandbox B name          : {SANDBOX_B_NAME}")
        logger.line(f"sandbox B id            : {sandbox_b_id}")
        logger.line(f"mount path              : {MOUNT_PATH}")
        logger.line()

        logger.line("Sandbox B validates Stage 1 and writes deterministic Stage 2")
        result = sandbox_b.run("sh", ["-lc", sandbox_b_command(stage2_bytes)])
        stdout = result.stdout or ""
        stderr = result.stderr or ""
        exit_code = getattr(result, "exit_code", None)
        logger.line(f"sandbox B exit code     : {exit_code}")
        if stderr.strip():
            logger.line(f"sandbox B stderr        : {stderr.strip()}")
        if exit_code not in (0, None):
            raise RuntimeError(f"Sandbox B command failed with exit code {exit_code}")

        try:
            sandbox_report = json.loads(base64.b64decode(stdout.strip(), validate=True).decode("utf-8"))
        except Exception as exc:
            raise RuntimeError("Sandbox B report was not valid base64-encoded JSON") from exc

        logger.line(f"sandbox B Stage 1 bytes : {sandbox_report['stage1_bytes']}")
        logger.line(f"sandbox B Stage 1 hash  : {sandbox_report['stage1_sha256']}")
        logger.line(f"sandbox B Stage 2 bytes : {sandbox_report['stage2_bytes']}")
        logger.line(f"sandbox B Stage 2 hash  : {sandbox_report['stage2_sha256']}")
        if sandbox_report["stage1_bytes"] != STAGE1_EXPECTED_BYTES:
            raise RuntimeError("Sandbox B Stage 1 byte count mismatch")
        if sandbox_report["stage1_sha256"] != STAGE1_EXPECTED_SHA256:
            raise RuntimeError("Sandbox B Stage 1 SHA-256 mismatch")
        if int(sandbox_report["stage2_bytes"]) != len(stage2_bytes):
            raise RuntimeError("Sandbox B Stage 2 byte count mismatch")
        if sandbox_report["stage2_sha256"] != stage2_expected_hash:
            raise RuntimeError("Sandbox B Stage 2 SHA-256 mismatch")
        sandbox_stage2_bytes = base64.b64decode(sandbox_report["stage2_base64"], validate=True)
        if sandbox_stage2_bytes != stage2_bytes:
            raise RuntimeError("Sandbox B Stage 2 bytes did not match host canonical bytes")
        logger.line("sandbox B Stage 1 check : PASS")
        logger.line("sandbox B Stage 2 write : PASS (local sanity check only)")
        logger.line()

        logger.line("Polling host-side Filesystem.read_file() for published Stage 2 state")
        observed_bytes, observed_hash, attempts, elapsed = poll_external_stage2(
            fs=fs,
            expected_bytes=stage2_bytes,
            expected_hash=stage2_expected_hash,
            logger=logger,
        )
        logger.line("external Stage 2 read   : PASS")
        logger.line(f"external Stage 2 bytes  : {len(observed_bytes)}")
        logger.line(f"external Stage 2 sha256 : {observed_hash}")
        logger.line(f"poll attempts           : {attempts}")
        logger.line(f"poll elapsed seconds    : {elapsed:.2f}")
        logger.line()

        run_result = {
            "experiment": EXPERIMENT_NAME,
            "status": "PASS",
            "sdk_version": sdk_version,
            "filesystem_name": FILESYSTEM_NAME,
            "mount_path": MOUNT_PATH,
            "stage1_path": STAGE1_PATH,
            "stage1_byte_count": len(stage1_host_bytes),
            "stage1_sha256": stage1_host_hash,
            "stage2_path": STAGE2_PATH,
            "stage2_byte_count": len(stage2_bytes),
            "stage2_expected_sha256": stage2_expected_hash,
            "stage2_observed_sha256": observed_hash,
            "poll_attempts": attempts,
            "poll_elapsed_seconds": round(elapsed, 3),
            "terminated_sandbox_b_id": sandbox_b_id,
            "terminated_sandbox_b_name": SANDBOX_B_NAME,
        }
        RESULT_FILE.write_text(json.dumps(run_result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        logger.line("PASS criteria")
        logger.line("  host Stage 1 precondition      : PASS")
        logger.line("  new Sandbox B created          : PASS")
        logger.line("  Sandbox B Stage 1 read         : PASS")
        logger.line("  Sandbox B Stage 2 write        : PASS")
        logger.line("  host Filesystem.read_file      : PASS")
        logger.line("  Stage 2 SHA-256 content match  : PASS")
        logger.line()
        logger.line("final result               : PASS")
        return 0
    finally:
        if sandbox_b is not None:
            logger.line()
            logger.line("Terminating Sandbox B")
            with contextlib.suppress(Exception):
                sandbox_b.terminate()
                logger.line("sandbox B termination  : requested")
        logger.close()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise
