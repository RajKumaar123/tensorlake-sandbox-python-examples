"""
Create a Tensorlake sandbox and display its key details.

This example demonstrates the first verified Tensorlake workflow:
loading credentials, creating a sandbox, and reading basic metadata.
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
    get_sandbox_status,
    load_api_key,
    print_section,
)


def main() -> None:
    """Create a sandbox and print a concise summary of the result."""
    print("Creating Tensorlake sandbox...")

    sandbox = None
    try:
        api_key = load_api_key()
        sandbox = create_sandbox(api_key)
    except ValueError as exc:
        print(f"Configuration error: {exc}")
        raise SystemExit(1) from exc
    except Exception as exc:
        print(f"Failed to create sandbox: {exc}")
        raise SystemExit(1) from exc

    print("Sandbox created successfully.")
    print_section("Sandbox Details")
    print(f"Sandbox ID    : {sandbox.sandbox_id}")
    print(f"Sandbox Name  : {getattr(sandbox, 'name', 'N/A')}")
    print(f"Sandbox Status: {get_sandbox_status(sandbox)}")
    print("-" * 40)
    print()
    print("Terminating sandbox...")
    cleanup_sandbox(sandbox)

    # This example creates a temporary sandbox, so we clean it up after use.


if __name__ == "__main__":
    main()
