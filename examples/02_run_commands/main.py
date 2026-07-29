"""
Run a command inside a TensorLake sandbox and display the command result.

This example demonstrates how to execute a command inside a TensorLake
sandbox and inspect the execution result, including stdout, stderr,
exit code, and trace ID.
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
SANDBOX_NAME = "tensorlake-example-02-run-commands"


def main() -> None:
    """Create a sandbox, execute a command, and display the result."""

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

    # Keep a reference to the sandbox so it can always
    # be cleaned up in the finally block.
    sandbox = None

    try:
        # Provision a new TensorLake sandbox.
        sandbox = Sandbox.create(
            api_key=api_key,
            name=SANDBOX_NAME,
        )

        log("Sandbox created successfully.")
        log()

        # Retrieve the current sandbox status.
        status = sandbox.status
        if callable(status):
            status = status()

        # Convert the SDK status object into a readable value.
        status = getattr(status, "value", getattr(status, "name", status))

        # Display sandbox metadata.
        log("Sandbox Details")
        log("-" * 40)
        log(f"Sandbox ID     : {sandbox.sandbox_id}")
        log(f"Sandbox Name   : {sandbox.name}")
        log(f"Sandbox Status : {status}")
        log("-" * 40)

        log()
        log("Executing command...")

        # Execute a command inside the sandbox.
        result = sandbox.run(
            command="python",
            args=["--version"],
        )

        # Display the command execution details.
        log()
        log("Command Result")
        log("-" * 40)
        log(f"Trace ID  : {result.trace_id}")
        log(f"Exit Code : {result.exit_code}")
        log()

        log("STDOUT")
        log(result.stdout.strip() or "<empty>")
        log()

        log("STDERR")
        log(result.stderr.strip() or "<empty>")
        log("-" * 40)

    except Exception as exc:
        log(f"Failed to execute command: {exc}")
        raise

    finally:
        # Always terminate the sandbox to avoid leaving
        # temporary resources running.
        if sandbox is not None:
            log()
            log("Cleaning up sandbox...")
            sandbox.terminate()
            log("Sandbox terminated successfully.")

        # Save the console output to output.txt.
        logger.save()


if __name__ == "__main__":
    main()