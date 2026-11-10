"""Analyze linked textbook chunk tokens by subtopic.

Usage:
    cd apps/backend
    uv run python scripts/analyze_textbook_tokens.py
    uv run python scripts/analyze_textbook_tokens.py --encoding cl100k_base
    uv run python scripts/analyze_textbook_tokens.py \\
        --output .diagnostics/textbook-subtopic-token-table.md
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import tiktoken

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # apps/backend root

from scripts.textbook_corpus_lib import (
    linked_records_path,
    linked_subtopic_catalog_path,
    load_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--encoding",
        default="o200k_base",
        help="tiktoken encoding name to use for counting. Default: o200k_base.",
    )
    parser.add_argument(
        "--output",
        help="Optional path to write the markdown table.",
    )
    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def _normalized_text(value: Any) -> str:
    return " ".join(str(value or "").split())


def chunk_text(record: dict[str, Any]) -> str:
    """Build the non-duplicated chunk text for one linked textbook record."""
    parts: list[str] = []
    for key in ("content_text", "prompt_text", "answer_text"):
        text = _normalized_text(record.get(key))
        if text and text not in parts:
            parts.append(text)
    if parts:
        return "\n\n".join(parts)
    return _normalized_text(record.get("retrieval_text"))


def markdown_table(rows: list[dict[str, Any]], *, encoding_name: str) -> str:
    lines = [
        f"# Textbook Token Counts By Subtopic ({encoding_name})",
        "",
        (
            "| Subtopic ID | Subtopic | Topic | Chunks | Total Chunk Tokens | "
            "Avg Tokens / Chunk | Max Chunk Tokens |"
        ),
        "| --- | --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            "| {subtopic_id} | {subtopic_title} | {topic_title} | {chunk_count} | "
            "{total_chunk_tokens} | {avg_chunk_tokens:.1f} | {max_chunk_tokens} |".format(**row)
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    encoding = tiktoken.get_encoding(args.encoding)

    catalog = load_json(linked_subtopic_catalog_path())
    catalog_rows = catalog["subtopics"] if isinstance(catalog, dict) else catalog
    records = load_jsonl(linked_records_path())

    records_by_subtopic: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        token_count = len(encoding.encode(chunk_text(record)))
        for subtopic_id in record.get("subtopic_ids") or []:
            records_by_subtopic.setdefault(subtopic_id, []).append(
                {
                    "record_id": record.get("record_id"),
                    "token_count": token_count,
                }
            )

    rows: list[dict[str, Any]] = []
    for subtopic in catalog_rows:
        subtopic_id = str(subtopic.get("subtopic_id") or "").strip()
        if not subtopic_id:
            continue
        chunk_tokens = [item["token_count"] for item in records_by_subtopic.get(subtopic_id, [])]
        chunk_count = len(chunk_tokens)
        total_chunk_tokens = sum(chunk_tokens)
        avg_chunk_tokens = total_chunk_tokens / chunk_count if chunk_count else 0.0
        max_chunk_tokens = max(chunk_tokens) if chunk_tokens else 0
        rows.append(
            {
                "subtopic_id": subtopic_id,
                "subtopic_title": str(subtopic.get("subtopic_title") or "").strip(),
                "topic_title": str(subtopic.get("topic_title") or "").strip(),
                "chunk_count": chunk_count,
                "total_chunk_tokens": total_chunk_tokens,
                "avg_chunk_tokens": avg_chunk_tokens,
                "max_chunk_tokens": max_chunk_tokens,
            }
        )

    table = markdown_table(rows, encoding_name=args.encoding)
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(table, encoding="utf-8")

    print(table, end="")


if __name__ == "__main__":
    main()
