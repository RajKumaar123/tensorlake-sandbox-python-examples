"""
Run a lightweight AI-agent style demo inside Tensorlake.

This example uses a PTY session as the interactive primitive and then runs a
simple command that represents an agent-style action inside the sandbox.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.common import cleanup_sandbox, create_sandbox, load_api_key, print_section


def main() -> None:
    """Create a sandbox, open an interactive session, and run a demo action."""
    print("Creating Tensorlake sandbox...")

    sandbox = None
    try:
        api_key = load_api_key()
        sandbox = create_sandbox(api_key, name="example-12-ai-agent-demo")
        print(f"Sandbox ID : {sandbox.sandbox_id}")
        print(f"Status     : {sandbox.status}")

        print_section("Creating agent session...")
        session = sandbox.create_pty_session(
            command="python",
            args=["-c", "print('agent-ready')"],
        )
        print(f"Trace ID   : {session.trace_id}")
        print(f"Session ID : {session.value['session_id']}")
        print(f"Token      : {session.value['token']}")

        print_section("Running agent-style action...")
        action_result = sandbox.run(
            command="python",
            args=["-c", "print('plan -> execute -> verify')"],
        )
        print(f"Trace ID  : {action_result.trace_id}")
        print(f"Exit Code : {action_result.exit_code}")
        print(f"STDOUT    : {action_result.stdout!r}")
        print(f"STDERR    : {action_result.stderr!r}")
    except ValueError as exc:
        print(f"Configuration error: {exc}")
        raise SystemExit(1) from exc
    except Exception as exc:
        print(f"Failed to complete example: {exc}")
        raise SystemExit(1) from exc
    finally:
        # AI-agent demos should clean up their sandbox after the verification step.
        print()
        print("Terminating sandbox...")
        cleanup_sandbox(sandbox)


if __name__ == "__main__":
    main()
