"""
Create parallel Tensorlake sandboxes from a source sandbox copy.

This example demonstrates sandbox duplication and verifies that each copy can
run independent work while the source sandbox remains available.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.common import cleanup_sandbox, create_sandbox, load_api_key, print_section


def main() -> None:
    """Create a source sandbox, clone it, and verify the copies."""
    print("Creating Tensorlake sandbox...")

    source = None
    clones: list[Any] = []
    try:
        api_key = load_api_key()
        source = create_sandbox(api_key, name="example-09-parallel-source")
        print(f"Source Sandbox ID : {source.sandbox_id}")
        print(f"Status           : {source.status}")

        print_section("Creating copies...")
        copy_result = source.copy(times=1)
        print(f"Trace ID  : {copy_result.trace_id}")
        print(f"Value     : {copy_result.value!r}")

        clone_ids = list(getattr(copy_result.value, "sandbox_ids", []) or [])
        if not clone_ids:
            raise SystemExit("No clone sandbox IDs were returned by copy().")

        for idx, sandbox_id in enumerate(clone_ids, start=1):
            clone = source.__class__.connect(sandbox_id, api_key=api_key)
            clones.append(clone)
            print(f"Clone {idx} Sandbox ID : {clone.sandbox_id}")
            print(f"Clone {idx} Status     : {clone.status}")

        print_section("Verifying clones...")
        for idx, clone in enumerate(clones, start=1):
            result = clone.run(
                command="python",
                args=["-c", f"print('clone-{idx}')"],
            )
            print(f"Clone {idx} Trace ID : {result.trace_id}")
            print(f"Clone {idx} STDOUT   : {result.stdout!r}")
            print(f"Clone {idx} STDERR   : {result.stderr!r}")
    except ValueError as exc:
        print(f"Configuration error: {exc}")
        raise SystemExit(1) from exc
    except Exception as exc:
        print(f"Failed to complete example: {exc}")
        raise SystemExit(1) from exc
    finally:
        # Parallel sandbox examples should clean up every sandbox they create.
        for clone in clones:
            print("Terminating clone sandbox...")
            cleanup_sandbox(clone)

        print("Terminating source sandbox...")
        cleanup_sandbox(source)


if __name__ == "__main__":
    main()
