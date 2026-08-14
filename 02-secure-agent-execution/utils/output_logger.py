"""Small console-and-file logger for secure-agent-execution experiments."""

from __future__ import annotations

from pathlib import Path


class OutputLogger:
    """Capture experiment output while also printing it to the console."""

    def __init__(self, experiment_file: str) -> None:
        experiment_path = Path(experiment_file).resolve()

        self.output_path = experiment_path.parent / "output.txt"
        self._lines: list[str] = []

    def log(self, message: str = "") -> None:
        """Print and capture one output line."""
        print(message)
        self._lines.append(message)

    def save(self) -> None:
        """Overwrite the experiment-specific output file with captured output."""
        self.output_path.write_text("\n".join(self._lines) + "\n", encoding="utf-8")
