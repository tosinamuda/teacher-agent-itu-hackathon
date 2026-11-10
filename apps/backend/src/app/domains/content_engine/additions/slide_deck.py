"""The cover of a slide deck: the lesson's own title and objectives, set by the app, not written."""

from __future__ import annotations

from app.shared.json_types import JsonObject, JsonValue
from app.shared.session_plan_view import SessionPlanView


def slide_deck_cover(plan: SessionPlanView | None) -> JsonObject:
    """What a deck saves beside its slides: ``cover`` with title, subtitle and objectives.

    The deck is for one lesson, so its title is the lesson's: the plan's own, else its subtopic,
    else its topic. The topic stays in the subtitle when the title is narrower than it.
    """
    if plan is None or not (title := plan.title or plan.subtopic or plan.topic):
        return {}
    subtitle = " · ".join(
        part
        for part in (plan.subject, plan.grade, plan.topic)
        if part and part.casefold() != title.casefold()
    )
    objectives: list[JsonValue] = [
        objective.objective_text
        for objective in plan.lesson_plan_objectives
        if objective.objective_text
    ]
    return {"cover": {"title": title, "subtitle": subtitle, "objectives": objectives}}
