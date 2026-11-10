"""Parse scheme-of-work HTML tables into JSON.

Input:  dataset/processed/scheme-of-work/JSS1 Lagos State Math Scheme-of-Work - *.md
Output: jss1_scheme.json
"""

from __future__ import annotations

import json
import re
from pathlib import Path

DATASET = Path(__file__).resolve().parents[4] / "dataset" / "processed"
SOW_DIR = DATASET / "scheme-of-work"
OUT_DIR = SOW_DIR

TERM_FILES = [
    ("First Term", "JSS1 Lagos State Math Scheme-of-Work - 1st Term.md"),
    ("Second Term", "JSS1 Lagos State Math Scheme-of-Work - 2nd Term.md"),
    ("Third Term", "JSS1 Lagos State Math Scheme-of-Work - 3rd Term.md"),
]

# Weeks to skip (revision, exam, vacation)
SKIP_PATTERNS = re.compile(
    r"revision|examination|exam|vacation|periodic\s+test|preparation",
    re.IGNORECASE,
)


def _clean_text(text: str) -> str:
    """Clean HTML artifacts and normalize whitespace."""
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _split_breakdown(text: str) -> list[str]:
    """Split breakdown cell into items."""
    # Split on <br>, newlines, or roman numeral prefixes
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    lines = text.split("\n")
    items = []
    for line in lines:
        line = line.strip()
        # Strip numbering: "i.", "ii.", "iii.", "iv.", "v.", "1.", "2."
        line = re.sub(r"^[ivxlc]+\.\s*", "", line, flags=re.IGNORECASE)
        line = re.sub(r"^\d+\.\s*", "", line)
        line = line.strip()
        if line:
            items.append(line)
    return items


def _extract_rows(html: str) -> list[tuple[str, str, str]]:
    """Extract (week, topic, breakdown) tuples from HTML table."""
    # Find all <tr>...</tr> blocks
    tr_pattern = re.compile(r"<tr>(.*?)</tr>", re.DOTALL)
    td_pattern = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL)

    rows = []
    for tr_match in tr_pattern.finditer(html):
        tr_content = tr_match.group(1)
        cells = td_pattern.findall(tr_content)
        if len(cells) < 3:
            continue

        week_raw = _clean_text(cells[0])
        topic_raw = cells[1]
        breakdown_raw = cells[2]

        # Skip header rows
        if week_raw.lower() in ("week", ""):
            continue
        # Skip non-numeric week entries (colspan headers, etc.)
        if not re.match(r"^\d", week_raw):
            continue

        # Handle malformed rows where topic text bleeds into
        # the week cell (e.g. "9\nPROCESSES" → week=9)
        week_num_match = re.match(r"(\d+)", week_raw)
        if not week_num_match:
            continue
        clean_week = week_num_match.group(1)

        # If week cell has extra text, it's the topic bleeding in
        extra = week_raw[len(clean_week) :].strip()
        if extra:
            topic_raw = extra + " " + _clean_text(topic_raw)

        rows.append((clean_week, topic_raw, breakdown_raw))

    return rows


def _parse_term(filepath: Path) -> list[dict]:
    """Parse a single term file into weekly entries."""
    content = filepath.read_text(encoding="utf-8")
    # Use only the first <table> block (1st term file has all 3 terms)
    table_match = re.search(r"<table>(.*?)</table>", content, re.DOTALL)
    if not table_match:
        return []
    raw_rows = _extract_rows(table_match.group(0))

    weeks = []
    for week_str, topic_html, breakdown_html in raw_rows:
        # Parse week number (handle "12 -13", "12-13")
        week_match = re.match(r"(\d+)", week_str)
        if not week_match:
            continue
        week_num = int(week_match.group(1))

        topic = _clean_text(topic_html)
        topic = re.sub(r"\s+", " ", topic).strip()

        # Fix known malformed entries (2nd term weeks 9-10)
        if re.match(r"^PROCESSES\s+ALGEBRAIC", topic):
            topic = "ALGEBRAIC PROCESSES"
        if re.match(r"^ALGEBRAIC\s+PROCESSES\s+COUNDED", topic):
            topic = "ALGEBRAIC PROCESSES CONTINUED"
        # Strip leading week number if duplicated in topic
        topic = re.sub(r"^\d+\s+", "", topic)

        # Skip revision/exam weeks
        if SKIP_PATTERNS.search(topic):
            continue

        breakdown = _split_breakdown(breakdown_html)

        weeks.append(
            {
                "week": week_num,
                "topic": topic,
                "breakdown": breakdown,
            }
        )

    return weeks


def parse_scheme_of_work() -> dict[str, list[dict]]:
    """Parse all term files, return {term_name: [weeks]}."""
    scheme = {}
    for term_name, filename in TERM_FILES:
        filepath = SOW_DIR / filename
        if not filepath.exists():
            print(f"  WARN: {filename} not found, skipping")
            continue
        weeks = _parse_term(filepath)
        scheme[term_name] = weeks
    return scheme


def main() -> None:
    print("Parsing scheme of work...")
    scheme = parse_scheme_of_work()

    out_path = OUT_DIR / "jss1_scheme.json"
    out_path.write_text(
        json.dumps(scheme, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    for term, weeks in scheme.items():
        print(f"  {term}: {len(weeks)} weeks")
    print(f"  -> {out_path.relative_to(DATASET.parent)}")


if __name__ == "__main__":
    main()
