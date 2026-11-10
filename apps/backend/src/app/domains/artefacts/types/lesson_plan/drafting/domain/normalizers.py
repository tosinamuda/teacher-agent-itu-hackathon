from __future__ import annotations

import re
from copy import deepcopy
from typing import cast

from app.shared.json_types import JsonObject, JsonValue
from app.shared.llm_markup import reader_ready

GroundedImage = dict[str, str]


#: An environment whose rows a ``\\hline`` separates.
_TABULAR_RE = re.compile(
    r"\\begin\{(array|matrix|pmatrix|bmatrix|Bmatrix|vmatrix|Vmatrix|aligned|cases)\}.*?\\end\{\1\}",
    flags=re.DOTALL,
)
#: A lone ``\`` (a control space) where a ``\\`` row break was meant: before ``\hline`` or the end.
_UNBROKEN_ROW_RE = re.compile(
    r"(?<!\\)\\(?!\\)\s*(?=\\hline|\\end\{(?:array|matrix|pmatrix|bmatrix|Bmatrix|vmatrix|Vmatrix"
    r"|aligned|cases)\})"
)
#: The LaTeX delimiters, not a ``\\`` line break followed by a bracket.
_DISPLAY_RE = re.compile(r"(?<!\\)\\\[(.*?)(?<!\\)\\\]", flags=re.DOTALL)
_INLINE_RE = re.compile(r"(?<!\\)\\\((.*?)(?<!\\)\\\)", flags=re.DOTALL)


def clean_latex(text: str) -> str:
    """A drafted field as a reader is shown it, its maths delimited the way plans keep it.

    The model's string goes through the one repair chain every reader-facing string does;
    then its display maths goes on lines of its own, where markdown reads it as a block.
    """
    if not text:
        return text
    text = reader_ready(text)
    text = _TABULAR_RE.sub(lambda match: _UNBROKEN_ROW_RE.sub(r"\\\\ ", match.group(0)), text)
    text = _DISPLAY_RE.sub(lambda match: f"\n$$\n{match.group(1).strip()}\n$$\n", text)
    text = _INLINE_RE.sub(lambda match: f"${match.group(1)}$", text)
    return re.sub(r"\n{3,}", "\n\n", text)


def collect_grounded_image_assets(evidence_bundle: list[JsonObject]) -> list[GroundedImage]:
    grounded_assets: list[GroundedImage] = []
    seen: set[tuple[str, str]] = set()

    for record in evidence_bundle:
        record_id = str(record.get("section_ref") or "").strip()
        source_html_path = str(record.get("source_html_path") or "").strip()
        source_anchor_id = str(record.get("source_anchor_id") or "").strip()
        raw_assets = record.get("asset_refs")
        asset_refs = raw_assets if isinstance(raw_assets, list) else []
        for raw_asset in asset_refs:
            if not isinstance(raw_asset, dict):
                continue
            asset = raw_asset
            if str(asset.get("asset_type") or "").strip() != "image":
                continue
            src = str(asset.get("src") or "").strip()
            if not src or not record_id:
                continue
            key = (record_id, src)
            if key in seen:
                continue
            seen.add(key)
            grounded_assets.append(
                {
                    "url": src,
                    "caption": str(asset.get("caption") or "").strip(),
                    "source_record_id": record_id,
                    "source_html_path": source_html_path,
                    "source_anchor_id": source_anchor_id,
                }
            )

    return grounded_assets


def build_grounded_figure_blocks(
    existing_blocks: list[JsonObject],
    *,
    grounded_images: list[GroundedImage],
    step_id: str,
) -> list[JsonObject]:
    """Build image ``VisualBlock``s for grounded source figures the draft didn't emit.

    The drafter reproduces source *tables* as LaTeX explanation blocks but rarely emits
    the source's image figures (counting charts, diagrams), so a step ends up telling the
    teacher to "project the counting chart" while no chart ever renders. We attach those
    grounded figures deterministically — no LLM — deduped against any image block the draft
    already carries (by url). Tables already shown as LaTeX are never duplicated here
    because ``collect_grounded_image_assets`` only yields ``asset_type == "image"`` assets,
    not the ``display_math`` the drafter renders inline.
    """
    existing_visuals = [
        block for block in existing_blocks if str(block.get("type") or "").strip() == "visual"
    ]
    existing_urls = {str(block.get("url") or "").strip() for block in existing_visuals}
    figures: list[JsonObject] = []
    # The dataset has no figure numbers, so we number the step's figures ourselves (in
    # placement order). The same numbering is fed to the writer, so its "Figure 1" prose
    # references line up with the captions shown here.
    figure_number = len(existing_visuals)
    for index, image in enumerate(grounded_images, start=1):
        url = str(image.get("url") or "").strip()
        record_id = str(image.get("source_record_id") or "").strip()
        if not url or not record_id or url in existing_urls:
            continue
        existing_urls.add(url)
        figure_number += 1
        source_caption = str(image.get("caption") or "").strip()
        label = f"Figure {figure_number}"
        caption = f"{label}: {source_caption}" if source_caption else label
        figures.append(
            {
                "id": f"{step_id}-figure-{index}",
                "type": "visual",
                "variant": "image",
                # "Figure N: <verbatim source caption>" — numbered + grounded, not LLM-invented.
                "caption": caption,
                "url": url,
                "source_record_id": record_id,
                "source_html_path": image.get("source_html_path") or None,
                "source_anchor_id": image.get("source_anchor_id") or None,
            }
        )
    return figures


class ContentBlockNormalizer:
    def __init__(self, *, grounded_images: list[GroundedImage] | None) -> None:
        self._grounded_images = grounded_images
        self._handlers = {
            "explanation": self._normalize_explanation,
            "worked_example": self._normalize_worked_example,
            "practice": self._normalize_practice,
            "visual": self._normalize_visual,
        }

    def normalize(self, block: JsonObject) -> JsonObject | None:
        block_type = str(block.get("type") or "").strip()
        handler = self._handlers.get(block_type)
        if handler is None:
            return block
        return handler(block)

    def _normalize_explanation(self, block: JsonObject) -> JsonObject:
        if isinstance(block.get("content"), str):
            block["content"] = clean_latex(str(block["content"]))
        return block

    def _normalize_worked_example(self, block: JsonObject) -> JsonObject:
        if isinstance(block.get("problem"), str):
            block["problem"] = clean_latex(str(block["problem"]))
        if isinstance(block.get("final_answer"), str):
            block["final_answer"] = clean_latex(str(block["final_answer"]))
        raw_steps = block.get("steps")
        if not isinstance(raw_steps, list):
            return block
        normalized_steps: list[JsonValue] = []
        for raw_step in raw_steps:
            if not isinstance(raw_step, dict):
                normalized_steps.append(raw_step)
                continue
            step_payload = raw_step
            if isinstance(step_payload.get("content"), str):
                step_payload["content"] = clean_latex(str(step_payload["content"]))
            normalized_steps.append(step_payload)
        block["steps"] = normalized_steps
        return block

    def _normalize_practice(self, block: JsonObject) -> JsonObject:
        if isinstance(block.get("question"), str):
            block["question"] = clean_latex(str(block["question"]))
        if isinstance(block.get("answer"), str):
            block["answer"] = clean_latex(str(block["answer"]))
        raw_hints = block.get("hints")
        if isinstance(raw_hints, list):
            block["hints"] = [
                clean_latex(hint) if isinstance(hint, str) else hint for hint in raw_hints
            ]
        return block

    def _normalize_visual(self, block: JsonObject) -> JsonObject | None:
        if isinstance(block.get("caption"), str):
            block["caption"] = clean_latex(str(block["caption"]))
        if str(block.get("variant") or "").strip() != "image":
            return block
        if self._grounded_images is None:
            return block
        current_url = str(block.get("url") or "").strip()
        matched_asset = next(
            (asset for asset in self._grounded_images if asset["url"] == current_url),
            None,
        )
        if matched_asset is None and self._grounded_images:
            matched_asset = self._grounded_images[0]
        if matched_asset is None:
            return None
        block["url"] = matched_asset["url"]
        block["source_record_id"] = matched_asset["source_record_id"]
        block["source_html_path"] = matched_asset["source_html_path"] or None
        block["source_anchor_id"] = matched_asset["source_anchor_id"] or None
        return block


def normalize_content_block(
    block: JsonObject,
    *,
    grounded_images: list[GroundedImage] | None,
) -> JsonObject | None:
    return ContentBlockNormalizer(grounded_images=grounded_images).normalize(block)


def _instructional_type_for(step_kind: str, block_types: set[str]) -> str | None:
    if step_kind == "core":
        if "worked_example" in block_types:
            return "explain_example_practice"
        if "practice" in block_types:
            return "explain_practice"
        return "explain_only"
    if step_kind == "evaluation":
        return "check"
    if step_kind == "intro":
        return None
    return None


def normalize_step_content(
    step: JsonObject,
    *,
    grounded_images: list[GroundedImage] | None,
) -> JsonObject:
    if isinstance(step.get("content"), str):
        step["content"] = clean_latex(str(step["content"]))

    blocks = step.get("blocks")
    if not isinstance(blocks, list):
        return step

    block_normalizer = ContentBlockNormalizer(grounded_images=grounded_images)
    normalized_blocks: list[JsonObject] = []
    for block in blocks:
        if not isinstance(block, dict):
            continue
        normalized = block_normalizer.normalize(block)
        if normalized is not None:
            normalized_blocks.append(normalized)

    # Embed grounded source figures the drafter referenced but never emitted as blocks.
    if grounded_images:
        normalized_blocks.extend(
            build_grounded_figure_blocks(
                normalized_blocks,
                grounded_images=grounded_images,
                step_id=str(step.get("step_id") or "step"),
            )
        )
    # Raw pre-validation blocks: build_grounded_figure_blocks needs list[JsonObject],
    # but the JSON slot is JsonValue — an always-safe upcast (every JsonObject is one).
    step["blocks"] = cast("list[JsonValue]", normalized_blocks)

    step_kind = str(step.get("step_kind") or "").strip()
    block_types = {str(block.get("type") or "").strip() for block in normalized_blocks}
    step["instructional_type"] = _instructional_type_for(step_kind, block_types)

    return step


_RETIRED_STEP_KEYS = ("teacher_activities", "student_activities", "mode")


def _with_activities_in_order(step: JsonObject) -> JsonObject:
    """A step stored before activities were one ordered list: the teacher's, then the students'.

    The two lists never recorded how they interleaved, so the order they were written in is all
    there is to keep. `mode` no longer exists and is dropped.
    """
    if "activities" not in step:
        step["activities"] = [
            {"who": who, "what": what}
            for who, key in (("teacher", "teacher_activities"), ("student", "student_activities"))
            for what in _texts(step.get(key))
        ]
    for key in _RETIRED_STEP_KEYS:
        step.pop(key, None)
    return step


def _texts(value: JsonValue) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]


def normalize_session_plan_payload(session_plan: JsonObject) -> JsonObject:
    normalized = deepcopy(session_plan)

    steps = normalized.get("steps")
    if isinstance(steps, list):
        normalized["steps"] = [
            normalize_step_content(_with_activities_in_order(step), grounded_images=None)
            if isinstance(step, dict)
            else step
            for step in steps
        ]

    return normalized
