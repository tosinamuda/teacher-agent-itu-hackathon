# The judged run generated from the raw notes — 2026-08-20

`c0c3-worksheet` is the run the H1 result rests on: 72 packs, rated twice, 576
dimension-scores, and the conclusion that **H1a is null** and **the evidence step is what
separates**. It was generated from the **frozen transcription**, not from `notes-clean/` —
so every hand correction made to the notes reached none of it.

## The evidence, on the wire

That run stored its prompts. `t3-w06`'s two copies differ enough to tell apart:

| marker | raw note | `notes-clean/` | the judged C2 prompt |
| --- | ---: | ---: | ---: |
| `**layered**` — editorial the clean copy exists to remove | 3 | **0** | **18** |
| "The set square has not moved" — a clean-only caption | 0 | 1 | **0** |
| "Join $P$ to $Q$ with a ruler" — the declared bisection fix | 0 | 1 | **0** |

Not inference from metadata: this is what was sent.

## The metadata agrees, and says how

`fingerprint.json` records the arm. Decoding the digests:

| run | notes | figures | signatures |
| --- | --- | --- | --- |
| `c0c3-worksheet` **(judged)** | raw | reference | shared |
| `c0c3-renumbered` **(judged, re-rated)** | raw | reference | shared |
| `c1-clean-payload` | raw | reference | shared |
| `c1-clean-control` | raw | reference | shared |
| `c1-corrected-b` | raw | reference | shared |
| `captions-regen` (2026-08-20) | clean | source | leveled |

Every run before today records the same three values, and they are exactly the argparse
defaults that stood until `6a28b704` (2026-08-19) changed `--generator` and `--signatures`.
`--note-source` still defaults to `raw` and `--figures` to `reference`.

The chain was checked end to end rather than assumed: `runner` builds `RunConfig` from the
parsed args, `execution` passes `config.signatures / note_source / figures` into
`write_fingerprint`, and only a module-move commit has ever touched that call. The
fingerprint records what ran. **Those runs were launched without the flags.**

`c1-clean-payload` is the tell — a run named for clean notes, recording `raw`.

## What it costs

`HANDOFF.md` §5.1 documents the command **with** `--signatures leveled --note-source clean
--figures source`. That is not the command that produced the judged packs.

So the judged generation never saw:

- the `t3-w06` caption rewrites, and `fig-03`/`fig-05` redrawn because the set squares had
  no right angle;
- the bisection procedure completed — the frozen steps stop before joining $P$ to $Q$, so
  executed literally they leave the segment unbisected;
- the $90^\circ$ procedure reconstructed from the photograph, which the frozen note lacks
  entirely;
- the editorial removal `note_editorial` exists for. Its own docstring records that this
  commentary "reaches the generator, gets paraphrased into learner text, and costs repair
  passes: 5 of 12 critic findings in round 8". It was in the judged prompt 18 times.

It also read `shared` signatures, which `HANDOFF.md` itself warns "leaves C0 reading
present-but-empty plan keys" — a confound on the control arm of the sole registered
endpoint.

## What this does and does not overturn

It does **not** show the null is wrong. It shows the judged packs were generated from
inputs the study had already decided were defective, and that the run record said so all
along in a field nobody decoded.

The measured judge noise stands — that was two ratings of one generation, and holds
whatever the generation read.

## What was done

`clean-six` (2026-08-20): all six lessons, C0–C3, three draws, on `compose-v2 / leveled /
clean / source`. 72 packs. The wire check that the judged run fails, it passes — inverted
exactly:

| marker | judged prompt | clean-six traces |
| --- | ---: | ---: |
| `**layered**` (raw only) | 18 | **0** |
| "The set square has not moved" (clean only) | 0 | **14** |
| "Join $P$ to $Q$ with a ruler" (clean only) | 0 | **6** |
| `fig-05.` (a caption written 2026-08-19) | — | **25** |

### What moved

**`raw_latex_markers` is zero on every arm.** It was 6.1 / 5.6 / 13.8 / 13.5 per pack for
C0 / C1 / C2 / C3 in the judged run — the open, directionally-unfair rendering defect the
handoff lists — and is 0.0 / 0.0 / 0.0 / 0.0 now.

**Recall is not reported here, and must not be.** It answers one question — did the
pipeline carry her content through — and the generation prompt asks the pack to cover what
the lesson taught, so a pack that mirrors the note scores high by construction. It flatters
exactly the arms that receive the note. A recall difference is not evidence about a
condition; only the frozen rubric, judged blind, adjudicates one. `clean-six` is **72
packs, unjudged**.

**Nothing here is attributable.** Three flags moved together — notes, figures and
signatures — on top of nine days of code. This says the judged numbers were measured on a
different system, not which change accounts for what. Anything causal needs one flag at a
time.

## The guard this needs

The fingerprint recorded the arm faithfully and nothing read it. `--diff` compares two runs
on request; nothing compares a run against the arm it was *supposed* to use. A run whose
recorded arm differs from the one its label or notes claim should fail at write time, not
wait nine days for someone to decode a digest.
