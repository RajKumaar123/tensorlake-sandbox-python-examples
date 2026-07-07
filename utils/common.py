"""Shared helpers for Tensorlake examples."""

from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv

from tensorlake.sandbox import Sandbox


def load_api_key() -> str:
    """Load and validate the Tensorlake API key from the environment."""
    # Every example starts by loading the local .env file.
    load_dotenv()

    api_key = os.getenv("TENSORLAKE_API_KEY")
    if not api_key:
        raise ValueError(
            "TENSORLAKE_API_KEY is missing. Add it to your .env file first."
        )

    return api_key


def create_sandbox(api_key: str, name: str | None = None) -> Any:
    """Create and return a Tensorlake sandbox."""
    # Keep sandbox creation in one place so examples stay focused.
    return Sandbox.create(api_key=api_key, name=name)


def get_sandbox_status(sandbox: Any) -> Any:
    """Return sandbox status whether the SDK exposes it as a property or method."""
    status = getattr(sandbox, "status", None)
    if callable(status):
        return status()
    return status


def cleanup_sandbox(sandbox: Any) -> None:
    """Safely terminate a Tensorlake sandbox."""
    if sandbox is None:
        return

    try:
        # Temporary sandboxes should be released after use to avoid quota issues.
        sandbox.terminate()
        print("Sandbox terminated successfully.")
    except Exception as exc:
        print(f"Cleanup failed: {exc}")


def print_section(title: str) -> None:
    """Print a consistent section header for example output."""
    print()
    print(title)
    print("-" * 40)


def format_output(text: Any) -> str:
    """Return text encoded safely for console output."""
    if text is None:
        return ""

    return str(text).encode("ascii", "backslashreplace").decode("ascii")
