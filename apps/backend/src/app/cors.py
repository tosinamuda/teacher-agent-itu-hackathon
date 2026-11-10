"""CORS origin matching.

Which browser origins may call the API is configured entirely from one env var,
``CORS_ALLOWED_ORIGINS`` — nothing project-specific is baked into this code. The
value is a list of origin *patterns* separated by commas or whitespace (neither
can appear in an origin, so they never clash with the values). Each pattern is
either an exact origin or uses ``*`` as a wildcard:

    https://app.example.com          one exact origin
    https://*.example.com            every subdomain (e.g. Cloudflare Pages previews)
    http://localhost:*               any localhost port
    *.example.com                    scheme-less -> matches http and https

``*`` expands to ``[^/]+`` (one or more non-slash characters: a port, a label,
or several dotted labels) and never crosses a ``/``, so a wildcard can't reach
into a path. A pattern without a scheme matches both http and https.

Patterns compile to a single regex handed to Starlette's ``CORSMiddleware``,
which matches the Origin header with ``re.fullmatch`` — so the anchored trailing
segment defeats suffix attacks (``https://*.example.com`` never matches
``https://x.example.com.evil.com``). Localhost on any port is always allowed so
local development needs no configuration.
"""

from __future__ import annotations

import re

# Always-on so local dev never needs CORS configuration.
_BUILTIN_DEV_ORIGINS: tuple[str, ...] = (r"http://localhost:\d+", r"http://127\.0\.0\.1:\d+")

# An origin can't contain a comma or whitespace, so either safely separates
# patterns in the env value.
_SEPARATOR = re.compile(r"[,\s]+")


def parse_origin_patterns(raw: str) -> list[str]:
    """Split a comma/whitespace-separated env value into trimmed patterns."""
    return [pattern for pattern in _SEPARATOR.split(raw.strip()) if pattern]


def origin_pattern_to_regex(pattern: str) -> str:
    """Translate one origin pattern into a regex.

    Everything is escaped literally except ``*``, which becomes ``[^/]+``. A
    pattern without an explicit ``scheme://`` is treated as a host[:port] and
    matched against both http and https.
    """
    pattern = pattern.strip()
    body = re.escape(pattern).replace(r"\*", r"[^/]+")
    return body if "://" in pattern else rf"https?://{body}"


def build_cors_origin_regex(raw_origins: str) -> str:
    """Build the ``allow_origin_regex`` from the configured patterns.

    Always includes the localhost dev origins, then one alternative per
    configured pattern. Each alternative is parenthesised so the ``|`` is
    unambiguous under ``re.fullmatch`` (how Starlette tests origins).
    """
    alternatives = [
        *_BUILTIN_DEV_ORIGINS,
        *(origin_pattern_to_regex(pattern) for pattern in parse_origin_patterns(raw_origins)),
    ]
    return "|".join(f"({alternative})" for alternative in alternatives)
