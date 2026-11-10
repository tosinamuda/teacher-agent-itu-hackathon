"""Every route asks who is calling, unless it is listed here as open on purpose.

A route is guarded when it depends on ``requires(...)`` or on the resolved actor. The open
ones are catalogues and public metadata, health, drawings and client telemetry; none
returns a person's work, and none writes except the telemetry event.
"""

from __future__ import annotations

from fastapi.dependencies.models import Dependant
from fastapi.routing import APIRoute

from app.main import app

OPEN_ON_PURPOSE: dict[tuple[str, str], str] = {
    ("GET", "/"): "service banner",
    ("GET", "/health"): "liveness probe",
    ("GET", "/figures/{figure_id}.svg"): "content-addressed drawings, public by design",
    ("POST", "/events"): "client telemetry",
    ("GET", "/evaluation/meta"): "study title and institution",
    ("GET", "/experiments/research-defaults"): "default study settings",
    ("GET", "/curriculum/topics"): "the syllabus catalogue",
    ("GET", "/curriculum/sessions"): "the syllabus catalogue",
    ("GET", "/school/classes"): "onboarding catalogue",
    ("GET", "/school/schools"): "onboarding catalogue",
    ("GET", "/school/schools/{school_id}"): "onboarding catalogue",
    ("GET", "/school/setup/catalog"): "onboarding catalogue",
    ("GET", "/school/setup/workspaces"): "onboarding catalogue",
    ("GET", "/school/subject-offerings"): "onboarding catalogue",
    ("GET", "/teaching/workspaces"): "scoped to the caller inside the handler",
    ("GET", "/teaching/scheme-of-work/{week_id}"): "syllabus weeks",
    ("GET", "/teaching/term-class-subjects/by-id/{term_class_subject_id}"): "syllabus",
    ("GET", "/teaching/term-class-subjects/{course_id}"): "syllabus",
    ("GET", "/assessments/exit-assessment/status"): "created and released flags only",
    ("GET", "/content/{content_id}/chats/{chat_id}/events"): "checked inside the handler",
    ("GET", "/content/files/{content_id}"): "a signed link that ends in minutes",
}


def _calls(dependant: Dependant) -> list[str]:
    names = [getattr(dependant.call, "__qualname__", "")]
    for child in dependant.dependencies:
        names += _calls(child)
    return names


def _guarded(route: APIRoute) -> bool:
    return any(
        name.startswith(("requires.", "get_actor", "require_", "actor_for"))
        for name in _calls(route.dependant)
    )


def test_no_route_is_open_by_accident() -> None:
    open_routes = {
        (method, route.path)
        for route in app.routes
        if isinstance(route, APIRoute) and not _guarded(route)
        for method in route.methods - {"HEAD", "OPTIONS"}
    }
    assert open_routes - OPEN_ON_PURPOSE.keys() == set()


def test_nothing_on_the_open_list_is_guarded_or_gone() -> None:
    guarded_or_absent = set(OPEN_ON_PURPOSE) - {
        (method, route.path)
        for route in app.routes
        if isinstance(route, APIRoute) and not _guarded(route)
        for method in route.methods
    }
    assert guarded_or_absent == set()
