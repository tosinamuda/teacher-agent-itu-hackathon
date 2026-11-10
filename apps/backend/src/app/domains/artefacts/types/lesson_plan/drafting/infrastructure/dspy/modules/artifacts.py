"""The artifacts contract shared by the two lesson-generation layers.

Both the staged/curated pipeline (`LessonGenerationArtifacts`) and the single-call
no-linkage layer (`WholeLessonArtifacts`) expose the same surface the assembler,
semantic validator, and diagnostic writer read — `lesson_plan_objectives`,
`resolved_kcs`, `step_evidence_plans`, `core_steps`, `global_steps`,
`assessment_items`, `kc_plan` (theme / entry_behaviour / instructional_materials /
misconceptions), and `evidence_summaries`. `LessonGenerationArtifacts` additionally
carries the staged planning provenance (`planning_result`, `core_step_blueprints`,
durations) consumed only on the generation-metrics and diagnostic paths, which
narrow with `isinstance` before reading it. This alias makes that informal
duck-typing a checked type so both layers flow through the same code.
"""

from __future__ import annotations

from .generator import LessonGenerationArtifacts
from .whole_lesson_generator import WholeLessonArtifacts

GenerationArtifacts = LessonGenerationArtifacts | WholeLessonArtifacts
