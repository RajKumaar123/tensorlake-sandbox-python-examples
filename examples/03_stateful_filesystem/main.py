"""
Demonstrate that files created in a Tensorlake sandbox persist across commands.

This example intentionally keeps the sandbox alive because persistence is the
subject being demonstrated.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.common import create_sandbox, load_api_key, print_section


def run_command(sandbox: Any, command: str, args: list[str]) -> Any:
    """Run a command in the sandbox and return the result object."""
    return sandbox.run(command=command, args=args)


def main() -> None:
    """Create a sandbox, write a file, read it back, and list /tmp."""
    print("Creating Tensorlake sandbox...")

    try:
        api_key = load_api_key()
        sandbox = create_sandbox(api_key)
    except ValueError as exc:
        print(f"Configuration error: {exc}")
        raise SystemExit(1) from exc
    except Exception as exc:
        print(f"Failed to create sandbox: {exc}")
        raise SystemExit(1) from exc

    print(f"Sandbox ID : {sandbox.sandbox_id}")
    print(f"Status     : {sandbox.status}")

    print_section("Creating file...")
    create_result = run_command(
        sandbox,
        command="sh",
        args=["-c", "echo 'Hello Tensorlake!' > /tmp/hello.txt"],
    )
    print(f"Exit Code : {create_result.exit_code}")
    print(f"STDOUT    : {create_result.stdout!r}")
    print(f"STDERR    : {create_result.stderr!r}")

    print_section("Reading file...")
    read_result = run_command(
        sandbox,
        command="cat",
        args=["/tmp/hello.txt"],
    )
    print(f"Exit Code : {read_result.exit_code}")
    print(f"STDOUT    : {read_result.stdout!r}")
    print(f"STDERR    : {read_result.stderr!r}")

    print_section("Listing /tmp...")
    list_result = run_command(
        sandbox,
        command="ls",
        args=["-l", "/tmp"],
    )
    print(list_result.stdout)

    # This example demonstrates filesystem persistence, so the sandbox is
    # intentionally left running until the experiment is complete.


if __name__ == "__main__":
    main()
