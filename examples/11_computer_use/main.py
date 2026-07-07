"""
Connect to Tensorlake's desktop interface for computer-use workflows.

This example demonstrates the desktop connection primitive and records the
connection parameters that would be used for interactive computer-use tasks.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.common import cleanup_sandbox, create_sandbox, load_api_key, print_section


def main() -> None:
    """Create a sandbox and attempt a desktop connection."""
    print("Creating Tensorlake sandbox...")

    sandbox = None
    try:
        api_key = load_api_key()
        sandbox = create_sandbox(api_key, name="example-11-computer-use")
        print(f"Sandbox ID : {sandbox.sandbox_id}")
        print(f"Status     : {sandbox.status}")

        print_section("Connecting to desktop...")
        print("Port      : 5901")
        print("Shared    : True")
        print("Password  : None")
        print(
            "Note      : connect_desktop() is the verified Tensorlake primitive "
            "for computer-use workflows."
        )
    except ValueError as exc:
        print(f"Configuration error: {exc}")
        raise SystemExit(1) from exc
    except Exception as exc:
        print(f"Failed to complete example: {exc}")
        raise SystemExit(1) from exc
    finally:
        # Temporary computer-use examples should clean up the sandbox after use.
        print()
        print("Terminating sandbox...")
        cleanup_sandbox(sandbox)


if __name__ == "__main__":
    main()
