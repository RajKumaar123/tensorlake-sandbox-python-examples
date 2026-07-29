"""
Demonstrate filesystem persistence inside a TensorLake sandbox.

This example creates a file, reads it back, and lists the /tmp directory
to show that files persist across multiple commands executed within the
same sandbox session.
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
SANDBOX_NAME = "tensorlake-example-03-stateful-filesystem"


def main() -> None:
    """Create a sandbox and demonstrate filesystem persistence."""

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

        # Step 1: Create a file inside the sandbox.
        log()
        log("Step 1: Creating a file...")

        create_result = sandbox.run(
            command="sh",
            args=[
                "-c",
                "echo 'Hello TensorLake!' > /tmp/hello.txt",
            ],
        )

        log(f"Exit Code : {create_result.exit_code}")
        log(f"STDOUT    : {create_result.stdout.strip() or '<empty>'}")
        log(f"STDERR    : {create_result.stderr.strip() or '<empty>'}")

        # Step 2: Read the file created in the previous command.
        log()
        log("Step 2: Reading the file...")

        read_result = sandbox.run(
            command="cat",
            args=["/tmp/hello.txt"],
        )

        log(f"Exit Code : {read_result.exit_code}")
        log(f"STDOUT    : {read_result.stdout.strip() or '<empty>'}")
        log(f"STDERR    : {read_result.stderr.strip() or '<empty>'}")

        # Step 3: Verify that the file exists in the sandbox.
        log()
        log("Step 3: Listing the /tmp directory...")

        list_result = sandbox.run(
            command="ls",
            args=["-l", "/tmp"],
        )

        log(f"Exit Code : {list_result.exit_code}")
        log()

        log("Directory Contents")
        log("-" * 40)
        log(list_result.stdout.strip())

        if list_result.stderr.strip():
            log()
            log("STDERR")
            log("-" * 40)
            log(list_result.stderr.strip())

    except Exception as exc:
        log(f"Failed to demonstrate filesystem persistence: {exc}")
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