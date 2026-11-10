"""Which objective each comparison panel actually names, read from the delivered document.

A Part 2 document carries a panel only for the objectives a student has class work for,
sorted into curriculum order. That is a *subset*, not a prefix, so the panel's ordinal
says nothing about which objective it is: in the delivered set, 36 of 70 panels sit at an
ordinal that names a different objective. Reading the heading is the only way to know.

Every panel prints ``**Learning objective.** <title>`` directly under its comparison
heading, and the title comes from the same lesson plan the ids come from, so the match is
exact text against the plan's own titles. When it does not match, the panel resolves to
``None`` and the caller records the failure. There is deliberately no positional
fallback: a wrong id that looks plausible is worse than a gap that announces itself.
"""

from __future__ import annotations

import re
import zipfile
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

from . import reference

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
COMPARISON_HEADING = re.compile(r"^Objective (\d+) of (\d+) — your comparison")
LEARNING_OBJECTIVE = re.compile(r"^Learning objective\.\s*(.+?)\s*$")


@dataclass(frozen=True)
class Panel:
    """One comparison table, and the objective its own heading names."""

    ordinal: int
    """Position in the document, counting from one. NOT an objective index."""
    heading_text: str
    objective_id: str | None
    """``None`` when the heading matched no objective in the lesson plan."""

    @property
    def resolved(self) -> bool:
        return self.objective_id is not None


def _paragraphs(path: Path):
    with zipfile.ZipFile(path) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    for para in root.find(f"{W}body"):
        if para.tag != f"{W}p":
            continue
        text = "".join(node.text or "" for node in para.iter(f"{W}t")).strip()
        if not text:
            continue
        style = para.find(f"{W}pPr/{W}pStyle")
        yield (style.get(f"{W}val") if style is not None else ""), text


def resolve(paragraphs: Iterable[tuple[str, str]], plan: dict[str, Any]) -> list[Panel]:
    """Every comparison panel in a styled paragraph stream, in document order."""
    by_title = {title.rstrip(". "): oid for oid, title in reference.objectives(plan)}
    found: list[Panel] = []
    pending: int | None = None
    for style, text in paragraphs:
        if style.startswith("Heading") and (match := COMPARISON_HEADING.match(text)):
            pending = int(match.group(1))
            continue
        if pending is None:
            continue
        if objective := LEARNING_OBJECTIVE.match(text):
            title = objective.group(1).rstrip(". ")
            found.append(Panel(pending, title, by_title.get(title)))
            pending = None
    return found


def displayed(path: Path, plan: dict[str, Any]) -> list[Panel]:
    """Every comparison panel in one delivered document."""
    return resolve(_paragraphs(path), plan)
