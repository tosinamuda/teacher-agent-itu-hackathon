"""A plugin folder's files: text kept, hidden files and bytecode caches left out."""

from __future__ import annotations

from pathlib import Path

from app.domains.content.plugins.reader import folder_digest, read_files


def test_a_bytecode_cache_and_a_hidden_file_are_not_part_of_the_plugin(tmp_path: Path) -> None:
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "check.py").write_text("print('[]')", encoding="utf-8")
    (tmp_path / "scripts" / "__pycache__").mkdir()
    (tmp_path / "scripts" / "__pycache__" / "check.cpython-312.pyc").write_bytes(b"\xff\x00\xfe")
    (tmp_path / ".DS_Store").write_bytes(b"\xff\x00")
    before = folder_digest(tmp_path)

    files, problems = read_files(tmp_path)

    assert (files, problems) == ({"scripts/check.py": "print('[]')"}, [])
    (tmp_path / "scripts" / "__pycache__" / "other.pyc").write_bytes(b"\x01")
    assert folder_digest(tmp_path) == before
