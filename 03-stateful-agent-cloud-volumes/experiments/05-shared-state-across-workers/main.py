"""Experiment 5: Shared State Across Workers.

This experiment validates the recommended Cloud Volume concurrency pattern:
two independent sandboxes share one writable filesystem while each worker owns
and writes only its own path partition.
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

from tensorlake.filesystem import FileNotFoundInFilesystemError, FilesystemClient, FilesystemNotFoundError
from tensorlake.sandbox import FileSystemMount, Sandbox


EXPERIMENT_NAME = "05-shared-state-across-workers"
FILESYSTEM_NAME = "article3-stateful-agent-workspace"
SANDBOX_D_NAME = "article3-shared-state-worker-a"
SANDBOX_E_NAME = "article3-shared-state-worker-b"
MOUNT_PATH = "/workspace"
STAGE2_PATH = "state/stage2.json"
PRIMARY_CURRENT_STAGE2_SHA256 = "1676930860ab4e1b5cad4db2289e88c9aa8852ca17ce8a3858d10bf0bbf4cec7"
WORKER_A_PATH = "workers/worker-a/result.json"
WORKER_B_PATH = "workers/worker-b/result.json"
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


def canonical_worker_bytes(worker: str, owned_path: str, task: str, records: list[str]) -> bytes:
    payload = {
        "experiment": EXPERIMENT_NAME,
        "owned_path": owned_path,
        "records": records,
        "status": "completed",
        "task": task,
        "worker": worker,
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"


def get_required_filesystem(client: FilesystemClient) -> Any:
    try:
        return client.get(FILESYSTEM_NAME)
    except FilesystemNotFoundError as exc:
        raise RuntimeError(f"Required filesystem {FILESYSTEM_NAME!r} was not found") from exc


def assert_path_absent(fs: Any, path: str) -> None:
    try:
        fs.read_file(path)
    except FileNotFoundInFilesystemError:
        return
    raise RuntimeError(f"Experiment 5 target path already exists and will not be overwritten: {path}")


def verify_stage2_precondition(fs: Any) -> str:
    observed = fs.read_file(STAGE2_PATH)
    observed_hash = sha256_hex(observed)
    if observed_hash != PRIMARY_CURRENT_STAGE2_SHA256:
        raise RuntimeError(f"Primary Stage 2 precondition mismatch: {observed_hash}")
    return observed_hash


def mount_to_dict(mount: Any) -> dict[str, Any]:
    return {
        "file_system_id": getattr(mount, "file_system_id", None),
        "mount_path": getattr(mount, "mount_path", None),
        "read_only": getattr(mount, "read_only", None),
        "snapshot_id": getattr(mount, "snapshot_id", None),
        "type": type(mount).__name__,
    }


def verify_writable_mount(sandbox: Sandbox, label: str, logger: OutputLogger) -> dict[str, Any]:
    mounts = [mount_to_dict(mount) for mount in sandbox.list_file_systems()]
    matching = next((mount for mount in mounts if mount.get("mount_path") == MOUNT_PATH), None)
    if matching is None:
        raise RuntimeError(f"{label} did not list expected mount path {MOUNT_PATH!r}")
    if matching.get("file_system_id") != FILESYSTEM_NAME:
        raise RuntimeError(f"{label} mount filesystem mismatch: {matching}")
    if matching.get("read_only") is not False:
        raise RuntimeError(f"{label} mount is not listed as writable: {matching}")
    if matching.get("snapshot_id") is not None:
        raise RuntimeError(f"{label} mount unexpectedly has snapshot_id: {matching}")
    logger.line(f"{label} mount file_system_id : {matching.get('file_system_id')}")
    logger.line(f"{label} mount path           : {matching.get('mount_path')}")
    logger.line(f"{label} mount read_only      : {matching.get('read_only')}")
    logger.line(f"{label} mount snapshot_id    : {matching.get('snapshot_id')}")
    return matching


def worker_write_command(relative_path: str, expected_bytes: bytes) -> str:
    encoded_expected = base64.b64encode(expected_bytes).decode("ascii")
    script = f"""
import base64
import hashlib
import json
import pathlib

mount_path = pathlib.Path({MOUNT_PATH!r})
artifact_path = mount_path / {relative_path!r}
expected = base64.b64decode({encoded_expected!r})

artifact_path.parent.mkdir(parents=True, exist_ok=True)
with artifact_path.open("wb") as handle:
    handle.write(expected)
    handle.flush()

readback = artifact_path.read_bytes()
if readback != expected:
    raise SystemExit("worker local artifact readback mismatch")

report = {{
    "path": {relative_path!r},
    "bytes": len(readback),
    "sha256": hashlib.sha256(readback).hexdigest(),
    "artifact_base64": base64.b64encode(readback).decode("ascii"),
}}
print(base64.b64encode(json.dumps(report, sort_keys=True).encode("utf-8")).decode("ascii"))
"""
    return "python - <<'PY'\n" + script.strip() + "\nPY\nsync\n"


def peer_read_command(relative_path: str) -> str:
    script = f"""
import base64
import hashlib
import json
import pathlib

artifact_path = pathlib.Path({MOUNT_PATH!r}) / {relative_path!r}
data = artifact_path.read_bytes()
report = {{
    "path": {relative_path!r},
    "bytes": len(data),
    "sha256": hashlib.sha256(data).hexdigest(),
    "artifact_base64": base64.b64encode(data).decode("ascii"),
}}
print(base64.b64encode(json.dumps(report, sort_keys=True).encode("utf-8")).decode("ascii"))
"""
    return "python - <<'PY'\n" + script.strip() + "\nPY\n"


def decode_sandbox_report(stdout: str, label: str) -> dict[str, Any]:
    try:
        return json.loads(base64.b64decode(stdout.strip(), validate=True).decode("utf-8"))
    except Exception as exc:
        raise RuntimeError(f"{label} report was not valid base64-encoded JSON") from exc


def run_and_decode(sandbox: Sandbox, command: str, label: str, logger: OutputLogger) -> dict[str, Any]:
    result = sandbox.run("sh", ["-lc", command])
    stdout = result.stdout or ""
    stderr = result.stderr or ""
    exit_code = getattr(result, "exit_code", None)
    logger.line(f"{label} exit code        : {exit_code}")
    if stderr.strip():
        logger.line(f"{label} stderr           : {stderr.strip()}")
    if exit_code not in (0, None):
        raise RuntimeError(f"{label} command failed with exit code {exit_code}")
    return decode_sandbox_report(stdout, label)


def validate_report(report: dict[str, Any], expected_path: str, expected_bytes: bytes, expected_hash: str, label: str) -> None:
    observed_bytes = base64.b64decode(report["artifact_base64"], validate=True)
    if report["path"] != expected_path:
        raise RuntimeError(f"{label} path mismatch: {report['path']}")
    if int(report["bytes"]) != len(expected_bytes):
        raise RuntimeError(f"{label} byte count mismatch: {report['bytes']}")
    if report["sha256"] != expected_hash:
        raise RuntimeError(f"{label} SHA-256 mismatch: {report['sha256']}")
    if observed_bytes != expected_bytes:
        raise RuntimeError(f"{label} bytes did not match expected canonical bytes")


def poll_external_read(
    fs: Any,
    path: str,
    expected_bytes: bytes,
    expected_hash: str,
    logger: OutputLogger,
) -> tuple[bytes, str, int, float]:
    deadline = time.monotonic() + POLL_TIMEOUT_SECONDS
    attempts = 0
    started = time.monotonic()
    last_error = "none"

    while time.monotonic() < deadline:
        attempts += 1
        elapsed = time.monotonic() - started
        try:
            observed = fs.read_file(path)
            observed_hash = sha256_hex(observed)
            logger.line(
                f"external read {path} attempt {attempts}: elapsed={elapsed:.2f}s bytes={len(observed)} hash={observed_hash}"
            )
            if observed == expected_bytes and observed_hash == expected_hash:
                return observed, observed_hash, attempts, time.monotonic() - started
            last_error = "content/hash mismatch"
        except Exception as exc:
            last_error = f"{type(exc).__name__}: {exc}"
            logger.line(f"external read {path} attempt {attempts}: elapsed={elapsed:.2f}s pending ({type(exc).__name__})")
        time.sleep(POLL_INTERVAL_SECONDS)

    raise RuntimeError(
        f"external Filesystem.read_file() did not observe expected content at {path!r} "
        f"within {POLL_TIMEOUT_SECONDS:.0f}s; last result: {last_error}"
    )


def main() -> int:
    logger = OutputLogger(OUTPUT_FILE)
    sandbox_d = None
    sandbox_e = None
    try:
        repo_root = find_repo_root(Path(__file__).resolve())
        load_tensorlake_api_key(repo_root)

        sdk_version = importlib.metadata.version("tensorlake")
        worker_a_bytes = canonical_worker_bytes(
            worker="worker-a",
            owned_path="workers/worker-a",
            task="partition-a",
            records=["A001", "A002", "A003"],
        )
        worker_b_bytes = canonical_worker_bytes(
            worker="worker-b",
            owned_path="workers/worker-b",
            task="partition-b",
            records=["B001", "B002", "B003"],
        )
        worker_a_hash = sha256_hex(worker_a_bytes)
        worker_b_hash = sha256_hex(worker_b_bytes)

        logger.line("Experiment 5: Shared State Across Workers")
        logger.line("=" * 49)
        logger.line(f"tensorlake sdk              : {sdk_version}")
        logger.line(f"experiment                  : {EXPERIMENT_NAME}")
        logger.line(f"primary filesystem          : {FILESYSTEM_NAME}")
        logger.line(f"worker A path               : {WORKER_A_PATH}")
        logger.line(f"worker A expected sha256    : {worker_a_hash}")
        logger.line(f"worker B path               : {WORKER_B_PATH}")
        logger.line(f"worker B expected sha256    : {worker_b_hash}")
        logger.line("api key                     : configured (redacted)")
        logger.line()

        client = FilesystemClient()
        fs = get_required_filesystem(client)

        logger.line("Host-side preconditions")
        stage2_hash = verify_stage2_precondition(fs)
        assert_path_absent(fs, WORKER_A_PATH)
        assert_path_absent(fs, WORKER_B_PATH)
        logger.line(f"primary Stage 2 sha256      : {stage2_hash}")
        logger.line(f"Worker A target absent      : PASS")
        logger.line(f"Worker B target absent      : PASS")
        logger.line("host preconditions          : PASS")
        logger.line()

        mount_config = FileSystemMount(
            file_system_id=FILESYSTEM_NAME,
            mount_path=MOUNT_PATH,
            read_only=False,
        )

        logger.line("Creating Sandbox D and Sandbox E with same writable Cloud Volume")
        sandbox_d = Sandbox.create(name=SANDBOX_D_NAME, file_systems=[mount_config])
        sandbox_e = Sandbox.create(name=SANDBOX_E_NAME, file_systems=[mount_config])
        sandbox_d_id = getattr(sandbox_d, "sandbox_id", None) or getattr(sandbox_d, "id", None) or "unknown"
        sandbox_e_id = getattr(sandbox_e, "sandbox_id", None) or getattr(sandbox_e, "id", None) or "unknown"
        logger.line(f"sandbox D name              : {SANDBOX_D_NAME}")
        logger.line(f"sandbox D id                : {sandbox_d_id}")
        logger.line(f"sandbox E name              : {SANDBOX_E_NAME}")
        logger.line(f"sandbox E id                : {sandbox_e_id}")
        logger.line()

        logger.line("Verifying writable mounts")
        sandbox_d_mount = verify_writable_mount(sandbox_d, "Sandbox D", logger)
        sandbox_e_mount = verify_writable_mount(sandbox_e, "Sandbox E", logger)
        logger.line("mount configuration         : PASS")
        logger.line()

        logger.line("Worker A writes only its owned path")
        worker_a_report = run_and_decode(
            sandbox_d,
            worker_write_command(WORKER_A_PATH, worker_a_bytes),
            "Worker A",
            logger,
        )
        validate_report(worker_a_report, WORKER_A_PATH, worker_a_bytes, worker_a_hash, "Worker A local artifact")
        logger.line(f"Worker A bytes              : {worker_a_report['bytes']}")
        logger.line(f"Worker A sha256             : {worker_a_report['sha256']}")
        logger.line("Worker A local validation   : PASS")
        logger.line()

        logger.line("Worker B writes only its owned path")
        worker_b_report = run_and_decode(
            sandbox_e,
            worker_write_command(WORKER_B_PATH, worker_b_bytes),
            "Worker B",
            logger,
        )
        validate_report(worker_b_report, WORKER_B_PATH, worker_b_bytes, worker_b_hash, "Worker B local artifact")
        logger.line(f"Worker B bytes              : {worker_b_report['bytes']}")
        logger.line(f"Worker B sha256             : {worker_b_report['sha256']}")
        logger.line("Worker B local validation   : PASS")
        logger.line()

        logger.line("Polling host-side Filesystem.read_file() for both worker artifacts")
        _, external_a_hash, attempts_a, elapsed_a = poll_external_read(
            fs, WORKER_A_PATH, worker_a_bytes, worker_a_hash, logger
        )
        _, external_b_hash, attempts_b, elapsed_b = poll_external_read(
            fs, WORKER_B_PATH, worker_b_bytes, worker_b_hash, logger
        )
        logger.line("external Worker A read      : PASS")
        logger.line("external Worker B read      : PASS")
        logger.line(f"Worker A poll attempts      : {attempts_a}")
        logger.line(f"Worker A poll elapsed       : {elapsed_a:.2f}s")
        logger.line(f"Worker B poll attempts      : {attempts_b}")
        logger.line(f"Worker B poll elapsed       : {elapsed_b:.2f}s")
        logger.line()

        logger.line("Checking combined filesystem listing")
        with contextlib.suppress(Exception):
            worker_entries = fs.list_files("workers")
            entry_paths = [entry.path for entry in worker_entries]
            logger.line(f"workers/ listed entries     : {entry_paths}")
        logger.line()

        logger.line("Cross-worker visibility checks")
        peer_b_from_d = run_and_decode(
            sandbox_d,
            peer_read_command(WORKER_B_PATH),
            "Sandbox D reads Worker B",
            logger,
        )
        validate_report(peer_b_from_d, WORKER_B_PATH, worker_b_bytes, worker_b_hash, "Sandbox D peer read")
        peer_a_from_e = run_and_decode(
            sandbox_e,
            peer_read_command(WORKER_A_PATH),
            "Sandbox E reads Worker A",
            logger,
        )
        validate_report(peer_a_from_e, WORKER_A_PATH, worker_a_bytes, worker_a_hash, "Sandbox E peer read")
        logger.line("Sandbox D reads Worker B    : PASS")
        logger.line("Sandbox E reads Worker A    : PASS")
        logger.line()

        logger.line("Protecting previous Article 3 state")
        final_stage2_hash = verify_stage2_precondition(fs)
        logger.line(f"primary Stage 2 sha256      : {final_stage2_hash}")
        logger.line("previous state unchanged    : PASS")
        logger.line()

        run_result = {
            "experiment": EXPERIMENT_NAME,
            "status": "PASS",
            "sdk_version": sdk_version,
            "filesystem_name": FILESYSTEM_NAME,
            "mount_path": MOUNT_PATH,
            "sandbox_d_name": SANDBOX_D_NAME,
            "terminated_sandbox_d_id": sandbox_d_id,
            "sandbox_e_name": SANDBOX_E_NAME,
            "terminated_sandbox_e_id": sandbox_e_id,
            "sandbox_d_mount": sandbox_d_mount,
            "sandbox_e_mount": sandbox_e_mount,
            "stage2_path": STAGE2_PATH,
            "primary_stage2_sha256": final_stage2_hash,
            "worker_a_path": WORKER_A_PATH,
            "worker_a_byte_count": len(worker_a_bytes),
            "worker_a_expected_sha256": worker_a_hash,
            "worker_a_observed_sha256": external_a_hash,
            "worker_a_poll_attempts": attempts_a,
            "worker_a_poll_elapsed_seconds": round(elapsed_a, 3),
            "worker_b_path": WORKER_B_PATH,
            "worker_b_byte_count": len(worker_b_bytes),
            "worker_b_expected_sha256": worker_b_hash,
            "worker_b_observed_sha256": external_b_hash,
            "worker_b_poll_attempts": attempts_b,
            "worker_b_poll_elapsed_seconds": round(elapsed_b, 3),
            "cross_worker_visibility_status": "PASS",
            "previous_state_protection_status": "PASS",
        }
        RESULT_FILE.write_text(json.dumps(run_result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        logger.line("PASS criteria")
        logger.line("  primary Stage 2 precondition        : PASS")
        logger.line("  Worker A target absent              : PASS")
        logger.line("  Worker B target absent              : PASS")
        logger.line("  Sandbox D created                   : PASS")
        logger.line("  Sandbox E created                   : PASS")
        logger.line("  both writable mounts verified       : PASS")
        logger.line("  Worker A owned-path write           : PASS")
        logger.line("  Worker B owned-path write           : PASS")
        logger.line("  Worker A external read              : PASS")
        logger.line("  Worker B external read              : PASS")
        logger.line("  Sandbox D reads Worker B            : PASS")
        logger.line("  Sandbox E reads Worker A            : PASS")
        logger.line("  primary Stage 2 remains unchanged   : PASS")
        logger.line()
        logger.line("final result                    : PASS")
        return 0
    finally:
        if sandbox_e is not None:
            logger.line()
            logger.line("Terminating Sandbox E")
            with contextlib.suppress(Exception):
                sandbox_e.terminate()
                logger.line("sandbox E termination      : requested")
        if sandbox_d is not None:
            logger.line()
            logger.line("Terminating Sandbox D")
            with contextlib.suppress(Exception):
                sandbox_d.terminate()
                logger.line("sandbox D termination      : requested")
        logger.close()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise
