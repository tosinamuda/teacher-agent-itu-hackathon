import { ContentBlockRenderer } from "@/shared/components/renderer/ContentBlockRenderer";

import { ReviewLessonPlan } from "../api/lessonPlan";

const ROLE_LABEL: Record<string, string> = {
  intro: "Introduction",
  core: "Core teaching",
  evaluation: "Evaluation",
};

/**
 * The authored lesson plan, rendered read-only for side-by-side comparison with
 * the generated revision note — so the teacher can judge how faithfully the note
 * reflects what they planned to teach before accepting it.
 */
export function LessonPlanComparePanel({ plan }: { plan: ReviewLessonPlan }) {
  return (
    <div className="space-y-5">
      <div>
        <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-(--muted)">
          Lesson plan
        </p>
        <h2 className="text-2xl font-semibold text-(--ink)">
          {plan.subtopic || plan.topic || "Lesson plan"}
        </h2>
        <p className="text-sm text-(--muted)">
          What you planned to teach — the note is built from this.
        </p>
      </div>

      {plan.lesson_plan_objectives.length > 0 ? (
        <div className="rounded-2xl border border-(--line) bg-white p-5">
          <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-(--accent-deep)">
            Lesson objectives
          </p>
          <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-(--ink)">
            {plan.lesson_plan_objectives.map((objective, index) => (
              <li key={objective.lesson_objective_id ?? index}>
                {objective.objective_text}
              </li>
            ))}
          </ul>
        </div>
      ) : null}

      {plan.steps.map((step, index) => (
        <article
          key={index}
          className="rounded-2xl border border-(--line) bg-white p-5"
        >
          <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-(--accent-deep)">
            {ROLE_LABEL[step.step_role ?? step.step_kind ?? ""] ??
              `Step ${index + 1}`}
          </p>
          <h3 className="text-lg font-semibold text-(--ink)">
            {step.title ?? "Untitled step"}
          </h3>
          {step.blocks.length > 0 ? (
            <div className="mt-4 space-y-4">
              {step.blocks.map((block, blockIndex) => (
                <ContentBlockRenderer
                  key={block.id ?? `${index}-${blockIndex}`}
                  block={block}
                />
              ))}
            </div>
          ) : null}
        </article>
      ))}
    </div>
  );
}
