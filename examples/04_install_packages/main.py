"""
Install pandas inside a TensorLake sandbox and verify the installation.

This example demonstrates how to install a Python package inside a
TensorLake sandbox and verify that it is immediately available for use.
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
SANDBOX_NAME = "tensorlake-example-04-install-packages"


def main() -> None:
    """Create a sandbox, install pandas, verify the installation, and clean up."""

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
        log("Step 1: Installing pandas...")

        install_result = sandbox.run(
            command="python",
            args=[
                "-m",
                "pip",
                "install",
                "--break-system-packages",
                "pandas",
            ],
        )

        log(f"Exit Code : {install_result.exit_code}")

        if install_result.exit_code == 0:
            log("Package installed successfully.")
        else:
            log("Package installation failed.")

        if install_result.stderr.strip():
            log()
            log("STDERR")
            log("-" * 40)
            log(install_result.stderr.strip())

        #
        # Step 2
        #

        log()
        log("Step 2: Verifying pandas installation...")

        verify_result = sandbox.run(
            command="python",
            args=[
                "-c",
                "import pandas as pd; print(pd.__version__)",
            ],
        )

        log(f"Exit Code : {verify_result.exit_code}")
        log(f"Pandas Version : {verify_result.stdout.strip()}")

        if verify_result.stderr.strip():
            log()
            log("STDERR")
            log("-" * 40)
            log(verify_result.stderr.strip())

    except Exception as exc:
        log(f"Failed to install pandas: {exc}")
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