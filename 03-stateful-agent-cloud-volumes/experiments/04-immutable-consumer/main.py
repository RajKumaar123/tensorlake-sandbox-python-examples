"""Experiment 4: Immutable Consumer.

This experiment validates snapshot-pinned read-only consumption of a known-good
Cloud Volume state from a new Sandbox C.
"""

from __future__ import annotations

import base64
import contextlib
import hashlib
import importlib.metadata
import json
import os
import sys
from pathlib import Path
from typing import Any

from tensorlake.filesystem import FileNotFoundInFilesystemError, FilesystemClient, FilesystemNotFoundError
from tensorlake.sandbox import FileSystemMount, Sandbox


EXPERIMENT_NAME = "04-immutable-consumer"
PRIMARY_FILESYSTEM_NAME = "article3-stateful-agent-workspace"
RECOVERY_FILESYSTEM_NAME = "article3-stateful-agent-recovered"
SNAPSHOT_ID = "b1cd0a588a1ab3c271ae0ea8c596b2968b07f7f463c70cd62644c2c4ccc46869"
SANDBOX_C_NAME = "article3-immutable-consumer-sandbox-c"
MOUNT_PATH = "/workspace"
STAGE1_PATH = "state/stage1.json"
STAGE1_KNOWN_GOOD_SHA256 = "d557785c9e71629419e18b2e0f70eba9897dd84b9ede8979288b83929f7d3872"
STAGE2_PATH = "state/stage2.json"
STAGE2_KNOWN_GOOD_SHA256 = "f7a01912dc63453f1d8e4c06cf16b890f9819f38459c3670d16abacd051ff601"
PRIMARY_CURRENT_STAGE2_SHA256 = "1676930860ab4e1b5cad4db2289e88c9aa8852ca17ce8a3858d10bf0bbf4cec7"
PROHIBITED_PATH = "state/should-not-write.txt"
OUTPUT_FILE = Path(__file__).with_name("output.txt")
RESULT_FILE = Path(__file__).with_name("result.json")


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


def verify_hash(data: bytes, expected_hash: str, label: str) -> str:
    observed_hash = sha256_hex(data)
    if observed_hash != expected_hash:
        raise RuntimeError(f"{label} SHA-256 mismatch: {observed_hash}")
    return observed_hash


def get_required_filesystem(client: FilesystemClient, name: str, label: str) -> Any:
    try:
        return client.get(name)
    except FilesystemNotFoundError as exc:
        raise RuntimeError(f"Required {label} filesystem {name!r} was not found") from exc


def sandbox_c_validation_command() -> str:
    script = f"""
import base64
import errno
import hashlib
import json
import pathlib
import traceback

mount_path = pathlib.Path({MOUNT_PATH!r})
stage1_path = mount_path / {STAGE1_PATH!r}
stage2_path = mount_path / {STAGE2_PATH!r}
prohibited_path = mount_path / {PROHIBITED_PATH!r}

stage1_bytes = stage1_path.read_bytes()
stage2_bytes = stage2_path.read_bytes()
stage1_hash = hashlib.sha256(stage1_bytes).hexdigest()
stage2_hash = hashlib.sha256(stage2_bytes).hexdigest()

write_failed = False
write_error_type = ""
write_error_message = ""
write_error_errno = None
try:
    prohibited_path.write_text("this write should fail\\n", encoding="utf-8")
except OSError as exc:
    write_failed = True
    write_error_type = type(exc).__name__
    write_error_message = str(exc)
    write_error_errno = exc.errno
except Exception as exc:
    write_failed = True
    write_error_type = type(exc).__name__
    write_error_message = "".join(traceback.format_exception_only(type(exc), exc)).strip()

prohibited_exists = prohibited_path.exists()
result = {{
    "stage1_bytes": len(stage1_bytes),
    "stage1_sha256": stage1_hash,
    "stage2_bytes": len(stage2_bytes),
    "stage2_sha256": stage2_hash,
    "stage2_equals_current_primary": stage2_hash == {PRIMARY_CURRENT_STAGE2_SHA256!r},
    "write_failed": write_failed,
    "write_error_type": write_error_type,
    "write_error_message": write_error_message,
    "write_error_errno": write_error_errno,
    "write_error_is_erofs": write_error_errno == errno.EROFS,
    "prohibited_exists": prohibited_exists,
    "stage1_base64": base64.b64encode(stage1_bytes).decode("ascii"),
    "stage2_base64": base64.b64encode(stage2_bytes).decode("ascii"),
}}
print(base64.b64encode(json.dumps(result, sort_keys=True).encode("utf-8")).decode("ascii"))
"""
    return "python - <<'PY'\n" + script.strip() + "\nPY\n"


def mount_to_dict(mount: Any) -> dict[str, Any]:
    return {
        "file_system_id": getattr(mount, "file_system_id", None),
        "mount_path": getattr(mount, "mount_path", None),
        "read_only": getattr(mount, "read_only", None),
        "prefetch": getattr(mount, "prefetch", None),
        "snapshot_id": getattr(mount, "snapshot_id", None),
        "owner": getattr(mount, "owner", None),
        "type": type(mount).__name__,
    }


def main() -> int:
    logger = OutputLogger(OUTPUT_FILE)
    sandbox_c = None
    try:
        repo_root = find_repo_root(Path(__file__).resolve())
        load_tensorlake_api_key(repo_root)

        sdk_version = importlib.metadata.version("tensorlake")

        logger.line("Experiment 4: Immutable Consumer")
        logger.line("=" * 40)
        logger.line(f"tensorlake sdk              : {sdk_version}")
        logger.line(f"experiment                  : {EXPERIMENT_NAME}")
        logger.line(f"primary filesystem          : {PRIMARY_FILESYSTEM_NAME}")
        logger.line(f"recovered filesystem        : {RECOVERY_FILESYSTEM_NAME}")
        logger.line(f"pinned snapshot id          : {SNAPSHOT_ID}")
        logger.line(f"sandbox C name              : {SANDBOX_C_NAME}")
        logger.line("api key                     : configured (redacted)")
        logger.line()

        client = FilesystemClient()
        primary_fs = get_required_filesystem(client, PRIMARY_FILESYSTEM_NAME, "primary")

        logger.line("Host-side preconditions")
        primary_current_stage2 = primary_fs.read_file(STAGE2_PATH)
        primary_current_stage2_hash = verify_hash(
            primary_current_stage2,
            PRIMARY_CURRENT_STAGE2_SHA256,
            "Primary current Stage 2",
        )
        snapshots = primary_fs.list_snapshots()
        matching_snapshot = next(
            (item for item in snapshots if getattr(item, "id", None) == SNAPSHOT_ID),
            None,
        )
        if matching_snapshot is None:
            raise RuntimeError(f"Required permanent snapshot {SNAPSHOT_ID!r} was not found")
        historical_stage2 = primary_fs.read_file(STAGE2_PATH, version=SNAPSHOT_ID)
        historical_stage2_hash = verify_hash(
            historical_stage2,
            STAGE2_KNOWN_GOOD_SHA256,
            "Historical Stage 2 snapshot sanity check",
        )
        logger.line(f"primary current Stage 2     : {primary_current_stage2_hash}")
        logger.line(f"snapshot list count         : {len(snapshots)}")
        logger.line("snapshot present            : PASS")
        logger.line(f"snapshot Stage 2 sanity     : {historical_stage2_hash}")
        logger.line("host preconditions          : PASS")
        logger.line()

        mount_config = FileSystemMount(
            file_system_id=PRIMARY_FILESYSTEM_NAME,
            mount_path=MOUNT_PATH,
            read_only=True,
            snapshot_id=SNAPSHOT_ID,
        )
        logger.line("Creating Sandbox C with snapshot-pinned read-only mount")
        sandbox_c = Sandbox.create(
            name=SANDBOX_C_NAME,
            file_systems=[mount_config],
        )
        sandbox_c_id = getattr(sandbox_c, "sandbox_id", None) or getattr(sandbox_c, "id", None) or "unknown"
        logger.line(f"sandbox C id                : {sandbox_c_id}")
        logger.line(f"mount file_system_id        : {PRIMARY_FILESYSTEM_NAME}")
        logger.line(f"mount path                  : {MOUNT_PATH}")
        logger.line("mount read_only             : True")
        logger.line(f"mount snapshot_id           : {SNAPSHOT_ID}")
        logger.line()

        logger.line("Inspecting Sandbox C mount configuration")
        listed_mounts = sandbox_c.list_file_systems()
        mount_dicts = [mount_to_dict(mount) for mount in listed_mounts]
        logger.line(f"listed mount count          : {len(mount_dicts)}")
        matching_mount = next(
            (mount for mount in mount_dicts if mount.get("mount_path") == MOUNT_PATH),
            None,
        )
        if matching_mount is None:
            raise RuntimeError(f"Sandbox C did not list expected mount path {MOUNT_PATH!r}")
        logger.line(f"listed mount file_system_id : {matching_mount.get('file_system_id')}")
        logger.line(f"listed mount read_only      : {matching_mount.get('read_only')}")
        logger.line(f"listed mount snapshot_id    : {matching_mount.get('snapshot_id')}")
        if matching_mount.get("read_only") is not True:
            raise RuntimeError("Sandbox C mount is not listed as read_only=True")
        if matching_mount.get("snapshot_id") != SNAPSHOT_ID:
            raise RuntimeError("Sandbox C mount snapshot_id does not match expected snapshot")
        logger.line("mount configuration         : PASS")
        logger.line()

        logger.line("Sandbox C reads pinned known-good historical state and attempts mutation")
        result = sandbox_c.run("sh", ["-lc", sandbox_c_validation_command()])
        stdout = result.stdout or ""
        stderr = result.stderr or ""
        exit_code = getattr(result, "exit_code", None)
        logger.line(f"sandbox C exit code         : {exit_code}")
        if stderr.strip():
            logger.line(f"sandbox C stderr            : {stderr.strip()}")
        if exit_code not in (0, None):
            raise RuntimeError(f"Sandbox C validation command failed with exit code {exit_code}")

        try:
            sandbox_report = json.loads(base64.b64decode(stdout.strip(), validate=True).decode("utf-8"))
        except Exception as exc:
            raise RuntimeError("Sandbox C report was not valid base64-encoded JSON") from exc

        logger.line(f"sandbox C Stage 1 bytes     : {sandbox_report['stage1_bytes']}")
        logger.line(f"sandbox C Stage 1 sha256    : {sandbox_report['stage1_sha256']}")
        logger.line(f"sandbox C Stage 2 bytes     : {sandbox_report['stage2_bytes']}")
        logger.line(f"sandbox C Stage 2 sha256    : {sandbox_report['stage2_sha256']}")
        logger.line(f"Stage 2 equals current head : {sandbox_report['stage2_equals_current_primary']}")
        logger.line(f"write failed                : {sandbox_report['write_failed']}")
        logger.line(f"write error type            : {sandbox_report['write_error_type']}")
        logger.line(f"write error errno           : {sandbox_report['write_error_errno']}")
        logger.line(f"write error is EROFS        : {sandbox_report['write_error_is_erofs']}")
        logger.line(f"prohibited file exists      : {sandbox_report['prohibited_exists']}")

        if int(sandbox_report["stage1_bytes"]) != len(base64.b64decode(sandbox_report["stage1_base64"])):
            raise RuntimeError("Sandbox C Stage 1 byte count did not match returned bytes")
        if int(sandbox_report["stage2_bytes"]) != len(base64.b64decode(sandbox_report["stage2_base64"])):
            raise RuntimeError("Sandbox C Stage 2 byte count did not match returned bytes")
        if sandbox_report["stage1_sha256"] != STAGE1_KNOWN_GOOD_SHA256:
            raise RuntimeError("Sandbox C Stage 1 did not match known-good snapshot hash")
        if sandbox_report["stage2_sha256"] != STAGE2_KNOWN_GOOD_SHA256:
            raise RuntimeError("Sandbox C Stage 2 did not match known-good snapshot hash")
        if sandbox_report["stage2_sha256"] == PRIMARY_CURRENT_STAGE2_SHA256:
            raise RuntimeError("Sandbox C Stage 2 unexpectedly matched current primary modified state")
        if not sandbox_report["write_failed"]:
            raise RuntimeError("Write through snapshot-pinned read-only mount unexpectedly succeeded")
        if sandbox_report["prohibited_exists"]:
            raise RuntimeError("Prohibited file exists after failed write attempt")
        logger.line("sandbox C content check     : PASS")
        logger.line("read-only mutation check    : PASS")
        logger.line()

        logger.line("Verifying current primary filesystem was not modified by Experiment 4")
        final_primary_stage2_hash = verify_hash(
            primary_fs.read_file(STAGE2_PATH),
            PRIMARY_CURRENT_STAGE2_SHA256,
            "Final primary current Stage 2",
        )
        try:
            primary_fs.read_file(PROHIBITED_PATH)
            raise RuntimeError(f"Prohibited file {PROHIBITED_PATH!r} exists in primary filesystem")
        except FileNotFoundInFilesystemError:
            prohibited_primary_status = "absent"
        logger.line(f"primary current Stage 2     : {final_primary_stage2_hash}")
        logger.line(f"primary prohibited file     : {prohibited_primary_status}")
        logger.line("no-write verification       : PASS")
        logger.line()

        run_result = {
            "experiment": EXPERIMENT_NAME,
            "status": "PASS",
            "sdk_version": sdk_version,
            "primary_filesystem": PRIMARY_FILESYSTEM_NAME,
            "recovery_filesystem": RECOVERY_FILESYSTEM_NAME,
            "snapshot_id": SNAPSHOT_ID,
            "sandbox_c_name": SANDBOX_C_NAME,
            "terminated_sandbox_c_id": sandbox_c_id,
            "mount_path": MOUNT_PATH,
            "mount_read_only": True,
            "mount_snapshot_id": SNAPSHOT_ID,
            "stage1_path": STAGE1_PATH,
            "stage1_known_good_sha256": STAGE1_KNOWN_GOOD_SHA256,
            "sandbox_c_stage1_sha256": sandbox_report["stage1_sha256"],
            "stage2_path": STAGE2_PATH,
            "stage2_known_good_sha256": STAGE2_KNOWN_GOOD_SHA256,
            "sandbox_c_stage2_sha256": sandbox_report["stage2_sha256"],
            "primary_current_stage2_sha256": final_primary_stage2_hash,
            "mutation_attempt_status": "blocked",
            "mutation_error_type": sandbox_report["write_error_type"],
            "mutation_error_errno": sandbox_report["write_error_errno"],
            "mutation_error_is_erofs": sandbox_report["write_error_is_erofs"],
            "prohibited_path": PROHIBITED_PATH,
            "prohibited_path_status": prohibited_primary_status,
        }
        RESULT_FILE.write_text(json.dumps(run_result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        logger.line("PASS criteria")
        logger.line("  primary current Stage 2 modified    : PASS")
        logger.line("  permanent snapshot exists           : PASS")
        logger.line("  new Sandbox C created               : PASS")
        logger.line("  pinned read-only mount succeeds     : PASS")
        logger.line("  Sandbox C Stage 1 known-good        : PASS")
        logger.line("  Sandbox C Stage 2 known-good        : PASS")
        logger.line("  Sandbox C differs from current head : PASS")
        logger.line("  write through mount fails           : PASS")
        logger.line("  prohibited file absent              : PASS")
        logger.line()
        logger.line("final result                    : PASS")
        return 0
    finally:
        if sandbox_c is not None:
            logger.line()
            logger.line("Terminating Sandbox C")
            with contextlib.suppress(Exception):
                sandbox_c.terminate()
                logger.line("sandbox C termination      : requested")
        logger.close()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise
