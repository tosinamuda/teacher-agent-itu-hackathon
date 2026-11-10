"""Signed, short-lived links to a file of the app, for a client that cannot sign in to the web app.

A link names one piece of content and a time. It is signed with a secret only the server knows,
so nobody can make a link for content they were not given one for, or keep it past its time.
"""

from __future__ import annotations

import hashlib
import hmac
import os

SECRET_VARIABLE = "DOWNLOAD_LINK_SECRET"
LIFETIME_SECONDS = 15 * 60


def secret_from_environment() -> str | None:
    """The signing secret of this deploy; none where links are not set up."""
    return os.environ.get(SECRET_VARIABLE) or None


def _signature(secret: str, content_id: str, expires: int) -> str:
    return hmac.new(secret.encode(), f"{content_id}.{expires}".encode(), hashlib.sha256).hexdigest()


def issue(secret: str, content_id: str, now: float) -> tuple[int, str]:
    """The time a link to ``content_id`` ends, and its signature."""
    expires = int(now) + LIFETIME_SECONDS
    return expires, _signature(secret, content_id, expires)


def is_valid(secret: str | None, content_id: str, expires: int, signature: str, now: float) -> bool:
    """Whether the link was issued by this server for ``content_id`` and has not ended."""
    return (
        secret is not None
        and expires >= now
        and hmac.compare_digest(_signature(secret, content_id, expires), signature)
    )
