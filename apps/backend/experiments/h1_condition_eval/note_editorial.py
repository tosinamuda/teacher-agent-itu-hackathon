"""Generation-facing notes: the frozen transcription with review commentary removed.

The transcription's figure captions do two jobs at once — they describe a drawing
the model cannot see (which it needs) and they record review findings about what
the drawing fails to label (which it must never read). The second kind reaches the
generator, gets paraphrased into learner text, and costs repair passes: 5 of 12
critic findings in round 8 were spent removing it.

The cleaned notes are FILES, edited by hand and reviewable as a diff against the
frozen source. Nothing here decides what is editorial; that judgement lives in the
files themselves, where it can be read.

    uv run python -m experiments.h1_condition_eval.note_editorial export    # seed
    uv run python -m experiments.h1_condition_eval.note_editorial diff      # review
    uv run python -m experiments.h1_condition_eval.note_editorial verify    # nothing lost
    uv run python -m experiments.h1_condition_eval.note_editorial declare   # nothing added
    uv run python -m experiments.h1_condition_eval.note_editorial audit     # ids still line up
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
from pathlib import Path

from experiments.h1_condition_eval.dataset import EVAL_SET_PATH

CLEAN_DIR = Path(__file__).parent / "notes-clean"

# Curriculum mapping carried in step titles, which ship to the model on the evidence
# item and as its citable label. Mechanical, so it is stripped here rather than by
# hand. Both spellings occur, and the tag itself may contain brackets:
# "*(core → objective 1)*" and "*(objective (i))*".
TITLE_TAG = re.compile(r"\s*\*\(.*?objective.*\)\*\s*$", re.IGNORECASE)


def _frozen() -> list[dict]:
    """The eval set with each note read as the TRANSCRIPTION wrote it.

    Everything here compares the generation copy against what she was transcribed as
    writing, so the baseline has to survive a re-freeze. Once ``eval_set.json`` is frozen
    from the documents, ``note`` is the generation copy and comparing against it would
    compare a file with itself — 39 visible additions become 0 and every declaration goes
    quiet. ``note_frozen`` is the transcription, carried forward for exactly this.
    """
    cases: list[dict] = json.loads(EVAL_SET_PATH.read_text())["cases"]
    for case in cases:
        for step in case["plan"]["steps"]:
            if step.get("note_frozen"):
                step["note"] = step["note_frozen"]
    return cases


def note_path(lesson: str, step_id: str) -> Path:
    return CLEAN_DIR / lesson / f"{step_id}.md"


#: What each ``--note-source`` actually is, spelled out. "clean" badly understates the
#: second one — it is not tidied prose, it is a corrected and research-enhanced corpus —
#: and the flag cannot be renamed without invalidating every recorded fingerprint. So the
#: word stays and the meaning gets printed beside it, everywhere a run or a rating is
#: reported.
NOTE_SOURCES = {
    "raw": (
        "RAW — the frozen transcription, UNCORRECTED. Review commentary still in the "
        "prose, figures as first drawn, drawings unlabelled. Not what the study intends "
        "a condition to read."
    ),
    "clean": (
        "CLEAN — notes-clean/, hand-corrected and research-enhanced: review commentary "
        "removed, every drawing labelled and captioned, figures redrawn where they "
        "contradicted the method, procedures completed. Each edit declared in "
        "note_editorial.DECLARED_ADDITIONS."
    ),
}


def describe_note_source(source: str) -> str:
    """The note source in words, for anything a person reads.

    Both judged runs recorded ``raw`` and nothing said so where anyone would look — the
    fingerprint holds it as a SHA-256, which is unreadable by design. A number measured
    on the uncorrected transcription must say so on its face.
    """
    return NOTE_SOURCES.get(source, f"UNKNOWN note source {source!r}")


def export() -> int:
    """Seed the editable copies. Never overwrites — hand edits are the point."""
    written = skipped = 0
    for case in _frozen():
        for step in case["plan"]["steps"]:
            if not step.get("note"):
                continue
            path = note_path(case["lesson"], step["step_id"])
            if path.exists():
                skipped += 1
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(step["note"], encoding="utf-8")
            written += 1
    print(f"wrote {written} note files, kept {skipped} already edited -> {CLEAN_DIR}")
    return 0


def clean_plan(plan: dict) -> tuple[dict, list[str]]:
    """The plan with each note replaced by its edited file.

    A missing file is an error, not a silent fall-through to the raw note: an arm
    that claims to be cleaned must be cleaned everywhere.
    """
    lesson = plan.get("lesson_key") or plan.get("lesson") or ""
    log: list[str] = []
    steps = []
    for step in plan.get("steps") or []:
        step = dict(step)
        title = TITLE_TAG.sub("", step.get("title") or "")
        if title != (step.get("title") or ""):
            log.append(f"{step['step_id']}: dropped curriculum tag from title")
            step["title"] = title
        if step.get("note"):
            path = note_path(lesson, step["step_id"])
            if not path.exists():
                raise SystemExit(
                    f"{lesson}/{step['step_id']}: no cleaned note at {path}. "
                    f"Run `python -m experiments.h1_condition_eval.note_editorial export` first."
                )
            edited = path.read_text(encoding="utf-8")
            if edited != step["note"]:
                removed = len(step["note"]) - len(edited)
                log.append(f"{step['step_id']}: {removed:+d} chars")
            step["note"] = edited
        steps.append(step)
    return {**plan, "steps": steps}, log


# Her document splits into steps by script, and the hand-edited files are seeded from
# that split — so anything the split drops was never available to edit. These are the
# paragraph kinds a note is not expected to carry: structure, the cleaner's own
# remarks, and classroom choreography addressed to the teacher.
TRANSCRIPT = Path.home() / "Documents/Unilag/Masters/Thesis"
# STRUCTURAL — the paragraph says what it is, so this cannot be wrong.
# A blockquote is the transcription's convention for a remark about the document;
# a heading is structure; "**Objective:**" is a labelled field.
MARKED = re.compile(r"^(?:#{1,6}\s|>\s|\*\*Objective:\*\*)")

# SEMANTIC — a guess at what prose means, and only sound while the convention above
# is followed. 44 of the 56 editorial paragraphs in the transcripts are already
# blockquoted; the 12 that are not are why this exists, 11 of them in `t3-w06`.
# Every paragraph that needs this instead of MARKED is reported, so the guessing
# is countable and can be driven to zero by marking the source.
GUESSED = re.compile(r"^(?:Teacher\s|\*\*(?:Derived|Researcher)\b)")


# Paragraphs reviewed by hand and confirmed to be about the DOCUMENT rather than the
# mathematics. Listed one by one, with the reason, rather than widening the pattern
# above until nothing is reported.
REVIEWED_NOT_TEACHING = {
    # t3-w02, directly under "## Presentation" — the cleaner describing the layout.
    "The note is organised under the step that teaches it: each core step carries its "
    "own explanation, worked examples and practice, and each maps to exactly one objective.",
}


def _paragraphs(text: str) -> list[str]:
    """Whitespace-collapsed paragraphs, so line wrapping cannot hide a difference."""
    return [" ".join(block.split()) for block in re.split(r"\n\s*\n", text) if block.strip()]


def _cleaned_source(lesson: str) -> Path | None:
    for candidate in (
        TRANSCRIPT / f"Dataset/private/study-record/transcripts/{lesson}/teacher-cleaned.md",
        TRANSCRIPT / f"Supplements/{lesson}/teacher-supplement.md",
    ):
        if candidate.exists():
            return candidate
    return None


# A paragraph opening "Teacher ..." is classroom choreography and is not carried into
# a note. That is the one rule here that can HIDE content rather than report it, so
# any such paragraph that also looks mathematical is listed for a human every run.
# The others fail loud; this one has to be looked at.
LOOKS_MATHEMATICAL = re.compile(r"[0-9]|\$|=|\\frac|\bcm\b|formula|equal|angle|propert", re.I)


def verify() -> int:
    """Every teaching paragraph of her document reaches some note file.

    The split is the one step still done by script. This does not trust it: it
    reads her cleaned document and reports any paragraph that is neither a
    heading, a cleaner's remark, choreography, nor present in a note.
    """
    missing_total = 0
    review: list[str] = []
    structural = guessed = 0
    for case in _frozen():
        lesson = case["lesson"]
        source = _cleaned_source(lesson)
        if source is None:
            print(f"  {lesson}: no cleaned source on disk — cannot verify")
            continue
        text = source.read_text(encoding="utf-8")
        stripped = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.DOTALL)
        parts = re.split(r"\n## (?:Presentation|Evaluation)\b", stripped)
        presentation = parts[1] if len(parts) > 1 else stripped
        carried = " ".join(
            " ".join((step.get("note") or "").split()) for step in case["plan"]["steps"]
        )
        missing = [
            para
            for para in _paragraphs(presentation)
            if not MARKED.match(para)
            and not GUESSED.match(para)
            and para not in REVIEWED_NOT_TEACHING
            and para not in carried
        ]
        paragraphs = _paragraphs(presentation)
        structural += sum(1 for para in paragraphs if MARKED.match(para))
        guessed += sum(1 for para in paragraphs if not MARKED.match(para) and GUESSED.match(para))
        review += [
            f"{lesson}: {para}"
            for para in _paragraphs(presentation)
            if para.startswith("Teacher ")
            and LOOKS_MATHEMATICAL.search(para)
            and para not in carried
        ]
        missing_total += len(missing)
        print(f"  {lesson}: {len(missing)} teaching paragraphs not carried into any note")
        for para in missing[:5]:
            print(f"      · {para[:100]}")
    print(f"\n{missing_total} unaccounted")
    print(
        f"{structural} paragraphs classified STRUCTURALLY (blockquote, heading, field) — "
        f"cannot be wrong.\n{guessed} classified by GUESSING at prose — sound only while "
        f"the transcripts mark their commentary. Mark those in the source and this "
        f"reaches zero."
    )
    if review:
        print(
            f"\n{len(review)} choreography paragraphs mention mathematics and are NOT carried.\n"
            "Skipping these is the only rule here that can hide content — read them:"
        )
        for line in review:
            print(f"      · {line[:118]}")
    return 1 if missing_total else 0


def additions(frozen: str, clean: str) -> list[str]:
    """Paragraphs the generation copy has that the frozen transcription does not.

    Cleaning removes. An addition is therefore an edit, and the one direction that
    can put text in front of the model that no teacher wrote.
    """
    was = _paragraphs(frozen)
    now = _paragraphs(clean)
    opcodes = difflib.SequenceMatcher(None, was, now).get_opcodes()
    return [
        para
        for tag, _, _, start, end in opcodes
        if tag in ("insert", "replace")
        for para in now[start:end]
    ]


def addition_digest(frozen: str, clean: str) -> str:
    joined = "\n".join(additions(frozen, clean))
    return hashlib.sha256(joined.encode()).hexdigest()[:12] if joined else ""


# Every edit that puts words in front of the model, declared one by one.
#
# The previous guard was a list of phrases already seen in the tree. It passed with
# four copies of an agent's caption commentary present, because the wording was new —
# a blocklist can only recognise what has already leaked. A digest over the added
# paragraphs is blind to wording: any addition, in any phrasing, fails by name.
#
#     uv run python -m experiments.h1_condition_eval.note_editorial declare
DECLARED_ADDITIONS: dict[tuple[str, str], tuple[str, str]] = {
    # t3-w05 needs no declaration. Its entry here patched a gap in the AUTHORED
    # supplement, whose note was extracted from Siyavula 13.6; her own week-5 pages were
    # captured in 2026-08 and write the prism formula out in full, so the generation copy
    # is the note unedited.
    #
    # The four entries below are one edit made across four files: every drawing in the
    # corpus can now be named. `**fig-NN.**` labels let a pack refer to a figure, and 21
    # of the 38 drawings had none, all of them on these two lessons.
    ("t3-w02", "step-t3w02-02"): (
        "1c9cb46866df",
        "fig-01 to fig-03: labels prepended to descriptions each drawing already "
        "carried, so a pack can refer to them. Plus fig-03's parallelogram CORRECTED: "
        "it said a double arrow on the horizontals and a single on the slanted sides, "
        "and the drawing is the other way round — one arrowhead on each horizontal, two "
        "on each slanted side. The arrows are what mark which pair is parallel to which, "
        "so inverted they told the model the wrong thing about a figure it cannot see. "
        "Pre-existing, and it survived the caption pass on this lesson.",
    ),
    ("t3-w02", "step-t3w02-03"): (
        "c3cf0790ba44",
        "fig-04: LABEL ONLY, prepended to the description of the two labelled circles "
        "that was already there.",
    ),
    ("t3-w02", "step-t3w02-04"): (
        "abe94cc2b230",
        "fig-05 to fig-14: DESCRIPTIONS WRITTEN. These ten drawings had none — six sat "
        "directly under their problem heading and four under a Solution marker. Each "
        "TikZ was compiled and the rendered figure read, then described by what it "
        "shows and what is marked on it, in the register of the captions she has "
        "elsewhere. Nothing is inferred from the surrounding text: fig-12 says a rope "
        "wound round an upright cylinder because that is what the drawing shows.",
    ),
    ("t3-w04", "step-t3w04-02"): (
        "f74c110beb0b",
        "fig-01 and fig-02: LABELS ONLY, prepended to the cube and cuboid descriptions "
        "already in the file.",
    ),
    ("t3-w04", "step-t3w04-03"): (
        "844150f14ee6",
        "fig-03 to fig-07: LABELS ONLY, prepended to the four pyramid descriptions and "
        "the cone description already in the file.",
    ),
    ("t3-w06", "step-t3w06-04"): (
        "be31bca58ea8",
        "Bisection steps 5-6 and the midpoint label $M$. Her numbered steps end at "
        "'cut the first arc at P and Q' — executed literally they leave the segment "
        "unbisected — but fig-12 already DRAWS the completion. The steps now say what "
        "her own drawing shows: join $P$ to $Q$, and $PQ$ crosses $AB$ at its midpoint "
        "at $90^\\circ$. $M$ names the crossing the figure marks but never labelled.",
    ),
    ("t3-w06", "step-t3w06-02"): (
        "96ca2ceee863",
        "Captions rewritten to describe what IS drawn, dropping the sentences that "
        "recorded what the drawing fails to label — those belong in the review copy. "
        "Plus fig-03 and fig-05 REDRAWN: her set squares there have no right angle "
        "(62/94/24) and the right-angle mark sits at the ruler junction, an arrangement "
        "that cannot exist. Both now use a right-angled triangle with the mark at the "
        "corner where the edge on $AB$ meets the upright edge, the ruler resting on the "
        "sloping edge — which is what makes it lean — and fig-05's two positions one "
        "translation apart, since sliding along a held ruler cannot rotate the square. "
        "fig-03 also now says the drawn size and the end carrying the right angle are not "
        "part of the method: the model was reading one drawn instance as a specification "
        "and asserting a 45-degree hypotenuse the note never claims. fig-02's caption "
        "corrected 2026-08-09: it described the mark as the angle where the ruler's edge "
        "meets $AB$, which is what made these panels look wrong. The mark is the set "
        "square's OWN right angle, between the edge lying along $AB$ and the edge running "
        "DOWN from it — nothing to do with the ruler, which is only the guide the square "
        "slides along. That 2026-08-09 wording said 'rising', and the square is drawn "
        "below $AB$: every vertex of it has $y \\le 0$, and fig-01 describes the same edge "
        "as running down. Corrected 2026-08-19.",
    ),
    # The perpendicular half of what used to be one merged step. When her objective (i)
    # was split into two — parallel, perpendicular — her own six-step Presentation was
    # restored, and this content moved under the step that teaches it. Same hand edits as
    # its parallel-line sibling: captions describing what IS drawn, and fig-09's foot
    # labelled Q, which her own item 3 names but her drawing leaves unmarked.
    ("t3-w06", "step-t3w06-03"): (
        "816648f33966",
        "Captions rewritten to describe what IS drawn, dropping the sentences that "
        "recorded what the drawing fails to label — those belong in the review copy. "
        "Plus fig-08 REDRAWN, which that pass did not do: its caption named a "
        "'right-angled triangle' and the drawn one measures 56.58/36.29/87.14, so the "
        "caption asserted the very thing `geometry_audit/findings.md` says the figure "
        "does not show. Steps 2 and 3 name a hypotenuse and a 'third edge', and only a "
        "real right angle, marked, lets a reader tell them apart. The upright edge now "
        "stands square on the base with the mark at that corner.",
    ),
    ("t3-w06", "step-t3w06-05"): (
        "f9ac0b5705b4",
        "The $90^\\circ$ procedure, reconstructed by the researcher from the photograph "
        "of the page: the source draws the construction but writes no steps, so both "
        "arms invented one, every round, with the same tangency error. Plus fig-13's "
        "caption, corrected — the four strokes stand on the line in pairs, they are not "
        "'on each side of the middle'.",
    ),
    ("t3-w06", "step-t3w06-06"): (
        "60a9fa49a8b6",
        "fig-14's caption, rewritten to state which arc is swung from where. The frozen "
        "wording named neither centre, and the coordinates settle it. Plus fig-14 "
        "REDRAWN, which that pass did not do: the caption it produced says the arc is "
        "'swung from $B$ through $X$', and as drawn it began at 5 degrees — 0.45 units "
        "clear of the line — so it never cut $BC$ at $X$ at all. One number: the arc now "
        "starts at 0 degrees and springs from $X$, which is what step 1 says it does.",
    ),
}


def declare() -> int:
    """Print the manifest for the tree as it stands, for review then paste."""
    print("DECLARED_ADDITIONS = {")
    for case in _frozen():
        for step in case["plan"]["steps"]:
            if not step.get("note"):
                continue
            path = note_path(case["lesson"], step["step_id"])
            if not path.exists():
                continue
            added = additions(step["note"], path.read_text(encoding="utf-8"))
            if not added:
                continue
            digest = addition_digest(step["note"], path.read_text(encoding="utf-8"))
            print(f'    ("{case["lesson"]}", "{step["step_id"]}"): (')
            print(f'        "{digest}",')
            print('        "WHY — replace this",')
            print("    ),")
            for para in added:
                print(f"    # + {para[:96]}")
    print("}")
    return 0


def diff() -> int:
    """What the hand edits actually changed, per step."""
    total = 0
    for case in _frozen():
        for step in case["plan"]["steps"]:
            if not step.get("note"):
                continue
            path = note_path(case["lesson"], step["step_id"])
            if not path.exists():
                print(f"  {case['lesson']}/{step['step_id']}: NOT EXPORTED")
                continue
            lines = list(
                difflib.unified_diff(
                    step["note"].splitlines(),
                    path.read_text(encoding="utf-8").splitlines(),
                    fromfile=f"frozen/{step['step_id']}",
                    tofile=f"clean/{step['step_id']}",
                    lineterm="",
                    n=0,
                )
            )
            if lines:
                total += 1
                print("\n".join(lines))
    print(f"\n{total} step notes edited")
    return 0


def _steps_with_notes() -> set[tuple[str, str]]:
    return {
        (case["lesson"], step["step_id"])
        for case in _frozen()
        for step in case["plan"]["steps"]
        if step.get("note")
    }


def orphans() -> dict[str, list[tuple[str, str]]]:
    """Where the generation copies and the frozen plans disagree about which steps exist.

    Renumbering a lesson's steps breaks three things at once and none of them fails loudly:
    a copy for a dead step id lingers with stale content and is never read again; a live
    step with no copy only raises when a run reaches it; and a declaration keyed to a dead
    id silently stops guarding anything. Splitting `t3-w06`'s compound objective moved five
    step ids and hit all three on the same day `t3-w05`'s intro step had already shifted two.
    """
    frozen = _steps_with_notes()
    on_disk = {(path.parent.name, path.stem) for path in CLEAN_DIR.glob("*/*.md")}
    return {
        "orphaned_copies": sorted(on_disk - frozen),
        "missing_copies": sorted(frozen - on_disk),
        "orphaned_declarations": sorted(k for k in DECLARED_ADDITIONS if k not in frozen),
    }


def audit() -> int:
    """Report every disagreement between the copies, the declarations and the plans."""
    found = orphans()
    for name, items in found.items():
        label = name.replace("_", " ")
        if items:
            print(f"  {label}: {len(items)}")
            for lesson, step_id in items:
                print(f"      {lesson}/{step_id}")
        else:
            print(f"  {label}: none")
    return 1 if any(found.values()) else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("export", "diff", "verify", "declare", "audit"))
    actions = {"export": export, "diff": diff, "verify": verify, "declare": declare, "audit": audit}
    return actions[parser.parse_args().action]()


if __name__ == "__main__":
    raise SystemExit(main())
