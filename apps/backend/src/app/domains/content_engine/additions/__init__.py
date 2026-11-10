"""What each content type's plugin adds to its content when it is saved.

Each adder is one tool of the app's MCP server.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping

from app.domains.content_engine.additions.slide_deck import slide_deck_cover
from app.shared.json_types import JsonObject
from app.shared.session_plan_view import SessionPlanView

#: Reads the lesson's plan, when the draft has one, and answers the fields to add.
Adder = Callable[[SessionPlanView | None], JsonObject]

#: Each adder by the name of the MCP tool a plugin lists to have its content finished with it.
ADDERS: Mapping[str, Adder] = {"slide_deck_cover": slide_deck_cover}
