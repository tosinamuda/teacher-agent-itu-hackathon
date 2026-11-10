"""What is wrong with a plugin folder: one problem per fault, naming the file and the fix."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True)
class Problem:
    file: str
    message: str
    severity: Severity = Severity.ERROR

    def __str__(self) -> str:
        """The problem as a line of output."""
        return f"{self.severity.value}: {self.file}: {self.message}"


class PluginError(ValueError):
    """A plugin that cannot be used; ``problems`` lists everything found wrong."""

    def __init__(self, problems: list[Problem]) -> None:
        super().__init__("; ".join(str(problem) for problem in problems))
        self.problems = problems


def errors_in(problems: list[Problem]) -> list[Problem]:
    return [problem for problem in problems if problem.severity is Severity.ERROR]
