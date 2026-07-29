"""
Suspend and resume a TensorLake sandbox while preserving state.

This example demonstrates how sandbox state survives suspension and
remains available after the sandbox is resumed.
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
SANDBOX_NAME = "tensorlake-example-07-suspend-resume"

STATE_FILE = "/tmp/state.txt"
STATE_MESSAGE = "Suspend and Resume works!"


def main() -> None:
    """Suspend and resume a TensorLake sandbox while preserving state."""

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

        status = getattr(status, "value", getattr(status, "name", status))

        # Display sandbox metadata.
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
        log("Step 1: Creating state...")

        create_result = sandbox.run(
            command="sh",
            args=[
                "-c",
                f"echo '{STATE_MESSAGE}' > {STATE_FILE}",
            ],
        )

        log(f"Exit Code : {create_result.exit_code}")
        log(f"STDOUT    : {create_result.stdout.strip() or '<empty>'}")
        log(f"STDERR    : {create_result.stderr.strip() or '<empty>'}")

        #
        # Step 2
        #

        log()
        log("Step 2: Suspending sandbox...")

        sandbox.suspend()

        log("Sandbox suspended successfully.")

        #
        # Step 3
        #

        log()
        log("Step 3: Resuming sandbox...")

        sandbox.resume()

        log("Sandbox resumed successfully.")

        #
        # Step 4
        #

        log()
        log("Step 4: Verifying state...")

        verify_result = sandbox.run(
            command="cat",
            args=[STATE_FILE],
        )

        log(f"Exit Code : {verify_result.exit_code}")
        log(f"STDOUT    : {verify_result.stdout.strip() or '<empty>'}")
        log(f"STDERR    : {verify_result.stderr.strip() or '<empty>'}")

        #
        # Step 5
        #

        log()
        log("State verification completed successfully.")

    except Exception as exc:
        log(f"Failed to demonstrate suspend/resume: {exc}")
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