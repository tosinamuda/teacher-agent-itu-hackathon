from fastapi.routing import APIRoute

from app.main import app


def _route_paths() -> set[str]:
    return {route.path for route in app.routes if isinstance(route, APIRoute)}


def test_health_endpoint_exists():
    assert "/health" in _route_paths()


def test_root_endpoint_exists():
    assert "/" in _route_paths()


def test_events_endpoint_exists():
    assert "/events" in _route_paths()


def test_plans_endpoint_exists():
    assert "/artefacts/lesson-plans/generate" in _route_paths()


def test_a_plan_is_approved_as_content():
    paths = _route_paths()
    assert "/content/{content_id}/approvals" in paths
    assert "/artefacts/lesson-plans/versions/{version_id}/approve" not in paths


def test_teaching_sequence_routes_exist():
    route_paths = _route_paths()
    assert "/teaching/term-class-subjects/by-id/{term_class_subject_id}" in route_paths
    assert "/teaching/term-class-subjects/{course_id}" in route_paths
    assert "/teaching/scheme-of-work/{week_id}" in route_paths
    assert "/teaching/lesson-periods/{lesson_period_id}" in route_paths


def test_old_curriculum_sequence_routes_are_removed():
    route_paths = _route_paths()
    assert "/curriculum/term-class-subjects/by-id/{tcs_id}" not in route_paths
    assert "/curriculum/term-class-subjects/{course_id}" not in route_paths
    assert "/curriculum/scheme-of-work/{week_id}" not in route_paths
    assert "/curriculum/lesson-periods/{period_id}" not in route_paths
