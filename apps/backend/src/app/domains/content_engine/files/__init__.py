"""The files each content type is made into, one tool of the app's MCP server each."""

from __future__ import annotations

from collections.abc import Mapping

from app.domains.content_engine.files.builder import FileBuilder
from app.domains.content_engine.files.slide_deck import build_slide_deck_file

#: Each builder by the name of the MCP tool a plugin lists to have its content made into a file.
BUILDERS: Mapping[str, FileBuilder] = {"build_slide_deck_file": build_slide_deck_file}
