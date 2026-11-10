from app.db.metadata import target_metadata


def test_metadata_has_core_tables():
    tables = set(target_metadata.tables.keys())
    assert "curriculum_topics" in tables
    assert "curriculum_subtopics" in tables
    assert "class_sessions" in tables
    assert "lesson_plans" in tables
    assert "plan_versions" in tables
    assert "reference_materials" in tables
    assert "events" in tables


def test_metadata_has_renamed_tables():
    tables = set(target_metadata.tables.keys())
    assert "term_class_subjects" in tables
    assert "scheme_of_work" in tables
    assert "lesson_periods" in tables
    assert "exit_ticket_submissions" in tables
    assert "lesson_deliveries" in tables


def test_metadata_has_new_tables():
    tables = set(target_metadata.tables.keys())
    assert "artefact_plans" in tables
    assert "artefacts" in tables
    assert "curriculum_themes" in tables
    assert "knowledge_components" in tables
    assert "content_specifications" in tables
    assert "content_approvals" in tables
    assert "textbook_packets" in tables
    assert "textbook_records" in tables
    assert "textbook_record_subtopics" in tables
    assert "textbook_seed_runs" in tables
    assert "exit_ticket_items" in tables
    assert "student_item_responses" in tables


def test_metadata_has_no_dropped_tables():
    """A re-added model here would be created by 0001 and then dropped by 0008.

    ``0001_baseline`` builds a fresh DB with ``create_all`` off this metadata,
    so anything a later revision drops must stay out of it.
    """
    tables = set(target_metadata.tables.keys())
    assert "subtopic_mastery_states" not in tables
