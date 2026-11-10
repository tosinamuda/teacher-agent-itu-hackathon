"""Run the blinding checks over documents that have come back from the raters.

The build scans what it writes. A returned document carries something the build never
saw — the rater's own typing — so it has to be scanned again before it is committed,
against the same rules: no condition label, no student id, no lesson code, no internal
packet id, no candidate id, no run label.

The two checks answer differently on a returned document. An identifier is a failure
wherever it appears. A sensitive word is a failure only in what was *issued*: the build
must never print "generated", because that word breaks the blind. A rater who writes it
has told us something instead, and it is reported here rather than refused.

Run with::

    uv run python -m experiments.human_rating.disclosure <folder>
"""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

from .render import LeakError, leak_scan, sensitive_words

#: Word stores a paragraph's text in runs; the tags between them are not a word boundary
#: anywhere a rater typed, so they are dropped rather than replaced with a space.
_TAG = re.compile(r"<[^>]+>")
_PARAGRAPH = re.compile(r"</w:p>")


def text_of(document: Path) -> str:
    with zipfile.ZipFile(document) as archive:
        xml = archive.read("word/document.xml").decode("utf-8", "ignore")
    return _TAG.sub("", _PARAGRAPH.sub("\n", xml))


def scan(folder: Path) -> int:
    documents = sorted(folder.rglob("*.docx"))
    failures: list[tuple[Path, str]] = []
    flagged: list[tuple[Path, list[str]]] = []
    for document in documents:
        body = text_of(document)
        try:
            leak_scan(body)
        except LeakError as leak:
            failures.append((document, str(leak)))
        words = sensitive_words(body)
        if words:
            flagged.append((document, words))

    print(f"scanned {len(documents)} documents under {folder.name}")
    print(f"  identifier leaks : {len(failures)}")
    print(f"  sensitive words  : {len(flagged)}  (in rater prose, these are findings)")
    for document, leak in failures[:20]:
        print(f"    LEAK  {document.name}: {leak}")
    for document, words in flagged[:20]:
        print(f"    WORD  {document.name}: {', '.join(sorted(set(words)))}")
    return 1 if failures else 0


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    return scan(Path(sys.argv[1]))


if __name__ == "__main__":
    raise SystemExit(main())
