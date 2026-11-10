"""A part the content engine wrote for one lesson objective, as the pipeline's draft of a section.

The pipeline stores a section as an explanation, worked examples and practice. The engine
writes a title, an explanation, drawings, worked examples with their working, and practice. A
drawing stays in the explanation as the TikZ it is, because a later revision rebuilds a
section from its prose blocks and drops anything that is not.
"""

from __future__ import annotations

from app.shared.json_types import JsonObject, JsonValue

from .assembly import AuthoredBlock
from .schemas import MISCONCEPTION_LABEL, DraftBlock, DraftPractice, DraftSection


def _text(value: JsonValue | None) -> str:
    return str(value).strip() if value is not None else ""


def _records(value: JsonValue | None) -> list[JsonObject]:
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def _figure(figure: JsonObject) -> str:
    """A drawing as TikZ, then its caption in italics when it has one."""
    caption = _text(figure.get("caption"))
    return "\n\n".join(
        piece
        for piece in (_text(figure.get("drawing")), f"*{caption}*" if caption else "")
        if piece
    )


def _explanation(part: JsonObject) -> str:
    drawings = [_figure(figure) for figure in _records(part.get("figures"))]
    return "\n\n".join(block for block in (_text(part.get("explanation")), *drawings) if block)


def _example(example: JsonObject) -> DraftBlock:
    working = [
        f"- {_text(line.get('working'))} — {_text(line.get('commentary'))}"
        for line in _records(example.get("solution"))
    ]
    text = "\n\n".join(
        (
            _text(example.get("problem")),
            "**Solution**",
            "\n".join(working),
            f"**Answer:** {_text(example.get('answer'))}",
        )
    )
    return DraftBlock(block_type="worked_example", text=text)


def draft_from_part(part: JsonObject) -> DraftSection:
    """The section the engine's part for an objective describes."""
    return DraftSection(
        title=_text(part.get("title")),
        instructional_support=_explanation(part),
        worked_examples=[_example(example) for example in _records(part.get("worked_examples"))],
        practice=[
            DraftPractice(
                prompt=_text(item.get("question")),
                answer=_text(item.get("answer")),
                worked_solution=_text(item.get("worked_solution")) or None,
            )
            for item in _records(part.get("practice"))
        ],
    )


def _practice(part: JsonObject) -> list[DraftPractice]:
    return [
        DraftPractice(
            prompt=_text(item.get("question")),
            answer=_text(item.get("answer")),
            worked_solution=_text(item.get("worked_solution")) or None,
        )
        for item in _records(part.get("practice"))
    ]


def learner_blocks_from_part(part: JsonObject) -> list[AuthoredBlock]:
    """The prose blocks of a learner's section: explanation, misconception repair, examples."""
    draft = draft_from_part(part)
    blocks = [AuthoredBlock("explanation", draft.instructional_support)]
    repair = _text(part.get("misconception_repair"))
    if repair:
        blocks.append(AuthoredBlock("misconception_repair", MISCONCEPTION_LABEL + repair))
    blocks.extend(AuthoredBlock(block.block_type, block.text) for block in draft.worked_examples)
    return [block for block in blocks if block.text.strip()]


def learner_practice_from_part(part: JsonObject) -> list[DraftPractice]:
    """The practice of a learner's section."""
    return _practice(part)
