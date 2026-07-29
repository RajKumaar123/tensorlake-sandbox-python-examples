"""
Use TensorLake's native file APIs to write, read, list, and delete a file.

This example demonstrates how to manage files inside a TensorLake sandbox
using the SDK's native file APIs without relying on shell commands.
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
SANDBOX_NAME = "tensorlake-example-05-native-file-api"

FILE_PATH = "/tmp/native_example.txt"
FILE_CONTENT = b"Hello from TensorLake Native File API!"


def format_directory_listing(listing) -> str:
    """Format directory entries into a readable text block."""
    lines = [f"Path : {listing.path}"]

    if not listing.entries:
        lines.append("<empty>")
        return "\n".join(lines)

    for entry in listing.entries:
        entry_type = "Directory" if entry.is_dir else "File"
        lines.append(f"- {entry.name} ({entry_type})")

    return "\n".join(lines)


def main() -> None:
    """Demonstrate the TensorLake Native File API."""

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
        # Provision a new sandbox.
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
        log("Step 1: Writing a file...")

        write_result = sandbox.write_file(
            path=FILE_PATH,
            content=FILE_CONTENT,
        )

        log(f"Trace ID : {write_result.trace_id}")
        log(f"Result   : {write_result.value}")

        #
        # Step 2
        #

        log()
        log("Step 2: Reading the file...")

        read_result = sandbox.read_file(path=FILE_PATH)

        log(f"Trace ID : {read_result.trace_id}")
        log(f"Content  : {read_result.value.decode()}")

        #
        # Step 3
        #

        log()
        log("Step 3: Listing the directory...")

        list_result = sandbox.list_directory(path="/tmp")

        log(f"Trace ID : {list_result.trace_id}")
        log()

        log("Directory Contents")
        log("-" * 40)
        log(format_directory_listing(list_result.value))

        #
        # Step 4
        #

        log()
        log("Step 4: Deleting the file...")

        delete_result = sandbox.delete_file(path=FILE_PATH)

        log(f"Trace ID : {delete_result.trace_id}")
        log(f"Result   : {delete_result.value}")

        #
        # Step 5
        #

        log()
        log("Step 5: Verifying deletion...")

        verify_result = sandbox.list_directory(path="/tmp")

        log("Directory Contents")
        log("-" * 40)
        log(format_directory_listing(verify_result.value))

    except Exception as exc:
        log(f"Failed to demonstrate the Native File API: {exc}")
        raise

    finally:
        # Always terminate the sandbox after the demonstration.
        if sandbox is not None:
            log()
            log("Cleaning up sandbox...")
            sandbox.terminate()
            log("Sandbox terminated successfully.")

        # Save the console output to output.txt.
        logger.save()


if __name__ == "__main__":
    main()