"""
Run a command inside a Tensorlake sandbox and print the command result.

This example demonstrates the verified command execution pattern:
use a command and separate arguments, then inspect the result object.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.common import cleanup_sandbox, create_sandbox, load_api_key


def main() -> None:
    """Create a sandbox, run `python --version`, and print the result."""
    print("Creating Tensorlake sandbox...")

    sandbox = None
    try:
        api_key = load_api_key()
        sandbox = create_sandbox(api_key)
        print(f"Sandbox ID : {sandbox.sandbox_id}")
        print(f"Status     : {sandbox.status}")

        print()
        print("Executing command...")
        result = sandbox.run(command="python", args=["--version"])
    except ValueError as exc:
        print(f"Configuration error: {exc}")
        raise SystemExit(1) from exc
    except Exception as exc:
        print(f"Failed to execute example: {exc}")
        raise SystemExit(1) from exc

    print()
    print("Trace ID:")
    print(result.trace_id)
    print()
    print("Exit Code:")
    print(result.exit_code)
    print()
    print("STDOUT:")
    print(result.stdout)
    print()
    print("STDERR:")
    print(result.stderr)
    print()
    print("Terminating sandbox...")
    cleanup_sandbox(sandbox)

    # This example creates a temporary sandbox, so we clean it up after use.


if __name__ == "__main__":
    main()
