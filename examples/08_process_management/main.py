"""
Manage background processes inside a TensorLake sandbox.

This example demonstrates how to start, list, and terminate a managed
background process using the TensorLake Python SDK.
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
SANDBOX_NAME = "tensorlake-example-08-process-management"
PROCESS_NAME = "example-08-sleep"


def find_process(processes, process_name):
    """Return the managed process matching the requested name."""
    for process in processes:
        managed = getattr(process, "managed", None)

        if managed and getattr(managed, "name", None) == process_name:
            return process

    return None


def main() -> None:
    """Demonstrate process management inside a TensorLake sandbox."""

    # Initialize the logger. It prints to the console and
    # automatically creates/updates output.txt.
    logger = OutputLogger(__file__)
    log = logger.log

    log("Creating TensorLake sandbox...")

    # Load environment variables from the .env file.
    load_dotenv()

    # Read the TensorLake API key.
    api_key = os.getenv("TENSORLAKE_API_KEY")
    if not api_key:
        raise ValueError(
            "TENSORLAKE_API_KEY is missing. Add it to your .env file."
        )

    sandbox = None

    try:
        # Provision a new TensorLake sandbox.
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
        # Start a managed background process.
        #

        log()
        log("Starting background process...")

        start_result = sandbox.start_process(
            command="sh",
            args=["-c", "sleep 60"],
            name=PROCESS_NAME,
        )

        log(f"Trace ID : {start_result.trace_id}")
        log(f"PID      : {start_result.value.pid}")
        log(f"Status   : {start_result.value.status.value}")

        #
        # List running processes.
        #

        log()
        log("Listing processes...")

        processes = list(sandbox.list_processes())

        for process in processes:
            managed = getattr(process, "managed", None)

            managed_name = (
                getattr(managed, "name", "N/A")
                if managed
                else "N/A"
            )

            managed_status = (
                getattr(getattr(managed, "status", None), "value", "N/A")
                if managed
                else "N/A"
            )

            command = getattr(process, "command", "N/A")
            args = getattr(process, "args", [])

            status = getattr(process, "status", "N/A")
            status = getattr(status, "value", getattr(status, "name", status))

            log("-" * 40)
            log(f"PID            : {process.pid}")
            log(f"Command        : {command}")
            log(f"Arguments      : {args}")
            log(f"Status         : {status}")
            log(f"Managed Name   : {managed_name}")
            log(f"Managed Status : {managed_status}")

        #
        # Find the managed process.
        #

        process = find_process(processes, PROCESS_NAME)

        if process is None:
            raise RuntimeError(
                f"Unable to locate process '{PROCESS_NAME}'."
            )

        #
        # Kill the process.
        #

        log()
        log("Terminating process...")

        kill_result = sandbox.kill_process(process.pid)

        log(f"Trace ID : {kill_result.trace_id}")
        log(f"Result   : {kill_result.value}")

    except Exception as exc:
        log(f"Process management failed: {exc}")
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