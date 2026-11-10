"""Shared base classes and reusable field types for Pydantic API contracts.

``StrictRequest`` is the base for **API request bodies**: it forbids unknown
keys (``extra="forbid"``) so clients get a 422 instead of silently-dropped
fields, and strips surrounding whitespace from string inputs. Response models
should keep inheriting ``BaseModel`` directly, and type a moment as ``UtcDatetime``.
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, Field

from app.shared.time import as_utc


class StrictRequest(BaseModel):
    """Base for inbound API request bodies — rejects unknown keys."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


# A 1-5 Likert rating (e.g. rubric / section scores).
LikertScore = Annotated[int, Field(ge=1, le=5)]

# A 0-2 audit rubric score (source-grounding audit).
AuditScore = Annotated[int, Field(ge=0, le=2)]

# A moment sent with its UTC offset: without one, a browser reads the time as its own local time.
UtcDatetime = Annotated[datetime, AfterValidator(as_utc)]
