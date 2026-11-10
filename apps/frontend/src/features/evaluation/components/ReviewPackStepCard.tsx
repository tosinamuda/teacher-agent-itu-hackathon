import { ContentBlockRenderer } from "@/shared/components/renderer/ContentBlockRenderer";

import { EvaluationReviewPackStep } from "../types";

type ReviewPackStepCardProps = {
  step: EvaluationReviewPackStep;
  tone?: "base" | "candidate";
  anchorId?: string;
};

const toneClassName = {
  base: "bg-stone-50",
  candidate: "bg-white",
} as const;

/** Renders one read-only review-pack step with its learner-facing blocks. */
export function ReviewPackStepCard({
  step,
  tone = "candidate",
  anchorId,
}: ReviewPackStepCardProps) {
  const blocks = step.blocks ?? [];

  return (
    <article
      className={`rounded-none border border-[color:var(--line)] p-5 ${toneClassName[tone]}`}
      id={anchorId}
    >
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div className="space-y-1">
          <h4 className="text-lg font-semibold text-[color:var(--ink)]">
            {step.title ?? "Untitled section"}
          </h4>
          {step.estimated_minutes ? (
            <p className="text-sm text-[color:var(--muted)]">
              Estimated reading time: {step.estimated_minutes} min
            </p>
          ) : null}
        </div>
      </div>

      {blocks.length > 0 ? (
        <div className="mt-5 space-y-4">
          {blocks.map((block, index) => (
            <div key={block.id ?? `${step.step_id}-${index}`} className="space-y-3">
              <ContentBlockRenderer block={block} />
            </div>
          ))}
        </div>
      ) : (
        <p className="mt-4 text-sm text-[color:var(--muted)]">
          No learner-facing blocks were recorded for this section.
        </p>
      )}
    </article>
  );
}
