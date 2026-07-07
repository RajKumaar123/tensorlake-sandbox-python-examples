"""
Install pandas inside a Tensorlake sandbox and verify the installation.

This example demonstrates the package-installation workflow and cleans up the
temporary sandbox after the commands complete.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.common import (
    cleanup_sandbox,
    create_sandbox,
    format_output,
    load_api_key,
    print_section,
)


def main() -> None:
    """Create a sandbox, install pandas, verify it, and clean up."""
    print("Creating Tensorlake sandbox...")

    sandbox = None
    try:
        api_key = load_api_key()
        sandbox = create_sandbox(api_key)
        print(f"Sandbox ID : {sandbox.sandbox_id}")
        print(f"Status     : {sandbox.status}")

        print_section("Installing pandas...")
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
        print(f"Exit Code : {install_result.exit_code}")
        print(f"STDOUT    : {format_output(repr(install_result.stdout))}")
        print(f"STDERR    : {format_output(repr(install_result.stderr))}")

        print_section("Verifying pandas...")
        verify_result = sandbox.run(
            command="python",
            args=[
                "-c",
                "import pandas as pd; print(pd.__version__)",
            ],
        )
        print(f"Exit Code : {verify_result.exit_code}")
        print(f"STDOUT    : {format_output(repr(verify_result.stdout))}")
        print(f"STDERR    : {format_output(repr(verify_result.stderr))}")
    except ValueError as exc:
        print(f"Configuration error: {exc}")
        raise SystemExit(1) from exc
    except Exception as exc:
        print(f"Failed to complete example: {exc}")
        raise SystemExit(1) from exc
    finally:
        # Temporary sandboxes should be cleaned up after the example runs.
        print()
        print("Terminating sandbox...")
        cleanup_sandbox(sandbox)


if __name__ == "__main__":
    main()
