"""The four sequencing strategies. Each returns (assembled_step, llm_text, referenced_ids)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

import dspy
from pydantic import BaseModel

from app.shared.json_types import JsonObject
from experiments.sequencing_bakeoff.manifest import Asset, manifest_text, resolve

_OBJECTIVE = "Explain the concept of a million using the powers-of-ten table and counting charts."
_GRADE = "JSS1"
_MARKER = re.compile(r"\{\{asset:([^}]+)\}\}")


@dataclass
class Variant:
    key: str
    label: str
    step: JsonObject
    llm_text: str
    referenced_ids: list[str]


def _prose_block(step_id: str, index: int, text: str) -> JsonObject:
    return {"id": f"{step_id}-p{index}", "type": "explanation", "content": text}


def _missing_block(ref_id: str) -> JsonObject:
    return {
        "id": f"missing-{ref_id}",
        "type": "explanation",
        "content": f"*[unresolved asset: {ref_id}]*",
    }


# ---- V1: inline markers --------------------------------------------------------------


class WriteProseWithMarkers(dspy.Signature):
    """Write the teacher explanation for the lesson step as ONE markdown string.

    Where a source table or figure should appear in the flow, insert a marker EXACTLY like
    {{asset:REF_ID}} on its own line, using only ref_ids from the asset manifest. DO NOT
    reproduce any table, array, equation, or image yourself — each marker is replaced with
    the verbatim source. Place every manifest asset where it best supports the explanation.
    Each figure's caption is given in the manifest; refer to figures generally and do NOT
    state contents of a figure (numbers, ranges) beyond what its caption supports."""

    objective: str = dspy.InputField()
    grade: str = dspy.InputField()
    asset_manifest: str = dspy.InputField(
        desc="One `ref_id — caption` line per asset (the figure's real caption)."
    )
    markdown: str = dspy.OutputField(desc="Teacher prose with {{asset:REF_ID}} markers.")


def generate_markers(
    assets: list[Asset], *, objective: str = _OBJECTIVE, grade: str = _GRADE
) -> Variant:
    prediction = dspy.Predict(WriteProseWithMarkers)(
        objective=objective, grade=grade, asset_manifest=manifest_text(assets)
    )
    markdown = str(prediction.markdown)
    parts = _MARKER.split(markdown)
    blocks: list[JsonObject] = []
    referenced: list[str] = []
    for index, part in enumerate(parts):
        if index % 2 == 0:
            text = part.strip()
            if text:
                blocks.append(_prose_block("v1", index, text))
        else:
            ref_id = part.strip()
            referenced.append(ref_id)
            blocks.append(resolve(ref_id, assets) or _missing_block(ref_id))
    step: JsonObject = {"step_id": "v1", "title": "Understanding millions", "blocks": blocks}
    return Variant("markers", "V1 MARKERS", step, markdown, referenced)


# ---- V2: ordered block list ----------------------------------------------------------


class ProseOrRef(BaseModel):
    kind: Literal["prose", "ref"]
    text: str = ""
    ref_id: str = ""


class WriteProseBlocks(dspy.Signature):
    """Compose the lesson step as an ORDERED list of blocks for the best teaching flow.

    Each block is EITHER a prose block you write (kind="prose", text=...) OR a reference to a
    source asset (kind="ref", ref_id=... from the manifest). Use ref_ids only from the
    manifest; DO NOT reproduce tables/figures yourself. Include every manifest asset once,
    ordered where it best supports the explanation. Each figure's caption is given in the
    manifest; refer to figures generally and do NOT state contents of a figure (numbers,
    ranges) beyond what its caption supports."""

    objective: str = dspy.InputField()
    grade: str = dspy.InputField()
    asset_manifest: str = dspy.InputField(desc="One `ref_id — description` line per asset.")
    blocks: list[ProseOrRef] = dspy.OutputField(desc="Ordered prose/ref blocks.")


def generate_blocklist(
    assets: list[Asset], *, objective: str = _OBJECTIVE, grade: str = _GRADE
) -> Variant:
    prediction = dspy.Predict(WriteProseBlocks)(
        objective=objective, grade=grade, asset_manifest=manifest_text(assets)
    )
    blocks: list[JsonObject] = []
    referenced: list[str] = []
    llm_text_parts: list[str] = []
    for index, item in enumerate(prediction.blocks):
        if item.kind == "prose" and item.text.strip():
            blocks.append(_prose_block("v2", index, item.text.strip()))
            llm_text_parts.append(item.text.strip())
        elif item.kind == "ref":
            ref_id = item.ref_id.strip()
            referenced.append(ref_id)
            blocks.append(resolve(ref_id, assets) or _missing_block(ref_id))
    step: JsonObject = {"step_id": "v2", "title": "Understanding millions", "blocks": blocks}
    return Variant("blocklist", "V2 BLOCKLIST", step, "\n".join(llm_text_parts), referenced)


# ---- V3: prose only, assets appended -------------------------------------------------


class WriteProseOnly(dspy.Signature):
    """Write ONLY the teacher explanation prose for the step. The source table and figures
    are spliced in automatically AFTER your text — DO NOT reproduce any table, array,
    equation, or image. Refer to them in words (e.g. "the table below"). Each figure's caption
    is listed; refer to figures generally and do NOT state contents of a figure (numbers,
    ranges) beyond what its caption supports."""

    objective: str = dspy.InputField()
    grade: str = dspy.InputField()
    available_assets: str = dspy.InputField(
        desc="The assets spliced after your prose, with each figure's real caption."
    )
    explanation_markdown: str = dspy.OutputField(desc="Teacher prose only; no reproduced assets.")


def generate_append(
    assets: list[Asset], *, objective: str = _OBJECTIVE, grade: str = _GRADE
) -> Variant:
    prediction = dspy.Predict(WriteProseOnly)(
        objective=objective, grade=grade, available_assets=manifest_text(assets)
    )
    prose = str(prediction.explanation_markdown)
    blocks: list[JsonObject] = [_prose_block("v3", 0, prose)]
    blocks.extend(dict(asset.block) for asset in assets)  # fixed append, manifest order
    step: JsonObject = {"step_id": "v3", "title": "Understanding millions", "blocks": blocks}
    return Variant("append", "V3 APPEND", step, prose, [])  # no LLM-chosen placement


# ---- V0: regenerate everything (the no-transclusion baseline) -------------------------


class WriteFullStep(dspy.Signature):
    """Write the COMPLETE teacher explanation for the lesson step as ONE markdown string.

    Reproduce any source table yourself as a LaTeX array ($$\\begin{array}...$$) and describe
    the figures inline, exactly as a teacher's self-contained notes would — do not assume any
    asset is inserted for you. Each figure's caption is provided; describe a figure ONLY using
    its caption and do NOT state contents (numbers, ranges) beyond what the caption supports."""

    objective: str = dspy.InputField()
    grade: str = dspy.InputField()
    available_assets: str = dspy.InputField(desc="The source table/figures to reproduce inline.")
    explanation_markdown: str = dspy.OutputField(desc="Complete self-contained teacher notes.")


def generate_regenerate(
    assets: list[Asset], *, objective: str = _OBJECTIVE, grade: str = _GRADE
) -> Variant:
    """Matched-input baseline: the LLM writes the whole step incl. reproducing the table."""
    prediction = dspy.Predict(WriteFullStep)(
        objective=objective, grade=grade, available_assets=manifest_text(assets)
    )
    markdown = str(prediction.explanation_markdown)
    step: JsonObject = {
        "step_id": "v0",
        "title": "Lesson step",
        "blocks": [{"id": "v0-exp", "type": "explanation", "content": markdown}],
    }
    return Variant("regenerate", "V0 REGENERATE", step, markdown, [])


def variant_regenerate(stored_step: JsonObject) -> Variant:
    """The stored production step — the LLM wrote everything, including the table."""
    from experiments.content_repair.validators import block_list

    llm_text = "".join(str(b.get("content") or "") for b in block_list(stored_step))
    return Variant("regenerate", "V0 REGENERATE", stored_step, llm_text, [])
