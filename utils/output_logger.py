"""
Utility functions for logging console output and saving it to output.txt.

Each example uses this helper so that the console output shown during
execution is also written to an output.txt file alongside the example.
"""

from __future__ import annotations

from pathlib import Path


class OutputLogger:
    """Log messages to both the console and an output file."""

    def __init__(self, script_file: str | Path) -> None:
        """
        Initialize the logger.

        Args:
            script_file: Path to the current script (__file__). The logger
                creates an output.txt file in the same directory.
        """
        self.output_file = Path(script_file).with_name("output.txt")
        self.lines: list[str] = []

    def log(self, message: str = "") -> None:
        """
        Print a message to the console and store it for output.txt.

        Args:
            message: Message to log. Defaults to a blank line.
        """
        print(message)
        self.lines.append(message)

    def clear(self) -> None:
        """Clear all previously captured log messages."""
        self.lines.clear()

    def save(self) -> Path:
        """
        Save all captured messages to output.txt.

        Returns:
            Path to the generated output.txt file.
        """
        # Create the directory if it does not already exist.
        self.output_file.parent.mkdir(parents=True, exist_ok=True)

        self.output_file.write_text(
            "\n".join(self.lines),
            encoding="utf-8",
        )

        return self.output_file