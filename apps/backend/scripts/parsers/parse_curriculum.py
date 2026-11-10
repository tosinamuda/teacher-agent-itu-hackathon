"""Parse NERDC curriculum markdown tables into JSON intermediates.

Input:  dataset/processed/curriculum/THEME *.md (5 pipe-delimited tables)
Output: jss1_themes.json, jss1_topics.json
"""

from __future__ import annotations

import json
import re
from pathlib import Path

DATASET = Path(__file__).resolve().parents[4] / "dataset" / "processed"
CURRICULUM_DIR = DATASET / "curriculum"
OUT_DIR = CURRICULUM_DIR

THEME_FILES = [
    ("jss1-theme-1", "Number and Numeration", "THEME 1 - Number and Numeration.md"),
    ("jss1-theme-2", "Basic Operations", "Theme 2 - Basic Operation.md"),
    ("jss1-theme-3", "Algebra Processes", "Theme 3 - Algebra Processes.md"),
    ("jss1-theme-4", "Mensuration and Geometry", "Theme 4 - Mensuration And Geometry.md"),
    ("jss1-theme-5", "Everyday Statistics", "Theme 5 - Everyday Statistics.md"),
]


def _slugify(text: str) -> str:
    """Convert text to a URL-safe slug."""
    s = text.lower().strip()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"[\s]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def _split_cell(cell: str) -> list[str]:
    """Split a markdown table cell by <br>, strip numbering."""
    parts = re.split(r"<br\s*/?>", cell, flags=re.IGNORECASE)
    result = []
    for p in parts:
        p = p.strip()
        # Strip leading numbering: "1. ", "2. ", "i. ", "ii.", etc.
        p = re.sub(r"^\d+\.\s*", "", p)
        p = re.sub(r"^[ivxlc]+\.\s*", "", p, flags=re.IGNORECASE)
        p = p.strip()
        if p:
            result.append(p)
    return result


def _parse_table(md_text: str) -> list[list[str]]:
    """Parse a pipe-delimited markdown table into rows of cells."""
    lines = md_text.strip().split("\n")
    rows = []
    for line in lines:
        line = line.strip()
        if not line.startswith("|"):
            continue
        # Skip separator line
        if re.match(r"^\|[\s\-:|]+\|$", line):
            continue
        cells = [c.strip() for c in line.split("|")]
        # Remove empty first/last from leading/trailing pipes
        if cells and cells[0] == "":
            cells = cells[1:]
        if cells and cells[-1] == "":
            cells = cells[:-1]
        if len(cells) >= 8:
            rows.append(cells)
    return rows


def parse_curriculum() -> tuple[list[dict], list[dict]]:
    """Parse all theme files, return (themes, topics)."""
    themes = []
    topics = []

    for theme_key, theme_title, filename in THEME_FILES:
        filepath = CURRICULUM_DIR / filename
        if not filepath.exists():
            print(f"  WARN: {filename} not found, skipping")
            continue

        md = filepath.read_text(encoding="utf-8")
        rows = _parse_table(md)

        # Skip header row (first row with "#" in first cell)
        data_rows = []
        for r in rows:
            if r[0].strip() == "#" or r[0].strip().lower() == "no":
                continue
            data_rows.append(r)

        topic_titles = []
        for row in data_rows:
            # Columns: #, Topic, PerfObj, SubTopics, TA, SA, TLM, EG
            topic_name = row[1].strip()
            topic_key = f"jss1-math-{_slugify(topic_name)}"

            objectives = _split_cell(row[2])
            subtopic_items = _split_cell(row[3])
            teacher_activities = _split_cell(row[4])
            student_activities = _split_cell(row[5])
            tlm = _split_cell(row[6])
            eval_guide = _split_cell(row[7])

            subtopics = []
            for st_title in subtopic_items:
                st_slug = _slugify(st_title)
                subtopic_id = f"{topic_key}-{st_slug}"
                subtopics.append(
                    {
                        "subtopic_id": subtopic_id,
                        "title": st_title,
                    }
                )

            topic_titles.append(topic_name)
            topics.append(
                {
                    "theme_key": theme_key,
                    "topic": topic_name,
                    "topic_key": topic_key,
                    "objectives": objectives,
                    "subtopics": subtopics,
                    "teacher_activities": teacher_activities,
                    "student_activities": student_activities,
                    "tlm": tlm,
                    "eval_guide": eval_guide,
                }
            )

        themes.append(
            {
                "key": theme_key,
                "title": theme_title,
                "topic_titles": topic_titles,
            }
        )

    return themes, topics


def main() -> None:
    print("Parsing curriculum...")
    themes, topics = parse_curriculum()

    themes_path = OUT_DIR / "jss1_themes.json"
    topics_path = OUT_DIR / "jss1_topics.json"

    themes_path.write_text(json.dumps(themes, indent=2, ensure_ascii=False), encoding="utf-8")
    topics_path.write_text(json.dumps(topics, indent=2, ensure_ascii=False), encoding="utf-8")

    total_subtopics = sum(len(t["subtopics"]) for t in topics)
    print(f"  {len(themes)} themes, {len(topics)} topics, {total_subtopics} subtopics")
    print(f"  -> {themes_path.relative_to(DATASET.parent)}")
    print(f"  -> {topics_path.relative_to(DATASET.parent)}")


if __name__ == "__main__":
    main()
