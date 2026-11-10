"""Guard every session: a flush that would change a concluded lesson's record is refused.

The rule and its models live in ``concluded_record``. It is loaded on the first flush rather
than here, because this module is loaded with the session, before any model may be.
"""

from __future__ import annotations

from sqlalchemy import event
from sqlalchemy.orm import Session, UOWTransaction


def _refuse_changes_to_concluded_lessons(
    session: Session, _flush_context: UOWTransaction, _instances: object
) -> None:
    from app.db.concluded_record import refuse_changes_to_concluded_lessons

    refuse_changes_to_concluded_lessons(session)


def install() -> None:
    """Guard every session, sync or async, from here on."""
    if not event.contains(Session, "before_flush", _refuse_changes_to_concluded_lessons):
        event.listen(Session, "before_flush", _refuse_changes_to_concluded_lessons)
