"""Experiment 3: Version and Recover.

This experiment validates Cloud Volume versioned recovery:
known-good current state -> permanent snapshot -> deterministic unwanted
current-state modification -> historical read -> fork-based recovery.
"""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import sys
from pathlib import Path
from typing import Any

from tensorlake.filesystem import FilesystemClient, FilesystemNotFoundError


EXPERIMENT_NAME = "03-version-and-recover"
PRIMARY_FILESYSTEM_NAME = "article3-stateful-agent-workspace"
RECOVERY_FILESYSTEM_NAME = "article3-stateful-agent-recovered"
SNAPSHOT_MESSAGE = "experiment-03-known-good-before-mutation"
STAGE1_PATH = "state/stage1.json"
STAGE1_EXPECTED_SHA256 = "d557785c9e71629419e18b2e0f70eba9897dd84b9ede8979288b83929f7d3872"
STAGE2_PATH = "state/stage2.json"
STAGE2_KNOWN_GOOD_SHA256 = "f7a01912dc63453f1d8e4c06cf16b890f9819f38459c3670d16abacd051ff601"
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


def canonical_modified_stage2_bytes() -> bytes:
    payload = {
        "continued_from": STAGE1_PATH,
        "experiment": EXPERIMENT_NAME,
        "output_records": [
            "stage2-corrupted-output-001",
            "stage2-corrupted-output-002",
            "stage2-corrupted-output-003",
        ],
        "stage": 2,
        "status": "corrupted-test-state",
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"


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


def assert_recovery_filesystem_absent(client: FilesystemClient) -> None:
    try:
        client.get(RECOVERY_FILESYSTEM_NAME)
    except FilesystemNotFoundError:
        return
    raise RuntimeError(
        f"Recovery filesystem {RECOVERY_FILESYSTEM_NAME!r} already exists; "
        "not overwriting or deleting it automatically"
    )


def snapshot_to_dict(snapshot: Any) -> dict[str, Any]:
    return {
        "id": getattr(snapshot, "id", None),
        "message": getattr(snapshot, "message", None),
        "type": type(snapshot).__name__,
    }


def main() -> int:
    logger = OutputLogger(OUTPUT_FILE)
    try:
        repo_root = find_repo_root(Path(__file__).resolve())
        load_tensorlake_api_key(repo_root)

        sdk_version = importlib.metadata.version("tensorlake")
        modified_stage2_bytes = canonical_modified_stage2_bytes()
        modified_stage2_hash = sha256_hex(modified_stage2_bytes)

        logger.line("Experiment 3: Version and Recover")
        logger.line("=" * 41)
        logger.line(f"tensorlake sdk              : {sdk_version}")
        logger.line(f"experiment                  : {EXPERIMENT_NAME}")
        logger.line(f"primary filesystem          : {PRIMARY_FILESYSTEM_NAME}")
        logger.line(f"recovery filesystem         : {RECOVERY_FILESYSTEM_NAME}")
        logger.line(f"snapshot message            : {SNAPSHOT_MESSAGE}")
        logger.line(f"modified Stage 2 sha256     : {modified_stage2_hash}")
        logger.line("api key                     : configured (redacted)")
        logger.line()

        client = FilesystemClient()
        primary_fs = get_required_filesystem(client, PRIMARY_FILESYSTEM_NAME, "primary")
        assert_recovery_filesystem_absent(client)

        logger.line("Precondition: known-good state exists before mutation")
        stage1_bytes = primary_fs.read_file(STAGE1_PATH)
        stage2_known_good_bytes = primary_fs.read_file(STAGE2_PATH)
        stage1_hash = verify_hash(stage1_bytes, STAGE1_EXPECTED_SHA256, "Stage 1 precondition")
        stage2_known_good_hash = verify_hash(
            stage2_known_good_bytes,
            STAGE2_KNOWN_GOOD_SHA256,
            "Stage 2 known-good precondition",
        )
        logger.line(f"Stage 1 bytes               : {len(stage1_bytes)}")
        logger.line(f"Stage 1 sha256              : {stage1_hash}")
        logger.line(f"Stage 2 known-good bytes    : {len(stage2_known_good_bytes)}")
        logger.line(f"Stage 2 known-good sha256   : {stage2_known_good_hash}")
        logger.line("precondition                : PASS")
        logger.line()

        logger.line("Creating permanent known-good Cloud Volume snapshot")
        snapshot = primary_fs.snapshot(SNAPSHOT_MESSAGE)
        snapshot_id = getattr(snapshot, "id", None)
        if not snapshot_id:
            raise RuntimeError(f"Snapshot object did not expose a usable id: {snapshot!r}")
        logger.line(f"snapshot object type        : {type(snapshot).__name__}")
        logger.line(f"snapshot id                 : {snapshot_id}")
        logger.line(f"snapshot message            : {getattr(snapshot, 'message', '')}")
        logger.line()

        logger.line("Verifying snapshot appears in permanent snapshot list")
        snapshots = primary_fs.list_snapshots()
        matching_snapshot = next(
            (item for item in snapshots if getattr(item, "id", None) == snapshot_id),
            None,
        )
        if matching_snapshot is None:
            raise RuntimeError(f"Snapshot {snapshot_id!r} was not found in list_snapshots()")
        logger.line(f"snapshot list count         : {len(snapshots)}")
        logger.line(f"snapshot confirmed          : PASS")
        logger.line()

        logger.line("Writing deterministic unwanted current-state modification")
        version = primary_fs.write_file(
            STAGE2_PATH,
            modified_stage2_bytes,
            message="experiment-03-intentional-current-state-modification",
        )
        logger.line(f"write version object type   : {type(version).__name__}")
        logger.line(f"write version id            : {getattr(version, 'version_id', '')}")
        logger.line(f"write previous version id   : {getattr(version, 'previous_version_id', '')}")
        logger.line()

        logger.line("Verifying current head changed")
        current_stage2_bytes = primary_fs.read_file(STAGE2_PATH)
        current_stage2_hash = sha256_hex(current_stage2_bytes)
        if current_stage2_bytes != modified_stage2_bytes:
            raise RuntimeError("Current Stage 2 did not match deterministic modified bytes")
        if current_stage2_hash == STAGE2_KNOWN_GOOD_SHA256:
            raise RuntimeError("Current Stage 2 still matches known-good hash after mutation")
        logger.line(f"current Stage 2 bytes       : {len(current_stage2_bytes)}")
        logger.line(f"current Stage 2 sha256      : {current_stage2_hash}")
        logger.line("current head changed        : PASS")
        logger.line()

        logger.line("Reading known-good Stage 2 from permanent snapshot")
        historical_stage2_bytes = primary_fs.read_file(STAGE2_PATH, version=snapshot_id)
        historical_stage2_hash = verify_hash(
            historical_stage2_bytes,
            STAGE2_KNOWN_GOOD_SHA256,
            "Historical Stage 2",
        )
        logger.line(f"historical Stage 2 bytes    : {len(historical_stage2_bytes)}")
        logger.line(f"historical Stage 2 sha256   : {historical_stage2_hash}")
        logger.line("historical read             : PASS")
        logger.line()

        logger.line("Forking recovered filesystem from known-good snapshot")
        recovered_fs = client.fork(
            RECOVERY_FILESYSTEM_NAME,
            base_filesystem=PRIMARY_FILESYSTEM_NAME,
            snapshot=snapshot_id,
        )
        logger.line(f"recovered filesystem        : {RECOVERY_FILESYSTEM_NAME}")
        logger.line("fork-based recovery         : PASS")
        logger.line()

        logger.line("Verifying recovered filesystem contains known-good state")
        recovered_stage1_bytes = recovered_fs.read_file(STAGE1_PATH)
        recovered_stage2_bytes = recovered_fs.read_file(STAGE2_PATH)
        recovered_stage1_hash = verify_hash(
            recovered_stage1_bytes,
            STAGE1_EXPECTED_SHA256,
            "Recovered Stage 1",
        )
        recovered_stage2_hash = verify_hash(
            recovered_stage2_bytes,
            STAGE2_KNOWN_GOOD_SHA256,
            "Recovered Stage 2",
        )
        logger.line(f"recovered Stage 1 bytes     : {len(recovered_stage1_bytes)}")
        logger.line(f"recovered Stage 1 sha256    : {recovered_stage1_hash}")
        logger.line(f"recovered Stage 2 bytes     : {len(recovered_stage2_bytes)}")
        logger.line(f"recovered Stage 2 sha256    : {recovered_stage2_hash}")
        logger.line("recovered filesystem check  : PASS")
        logger.line()

        logger.line("Verifying primary remains modified and recovered remains known-good")
        final_primary_stage2_hash = sha256_hex(primary_fs.read_file(STAGE2_PATH))
        final_recovered_stage2_hash = sha256_hex(recovered_fs.read_file(STAGE2_PATH))
        if final_primary_stage2_hash != modified_stage2_hash:
            raise RuntimeError("Primary filesystem no longer contains the modified current Stage 2")
        if final_recovered_stage2_hash != STAGE2_KNOWN_GOOD_SHA256:
            raise RuntimeError("Recovered filesystem no longer contains known-good Stage 2")
        logger.line(f"primary current Stage 2     : {final_primary_stage2_hash}")
        logger.line(f"recovered Stage 2           : {final_recovered_stage2_hash}")
        logger.line("state separation            : PASS")
        logger.line()

        run_result = {
            "experiment": EXPERIMENT_NAME,
            "status": "PASS",
            "sdk_version": sdk_version,
            "primary_filesystem_name": PRIMARY_FILESYSTEM_NAME,
            "recovery_filesystem_name": RECOVERY_FILESYSTEM_NAME,
            "snapshot": snapshot_to_dict(snapshot),
            "stage1_path": STAGE1_PATH,
            "stage1_sha256": stage1_hash,
            "stage2_path": STAGE2_PATH,
            "stage2_known_good_sha256": stage2_known_good_hash,
            "stage2_modified_sha256": modified_stage2_hash,
            "historical_stage2_sha256": historical_stage2_hash,
            "recovered_stage1_sha256": recovered_stage1_hash,
            "recovered_stage2_sha256": recovered_stage2_hash,
        }
        RESULT_FILE.write_text(json.dumps(run_result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        logger.line("PASS criteria")
        logger.line("  Stage 1 precondition matched          : PASS")
        logger.line("  Stage 2 known-good precondition       : PASS")
        logger.line("  permanent snapshot created            : PASS")
        logger.line("  snapshot confirmed via list           : PASS")
        logger.line("  primary Stage 2 changed               : PASS")
        logger.line("  current head differs from known-good  : PASS")
        logger.line("  historical snapshot read              : PASS")
        logger.line("  fork from known-good snapshot         : PASS")
        logger.line("  recovered Stage 2 known-good          : PASS")
        logger.line("  recovered Stage 1 known-good          : PASS")
        logger.line("  primary remains modified              : PASS")
        logger.line("  recovered remains known-good          : PASS")
        logger.line()
        logger.line("final result                     : PASS")
        return 0
    finally:
        logger.close()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise
