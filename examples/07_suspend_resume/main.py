"""
Suspend and resume a Tensorlake sandbox while preserving state.

This example demonstrates that sandbox state survives suspension and is still
available after the sandbox is resumed.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.common import cleanup_sandbox, create_sandbox, load_api_key, print_section


def run_command(sandbox: Any, command: str, args: list[str]) -> Any:
    """Run a command in the sandbox and return the traced result."""
    return sandbox.run(command=command, args=args)


def main() -> None:
    """Create a sandbox, suspend it, resume it, and verify state survives."""
    print("Creating Tensorlake sandbox...")

    sandbox = None
    try:
        api_key = load_api_key()
        sandbox = create_sandbox(api_key, name="example-07-suspend-resume")
        print(f"Sandbox ID : {sandbox.sandbox_id}")
        print(f"Status     : {sandbox.status}")

        print_section("Creating state...")
        create_result = run_command(
            sandbox,
            command="sh",
            args=["-c", "echo 'suspend-resume works' > /tmp/state.txt"],
        )
        print(f"Exit Code : {create_result.exit_code}")
        print(f"STDOUT    : {create_result.stdout!r}")
        print(f"STDERR    : {create_result.stderr!r}")

        print_section("Suspending sandbox...")
        sandbox.suspend()
        print("Sandbox suspended successfully.")

        print_section("Resuming sandbox...")
        sandbox.resume()
        print("Sandbox resumed successfully.")

        print_section("Verifying state...")
        verify_result = run_command(sandbox, command="cat", args=["/tmp/state.txt"])
        print(f"Exit Code : {verify_result.exit_code}")
        print(f"STDOUT    : {verify_result.stdout!r}")
        print(f"STDERR    : {verify_result.stderr!r}")
    except ValueError as exc:
        print(f"Configuration error: {exc}")
        raise SystemExit(1) from exc
    except Exception as exc:
        print(f"Failed to complete example: {exc}")
        raise SystemExit(1) from exc
    finally:
        # Temporary lifecycle examples should still clean up after verification.
        print()
        print("Terminating sandbox...")
        cleanup_sandbox(sandbox)


if __name__ == "__main__":
    main()
