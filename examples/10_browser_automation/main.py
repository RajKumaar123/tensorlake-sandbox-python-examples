"""
Create a PTY session that can be used as a browser-automation primitive.

This example demonstrates the interactive session setup Tensorlake exposes
for browser-style automation workflows. It creates a PTY session, prints the
session credentials, and then cleans up the sandbox.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.common import cleanup_sandbox, create_sandbox, load_api_key, print_section


def main() -> None:
    """Create a sandbox and start an interactive PTY session."""
    print("Creating Tensorlake sandbox...")

    sandbox = None
    try:
        api_key = load_api_key()
        sandbox = create_sandbox(api_key, name="example-10-browser-automation")
        print(f"Sandbox ID : {sandbox.sandbox_id}")
        print(f"Status     : {sandbox.status}")

        print_section("Creating PTY session...")
        session = sandbox.create_pty_session(
            command="python",
            args=["--version"],
        )
        print(f"Trace ID   : {session.trace_id}")
        print(f"Session ID : {session.value['session_id']}")
        print(f"Token      : {session.value['token']}")
    except ValueError as exc:
        print(f"Configuration error: {exc}")
        raise SystemExit(1) from exc
    except Exception as exc:
        print(f"Failed to complete example: {exc}")
        raise SystemExit(1) from exc
    finally:
        # Temporary browser-automation primitives should still clean up the sandbox.
        print()
        print("Terminating sandbox...")
        cleanup_sandbox(sandbox)


if __name__ == "__main__":
    main()
