"""
Create a snapshot from a Tensorlake sandbox and inspect it.

This example demonstrates snapshot creation, listing, retrieval, and cleanup.
The sandbox is intentionally kept alive because the snapshot lifecycle is the
focus of the example and the snapshot must exist long enough to inspect it.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.common import cleanup_sandbox, create_sandbox, load_api_key, print_section


def describe_snapshot(snapshot: Any) -> None:
    """Print the snapshot metadata in a readable format."""
    print(f"Snapshot ID : {getattr(snapshot, 'snapshot_id', 'N/A')}")
    print(f"Name        : {getattr(snapshot, 'name', 'N/A')}")
    print(f"Status      : {getattr(snapshot, 'status', 'N/A')}")


def main() -> None:
    """Create a sandbox, checkpoint it, and inspect the snapshot metadata."""
    print("Creating Tensorlake sandbox...")

    try:
        api_key = load_api_key()
        sandbox = create_sandbox(api_key)
    except ValueError as exc:
        print(f"Configuration error: {exc}")
        raise SystemExit(1) from exc
    except Exception as exc:
        print(f"Failed to create sandbox: {exc}")
        raise SystemExit(1) from exc

    print(f"Sandbox ID : {sandbox.sandbox_id}")
    print(f"Status     : {sandbox.status}")

    print_section("Creating snapshot...")
    snapshot = sandbox.checkpoint()
    if snapshot is None:
        raise SystemExit("Snapshot creation did not return snapshot metadata.")

    describe_snapshot(snapshot)

    print_section("Listing snapshots...")
    snapshots = list(sandbox.list_snapshots())
    for item in snapshots:
        print(f"- {getattr(item, 'snapshot_id', 'N/A')}")

    print_section("Fetching snapshot...")
    snapshot_id = getattr(snapshot, "snapshot_id", None)
    if not snapshot_id:
        raise SystemExit("Snapshot metadata did not include snapshot_id.")

    fetched_snapshot = sandbox.__class__.get_snapshot(snapshot_id, api_key=api_key)
    describe_snapshot(fetched_snapshot)

    print_section("Deleting snapshot...")
    sandbox.__class__.delete_snapshot(snapshot_id, api_key=api_key)
    print(f"Deleted snapshot {snapshot_id}")
    print()
    print("Terminating sandbox...")
    cleanup_sandbox(sandbox)

    # This example focuses on snapshot lifecycle behavior, so the sandbox is
    # kept alive until the snapshot workflow completes.


if __name__ == "__main__":
    main()
