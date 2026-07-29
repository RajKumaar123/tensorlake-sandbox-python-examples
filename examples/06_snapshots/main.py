"""
Create and manage a TensorLake sandbox snapshot.

This example demonstrates how to create a snapshot, list available
snapshots, retrieve snapshot metadata, delete the snapshot, and
clean up the sandbox.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from tensorlake.sandbox import Sandbox

# Add the project root to the Python path so shared utilities
# can be imported when running this example directly.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.output_logger import OutputLogger

# A descriptive name makes it easier to identify this sandbox
# in the TensorLake dashboard and logs.
SANDBOX_NAME = "tensorlake-example-06-snapshots"


def log_snapshot(log, snapshot) -> None:
    """Display snapshot metadata."""

    status = getattr(snapshot, "status", "N/A")
    status = getattr(status, "value", getattr(status, "name", status))

    log(f"Snapshot ID : {getattr(snapshot, 'snapshot_id', 'N/A')}")
    log(f"Name        : {getattr(snapshot, 'name', 'N/A')}")
    log(f"Status      : {status}")


def main() -> None:
    """Create, inspect, and delete a TensorLake snapshot."""

    logger = OutputLogger(__file__)
    log = logger.log

    log("Creating TensorLake sandbox...")

    load_dotenv()

    api_key = os.getenv("TENSORLAKE_API_KEY")
    if not api_key:
        raise ValueError(
            "TENSORLAKE_API_KEY is missing. Add it to your .env file."
        )

    sandbox = None

    try:
        #
        # Create sandbox
        #

        sandbox = Sandbox.create(
            api_key=api_key,
            name=SANDBOX_NAME,
        )

        log("Sandbox created successfully.")
        log()

        status = sandbox.status
        if callable(status):
            status = status()

        status = getattr(status, "value", getattr(status, "name", status))

        log("Sandbox Details")
        log("-" * 40)
        log(f"Sandbox ID     : {sandbox.sandbox_id}")
        log(f"Sandbox Name   : {sandbox.name}")
        log(f"Sandbox Status : {status}")
        log("-" * 40)

        #
        # Step 1
        #

        log()
        log("Step 1: Creating a snapshot...")

        snapshot = sandbox.checkpoint()

        if snapshot is None:
            raise RuntimeError("Snapshot creation failed.")

        log_snapshot(log, snapshot)

        snapshot_id = snapshot.snapshot_id

        #
        # Step 2
        #

        log()
        log("Step 2: Listing snapshots...")

        snapshots = list(sandbox.list_snapshots())

        log(f"Snapshots Found : {len(snapshots)}")

        for item in snapshots:
            log(f"- {item.snapshot_id}")

        #
        # Step 3
        #

        log()
        log("Step 3: Retrieving snapshot...")

        fetched_snapshot = Sandbox.get_snapshot(
            snapshot_id,
            api_key=api_key,
        )

        log_snapshot(log, fetched_snapshot)

        #
        # Step 4
        #

        log()
        log("Step 4: Deleting snapshot...")

        Sandbox.delete_snapshot(
            snapshot_id,
            api_key=api_key,
        )

        log("Snapshot deleted successfully.")

    except Exception as exc:
        log(f"Failed to manage snapshot: {exc}")
        raise

    finally:
        if sandbox is not None:
            log()
            log("Cleaning up sandbox...")
            sandbox.terminate()
            log("Sandbox terminated successfully.")

        logger.save()


if __name__ == "__main__":
    main()