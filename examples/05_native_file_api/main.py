"""
Use Tensorlake's native file APIs to write, read, list, and delete a file.

This example uses the SDK file methods directly instead of shell commands, and
it cleans up the temporary sandbox after the workflow completes.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.common import (
    cleanup_sandbox,
    create_sandbox,
    load_api_key,
    print_section,
)


def describe_directory_entries(listing: Any) -> str:
    """Format directory entries into a readable text block."""
    lines = [f"path={listing.path}"]
    for entry in listing.entries:
        entry_type = "dir" if entry.is_dir else "file"
        lines.append(f"- {entry.name} ({entry_type})")
    return "\n".join(lines)


def main() -> None:
    """Create a sandbox and exercise the native file APIs."""
    print("Creating Tensorlake sandbox...")

    sandbox = None
    try:
        api_key = load_api_key()
        sandbox = create_sandbox(api_key)
        print(f"Sandbox ID : {sandbox.sandbox_id}")
        print(f"Status     : {sandbox.status}")

        print_section("Writing file...")
        write_result = sandbox.write_file(
            path="/tmp/native_example.txt",
            content=b"Hello from Tensorlake native file APIs!",
        )
        print(f"Trace ID  : {write_result.trace_id}")
        print(f"Value     : {write_result.value!r}")

        print_section("Reading file...")
        read_result = sandbox.read_file(path="/tmp/native_example.txt")
        print(f"Trace ID  : {read_result.trace_id}")
        print(f"Value     : {read_result.value!r}")

        print_section("Listing /tmp...")
        list_result = sandbox.list_directory(path="/tmp")
        print(f"Trace ID  : {list_result.trace_id}")
        print(describe_directory_entries(list_result.value))

        print_section("Deleting file...")
        delete_result = sandbox.delete_file(path="/tmp/native_example.txt")
        print(f"Trace ID  : {delete_result.trace_id}")
        print(f"Value     : {delete_result.value!r}")
    except ValueError as exc:
        print(f"Configuration error: {exc}")
        raise SystemExit(1) from exc
    except Exception as exc:
        print(f"Failed to complete example: {exc}")
        raise SystemExit(1) from exc
    finally:
        # Temporary sandboxes should be cleaned up after use to avoid quota buildup.
        print()
        print("Terminating sandbox...")
        cleanup_sandbox(sandbox)


if __name__ == "__main__":
    main()
