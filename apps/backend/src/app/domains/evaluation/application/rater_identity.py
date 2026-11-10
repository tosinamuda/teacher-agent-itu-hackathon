"""Named rater-identity queries and registration commands."""

from __future__ import annotations

import uuid

from app.domains.evaluation.application.errors import EvaluationApplicationError
from app.domains.evaluation.application.identity_ports import (
    RaterIdentities,
    RaterIdentityReader,
    RaterRegistrationStore,
)
from app.domains.evaluation.domain.records import RaterIdentity
from app.shared.ids import PublicIdPrefix, new_public_id
from app.shared.time import utc_now


class RaterIdentityConflictError(Exception):
    """A concurrent registration won the unique display-name key."""


async def rater_for_actor(
    reader: RaterIdentityReader,
    *,
    actor_user_id: uuid.UUID | None,
) -> RaterIdentity:
    """Resolve only the authenticated actor's linked rater identity."""
    if actor_user_id is None:
        raise EvaluationApplicationError(401, "not_authenticated")
    rater = await reader.rater_identity_for_user(user_id=actor_user_id)
    if rater is None:
        raise EvaluationApplicationError(403, "no_rater_identity_bound_to_this_user")
    return rater


async def ensure_synthetic_rater(
    store: RaterRegistrationStore,
    *,
    display_name: str,
) -> RaterIdentity:
    """Get or atomically register one synthetic persona identity."""
    normalized = _normalized_name(display_name)
    existing = await store.rater_identities.rater_identity_by_name(display_name=normalized)
    if existing is not None:
        return existing
    try:
        identity = await stage_rater_identity(store.rater_identities, display_name=normalized)
        await store.commit()
        return identity
    except RaterIdentityConflictError:
        await store.rollback()
        winner = await store.rater_identities.rater_identity_by_name(display_name=normalized)
        if winner is None:
            raise
        return winner


async def stage_rater_identity(
    persistence: RaterIdentities,
    *,
    display_name: str,
) -> RaterIdentity:
    """Resolve or stage an identity without committing the caller's transaction."""
    normalized = _normalized_name(display_name)
    existing = await persistence.rater_identity_by_name(display_name=normalized)
    if existing is not None:
        return existing
    now = utc_now()
    return await persistence.stage_rater_identity(
        RaterIdentity(
            id=uuid.uuid4(),
            rater_id=new_public_id(PublicIdPrefix.EVALUATION_RATER),
            display_name=normalized,
            user_id=None,
            created_at=now,
            updated_at=now,
        )
    )


def _normalized_name(display_name: str) -> str:
    normalized = display_name.strip()
    if len(normalized) < 2:
        raise EvaluationApplicationError(422, "rater_name_too_short")
    return normalized
