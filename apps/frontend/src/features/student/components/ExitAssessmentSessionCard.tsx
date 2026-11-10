import type { UseFormReturn } from "react-hook-form";

import {
  SurveyScaleSelect,
  type SurveyScaleOption,
} from "@/features/student/components/SurveyScaleSelect";
import type { AssessmentFormValues } from "@/features/student/hooks/useExitAssessment";

/** 1-5 answer options per the learner-model survey spec (session level). */
const INTEREST_OPTIONS: readonly SurveyScaleOption[] = [
  { value: 1, label: "1 · Not interested" },
  { value: 2, label: "2 · A little interested" },
  { value: 3, label: "3 · Somewhat interested" },
  { value: 4, label: "4 · Interested" },
  { value: 5, label: "5 · Very interested" },
];
const AFFECT_OPTIONS: readonly SurveyScaleOption[] = [
  { value: 1, label: "1 · Very confused" },
  { value: 2, label: "2 · Confused" },
  { value: 3, label: "3 · Okay" },
  { value: 4, label: "4 · Good" },
  { value: 5, label: "5 · Very good" },
];

/**
 * Session-level survey card: Interest + Affect, asked ONCE for the whole
 * subtopic session (the per-objective confidence/difficulty questions live on
 * each objective card). Learner-model spec: Interest(s,σ), Affect(s,σ) ∈ {1..5}.
 */
export function ExitAssessmentSessionCard({
  form,
}: {
  form: UseFormReturn<AssessmentFormValues>;
}) {
  return (
    <article className="rounded-2xl border border-(--line) bg-(--surface) p-5">
      <h3 className="mb-3 font-semibold text-(--ink)">
        About today&apos;s lesson
      </h3>
      {/* One survey question per row, matching the objective cards. */}
      <div className="flex flex-col gap-4">
        <SurveyScaleSelect
          form={form}
          name="session.interest"
          question="How interested were you in today's topic?"
          options={INTEREST_OPTIONS}
        />
        <SurveyScaleSelect
          form={form}
          name="session.affect"
          question="How did you feel at the end of the lesson?"
          options={AFFECT_OPTIONS}
        />
      </div>
    </article>
  );
}
