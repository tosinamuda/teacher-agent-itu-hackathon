"""CORS origin-pattern behaviour.

Starlette's CORSMiddleware tests an Origin header against ``allow_origin_regex``
with ``re.fullmatch``, so these tests apply the built regex the same way to
prove wildcard patterns allow what they should (incl. Cloudflare Pages preview
deploys) and reject look-alike origins.
"""

from __future__ import annotations

import re

from app.cors import (
    build_cors_origin_regex,
    origin_pattern_to_regex,
    parse_origin_patterns,
)


def _allows(raw_origins: str, origin: str) -> bool:
    """Mirror Starlette: an origin is allowed iff the built regex fullmatches it."""
    return re.compile(build_cors_origin_regex(raw_origins)).fullmatch(origin) is not None


def test_parse_splits_on_commas_and_whitespace() -> None:
    assert parse_origin_patterns("") == []
    assert parse_origin_patterns("   ") == []
    assert parse_origin_patterns("https://a.com, https://b.com") == [
        "https://a.com",
        "https://b.com",
    ]
    # Newlines/tabs/spaces are all valid separators.
    assert parse_origin_patterns("https://a.com\n https://b.com\thttps://c.com") == [
        "https://a.com",
        "https://b.com",
        "https://c.com",
    ]


def test_pattern_to_regex_wildcard_and_scheme() -> None:
    # `*` -> one or more non-slash chars; scheme is kept when present.
    assert origin_pattern_to_regex("https://*.b.com") == r"https://[^/]+\.b\.com"
    # Scheme-less patterns match both http and https.
    assert origin_pattern_to_regex("*.b.com") == r"https?://[^/]+\.b\.com"
    assert origin_pattern_to_regex("localhost:*") == r"https?://localhost:[^/]+"


def test_localhost_is_always_allowed_without_config() -> None:
    assert _allows("", "http://localhost:5173")
    assert _allows("", "http://localhost:3000")
    assert _allows("", "http://127.0.0.1:8000")
    # Nothing else is allowed when unconfigured.
    assert not _allows("", "https://app.example.com")


def test_subdomain_wildcard_allows_pages_previews() -> None:
    raw = "https://example.pages.dev, https://*.example.pages.dev"
    assert _allows(raw, "https://example.pages.dev")  # apex (explicit)
    assert _allows(raw, "https://a1b2c3d4.example.pages.dev")  # commit preview
    assert _allows(raw, "https://feat-mobile.example.pages.dev")  # branch alias


def test_multiple_patterns_and_ports() -> None:
    raw = "https://app.example.com, localhost:8080, https://*.preview.example.com"
    assert _allows(raw, "https://app.example.com")
    assert _allows(raw, "http://localhost:8080")  # scheme-less -> http ok
    assert _allows(raw, "https://localhost:8080")  # scheme-less -> https ok too
    assert _allows(raw, "https://x.preview.example.com")
    assert not _allows(raw, "https://app.example.com.evil.com")


def test_look_alike_origins_are_rejected() -> None:
    raw = "https://*.example.com"
    # Suffix attack — our host is only a prefix of the real origin host.
    assert not _allows(raw, "https://x.example.com.evil.com")
    # The bare apex has no leading label, so the subdomain wildcard misses it.
    assert not _allows(raw, "https://example.com")
    # Unrelated origin.
    assert not _allows(raw, "https://attacker.example.org")
