"""Materialise and expose note files for filesystem-based generator arms."""

from pathlib import Path

from app.domains.artefacts.types.post_class_review_pack.infrastructure.dspy.tools.source_reading import (  # noqa: E501
    Toolset,
    numbered,
)


def materialize_workspace(notes: dict[str, str], root: Path) -> Path:
    """Write each approved note as its own Markdown file."""
    root.mkdir(parents=True, exist_ok=True)
    for step_id, note in notes.items():
        (root / f"{step_id}.md").write_text(note, encoding="utf-8")
    return root


def file_tools(root: Path) -> list:
    """Return read-only tools over one evaluation workspace."""

    def available() -> list[Path]:
        return sorted(root.glob("*.md"))

    def list_notes() -> list[dict]:
        """List the available lesson-note files and their line counts."""
        return [
            {"file": path.name, "lines": len(path.read_text().splitlines())} for path in available()
        ]

    def read_note(file: str, start_line: int = 1, end_line: int | None = None) -> str:
        """Read one note as numbered lines, using inclusive line bounds."""
        path = root / Path(file).name
        if path.suffix != ".md" or not path.exists():
            return f"No file named {file!r}. Available: {[item.name for item in available()]}"
        return numbered(path.read_text().splitlines(), start_line, end_line)

    return [list_notes, read_note]


def workspace_toolset(root: Path) -> Toolset:
    """Return a generator toolset backed by one evaluation workspace."""
    return lambda request, unit: file_tools(root)
