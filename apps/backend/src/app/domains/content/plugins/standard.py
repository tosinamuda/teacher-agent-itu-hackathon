"""The Agent Plugins 1.0.0 schemas, and what a file that breaks them is reported as."""

from __future__ import annotations

import json
from functools import cache
from pathlib import Path

from jsonschema import Draft202012Validator

from app.domains.content.plugins.problems import Problem

VERSION = "1.0.0"
_SCHEMAS = Path(__file__).with_name("schemas")
PLUGIN_SCHEMA = f"https://agent-plugins.org/schemas/{VERSION}/plugin.schema.json"
MCP_SCHEMA = f"https://agent-plugins.org/schemas/{VERSION}/mcp.schema.json"


@cache
def _validator(name: str) -> Draft202012Validator:
    schema = json.loads((_SCHEMAS / f"{name}.schema.json").read_text(encoding="utf-8"))
    return Draft202012Validator(schema)


def breaks_the_standard(file: str, name: str, record: object) -> list[Problem]:
    """What the standard's schema ``name`` (``plugin`` or ``mcp``) says is wrong with ``record``."""
    found = sorted(_validator(name).iter_errors(record), key=lambda error: list(error.path))
    return [
        Problem(file, f"{'.'.join(str(step) for step in error.path) or 'file'}: {error.message}")
        for error in found
    ]
