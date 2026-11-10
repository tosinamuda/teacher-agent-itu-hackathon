# Sequencing bake-off — findings log (append-only)

Each run is a dated section below; runs are appended, never overwritten.

---

## Run — prior session

Design: 3 topics x 4 variants x 3 seeds (36 cells), judged by 2 models.

## Per-variant aggregates

| variant | valid% | refs clean% | mean llm_chars | gpt-oss-120b mean±sd | llama-3.3-70b-instruct mean±sd |
|---|---|---|---|---|---|
| regenerate | 100% | 0% | 5404 | 4.04±0.46 | 5.00±0.00 |
| markers | 100% | 67% | 2554 | 3.70±0.62 | 5.00±0.00 |
| blocklist | 100% | 100% | 1453 | 3.37±0.53 | 5.00±0.00 |
| append | 100% | 0% | 3260 | 3.15±0.50 | 5.00±0.00 |

## Paired win-rate (FOCAL = blocklist, per judge, across matched cells)


**Judge gpt-oss-120b**

| vs | wins | ties | losses | win-rate |
|---|---|---|---|---|
| blocklist vs regenerate | 1 | 1 | 7 | 17% |
| blocklist vs markers | 2 | 2 | 5 | 33% |
| blocklist vs append | 6 | 1 | 2 | 72% |

**Judge llama-3.3-70b-instruct**

| vs | wins | ties | losses | win-rate |
|---|---|---|---|---|
| blocklist vs regenerate | 0 | 9 | 0 | 50% |
| blocklist vs markers | 0 | 9 | 0 | 50% |
| blocklist vs append | 0 | 9 | 0 | 50% |

## Interpretation (the N=1 "blocklist wins" did NOT replicate)

**Headline: at scale, blocklist does NOT win on judged quality.** On the only discriminating
judge (gpt-oss-120b) the ranking was **regenerate (4.04) > markers (3.70) > blocklist (3.37) >
append (3.15)** — blocklist came *third*, and lost head-to-head to regenerate (17%) and markers
(33%). The earlier single-run blocklist win was noise.

**Two confounds make the judged-quality result unreliable:**

1. **Verbosity bias.** The judge rewarded the *longest* output: regenerate (5404 LLM chars)
   scored highest, blocklist (1453) lowest — a near-perfect inverse of brevity. The judge
   appears to conflate "more text" with "better lesson," a known LLM-judge failure mode.
2. **The second judge is useless here.** llama-3.3-70b returned **5.00 on every single cell**
   (sd 0.00) — zero discrimination. So we effectively have *one* judge, which sharply lowers
   confidence in any quality ranking.

**The LaTeX-corruption premise also did NOT replicate.** Regenerate was **100% valid across all
9 cells** — the broken `\hline` table we found in production was an *occasional* failure, not a
frequent one. So "regeneration reliably breaks LaTeX" is not supported; it breaks *sometimes*.

**What IS robust (deterministic, holds across all 9 cells):**
- **Ref faithfulness:** blocklist **100%** clean vs markers **67%**. The markers failures are
  concrete and repeatable: on the 3-figure decimals topic (ch01-b017) markers placed the table but
  **dropped all three figures on every seed**, while blocklist placed all four assets every time.
  The typed block-list output is more reliable than inline markers at not losing assets.
- **Char economy:** blocklist is cheapest by far — **1453** LLM chars vs markers 2554, append
  3260, regenerate **5404** (~3.7x blocklist). Less LLM-authored text = smaller corruption surface
  and lower cost.

**Honest verdict.** We **cannot** claim blocklist wins on pedagogical quality. Its case rests on
**efficiency + ref-faithfulness + validity-by-construction (for the occasions regeneration *does*
break) + free provenance** — not on judged quality, where a verbosity-biased single judge favors
the richer regeneration. The transclusion direction is *not* invalidated, but its justification is
narrower and more honest than the first run suggested.

**To actually resolve the quality question** you would need: a length-controlled / brevity-aware
judge (or length-normalised scoring), a *discriminating* second judge (drop llama-3.3-70b), more
seeds/topics, a regenerate arm that matches the real production writer (this one was a simplified
proxy), and ultimately the expert-teacher rating that is the thesis's real evaluation anyway.

---

## Run — 2026-06-03 (re-run)

Design: 3 topics x 4 variants x 3 seeds (36 cells), judged by 2 models.

## Per-variant aggregates

| variant | valid% | refs clean% | mean llm_chars | gpt-oss-120b mean±sd | llama-3.3-70b-instruct mean±sd |
|---|---|---|---|---|---|
| regenerate | 100% | 0% | 4282 | 4.19±0.79 | 5.00±0.00 |
| markers | 100% | 100% | 2343 | 4.30±0.62 | 5.00±0.00 |
| blocklist | 100% | 100% | 1174 | 3.85±0.94 | 5.00±0.00 |
| append | 100% | 0% | 2561 | 3.63±0.81 | 5.00±0.00 |

## Paired win-rate (FOCAL = blocklist, per judge, across matched cells)


**Judge gpt-oss-120b**

| vs | wins | ties | losses | win-rate |
|---|---|---|---|---|
| blocklist vs regenerate | 2 | 2 | 5 | 33% |
| blocklist vs markers | 2 | 2 | 5 | 33% |
| blocklist vs append | 4 | 3 | 2 | 61% |

**Judge llama-3.3-70b-instruct**

| vs | wins | ties | losses | win-rate |
|---|---|---|---|---|
| blocklist vs regenerate | 0 | 9 | 0 | 50% |
| blocklist vs markers | 0 | 9 | 0 | 50% |
| blocklist vs append | 0 | 9 | 0 | 50% |
