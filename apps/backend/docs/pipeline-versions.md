# Pipeline versions

A pipeline version is the code path that generates a revision pack. It fixes three things:

- the composer's tool descriptions
- the critic's instructions
- the repair step's output schema

Each version takes its name from the date of its code. The pack spec is data in
`content_specifications`, and every version injects the same stored spec.

| Version | Status | Study material it generated |
| --- | --- | --- |
| `2026-08-25` | Frozen | Part 1 (C0–C3), and Part 2's P0 (Part 1's C3 draw 1) |
| `2026-09-02` | Frozen, current | Part 2's P1 |

- A request with no version gets `CURRENT_PIPELINE`, which is `2026-09-02`.
- A named version never changes. New generation code gets a new version with a new date.
- A pack records its version in `artefact_refs["pipeline"]`. `pipeline_that_wrote()` reads it back.
- The content route takes the version in the `pipeline` field of `GenerateContentRequest`.

## Where the versions differ

The versions differ only in prompt text:

| Prompt part | `2026-09-02` adds | Code |
| --- | --- | --- |
| Composer tools | "Text is markdown … and never HTML" | `infrastructure/dspy/tools/section_draft.py` (`composition_tools`) |
| Repair block schema | The same markdown sentence | `infrastructure/dspy/contracts/repair_section.py`, `evaluated_revision.py` |
| Critic instructions | Acceptance of a "fig-NN" figure citation | `infrastructure/dspy/contracts/critique_sections.py` |

The paths are under `src/app/domains/artefacts/types/post_class_review_pack/`.

## How the tests hold each version

Each frozen version must send, byte for byte, the prompts recorded from the code that generated
its material. The records are in `tests/snapshots/prompts/evaluated/`.
`tests/test_review_pack_pipelines.py` checks them.

| Version | Recorded at | Checked |
| --- | --- | --- |
| `2026-08-25` | `5b43e968`, which recorded Part 1's run `c0c3-prism-objective` | The composer's first turn for C0–C3. The C3 critic and repair calls. Every prompt input the run fingerprinted, except `arm.sampling` (decoding settings). |
| `2026-09-02` | `a3d6bb58`, which recorded Part 2's run `h2-deepseek-clean` | P1's personalisation call. The critic and repair calls of its validation. |

- Part 2's run wrote no fingerprint. Its record depends on the commit and the time of the run.
- Identical prompts do not give identical material. The decoding settings changed after the study, and the model is not deterministic.

`src/app/domains/artefacts/types/post_class_review_pack/domain/pipeline.py` defines the versions.
