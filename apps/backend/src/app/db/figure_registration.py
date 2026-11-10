"""Register every drawing written into stored content, from any session, at its flush.

The rule lives in the figures domain. It is loaded on the first flush rather than here,
because this module is loaded with the session, before any model may be.
"""

from __future__ import annotations

from sqlalchemy import event
from sqlalchemy.orm import Session, UOWTransaction


def _register(session: Session, _flush_context: UOWTransaction, _instances: object) -> None:
    from app.domains.figures.infrastructure.registration import register_drawings

    register_drawings(session)


def install() -> None:
    if not event.contains(Session, "before_flush", _register):
        event.listen(Session, "before_flush", _register)
