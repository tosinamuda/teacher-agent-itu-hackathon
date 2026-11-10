"""The published copy of a file, and the only three ways it may differ from the repository's."""

from __future__ import annotations

import pytest

from experiments.dataset_export.rewrite import (
    CLASSWORK_RELEASE,
    CLASSWORK_WARNING,
    PRIVATE_NOTE,
    ExportError,
    published,
    without_private_paths,
    without_school,
)


def test_the_school_is_replaced_wherever_it_stands_as_a_word_and_keeps_its_case():
    assert without_school('"session_id": "gtc-t2-w09",') == '"session_id": "sch-t2-w09",'
    assert without_school("source_directory: ../original-captures/GTC Data/week 5") == (
        "source_directory: ../original-captures/SCH Data/week 5"
    )
    assert without_school("# Transcript schema (GTC field capture)") == (
        "# Transcript schema (SCH field capture)"
    )
    assert without_school("`gtc-curriculum-linkage.md`") == "`sch-curriculum-linkage.md`"


def test_a_tool_call_id_that_happens_to_spell_it_is_left_as_it_was_sent():
    for recorded in ("call_00_zpQGTC4xk", "ik0T8vAJukWeSpgtc", "_nrjKLRzfg72yyGtC"):
        assert without_school(recorded) == recorded


def test_a_classwork_file_leaves_with_the_basis_of_its_release_instead_of_its_warning():
    declaration = '<?xml version="1.0" encoding="utf-8"?>'
    source = f'{declaration}\n{CLASSWORK_WARNING}\n<classwork lesson="t2-w09">'
    out = published("transcripts/t2-w09/classwork.xml", source.encode()).decode()
    assert CLASSWORK_WARNING not in out
    assert CLASSWORK_RELEASE in out


def test_a_classwork_file_whose_warning_has_changed_is_refused_rather_than_shipped():
    with pytest.raises(ExportError):
        published("transcripts/t2-w09/classwork.xml", b"<classwork/>")


def test_a_binary_is_copied_byte_for_byte_even_when_its_bytes_spell_the_school():
    blob = b"%PDF-1.7\n\x00stream gtc \xff\xfe endstream"
    assert published("transcripts/_render/page.pdf", blob) == blob


def test_a_path_into_the_private_captures_leaves_as_a_note_that_they_are_not_released():
    field = "scripts_directory: ../original-captures/SCH Data/student/*/week-4 - 3rd Term"
    assert without_private_paths(field) == f"scripts_directory: {PRIVATE_NOTE}"
    prose = "The scripts sit in `../original-captures/SCH Data/student/*/Not Picked/`, which the"
    assert without_private_paths(prose) == f"The scripts sit in {PRIVATE_NOTE}, which the"
    assert without_private_paths(
        "fields in `../original-captures/sch-normalized/manifest.json`."
    ) == (f"fields in {PRIVATE_NOTE}.")


def test_a_published_transcript_names_neither_the_school_nor_the_private_folder():
    source = (
        "source_directory: ../original-captures/GTC Data/week 5 - 3rd Term\nlesson: gtc-t3-w05\n"
    )
    out = published("transcripts/t3-w05/teacher.md", source.encode()).decode()
    assert out == f"source_directory: {PRIVATE_NOTE}\nlesson: sch-t3-w05\n"
