"""
Start, list, and kill a process inside a Tensorlake sandbox.

This example demonstrates process management by launching a long-lived command,
listing the running processes, and then terminating the target process.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.common import cleanup_sandbox, create_sandbox, load_api_key, print_section


def find_process(processes: Any, name: str) -> Any:
    """Return the first process whose name matches the requested value."""
    for process in processes:
        managed = getattr(process, "managed", None)
        managed_name = getattr(managed, "name", None) if managed else None
        if getattr(process, "name", None) == name or managed_name == name:
            return process
    return None


def main() -> None:
    """Create a sandbox, start a process, inspect it, and kill it."""
    print("Creating Tensorlake sandbox...")

    sandbox = None
    process_name = "example-08-sleep"
    try:
        api_key = load_api_key()
        sandbox = create_sandbox(api_key)
        print(f"Sandbox ID : {sandbox.sandbox_id}")
        print(f"Status     : {sandbox.status}")

        print_section("Starting process...")
        start_result = sandbox.start_process(
            command="sh",
            args=["-c", "sleep 60"],
            name=process_name,
        )
        print(f"Trace ID  : {start_result.trace_id}")
        print(f"Value     : {start_result.value!r}")

        print_section("Listing processes...")
        processes = list(sandbox.list_processes())
        for process in processes:
            managed = getattr(process, "managed", None)
            managed_name = getattr(managed, "name", "N/A") if managed else "N/A"
            print(
                f"- pid={getattr(process, 'pid', 'N/A')} "
                f"name={getattr(process, 'name', 'N/A')} "
                f"managed_name={managed_name}"
            )

        target = find_process(processes, process_name)
        if target is None:
            raise SystemExit(f"Could not find process named {process_name}.")

        pid = getattr(target, "pid", None)
        if pid is None:
            raise SystemExit("Process metadata did not include a pid.")

        print_section("Killing process...")
        kill_result = sandbox.kill_process(pid)
        print(f"Trace ID  : {kill_result.trace_id}")
        print(f"Value     : {kill_result.value!r}")
    except ValueError as exc:
        print(f"Configuration error: {exc}")
        raise SystemExit(1) from exc
    except Exception as exc:
        print(f"Failed to complete example: {exc}")
        raise SystemExit(1) from exc
    finally:
        # Temporary process-management examples should clean up their sandbox.
        print()
        print("Terminating sandbox...")
        cleanup_sandbox(sandbox)


if __name__ == "__main__":
    main()
