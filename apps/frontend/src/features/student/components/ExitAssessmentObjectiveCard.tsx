import type { UseFormReturn } from "react-hook-form";

import type { ExitAssessmentObjective } from "@/features/student/api/exitAssessment";
import {
  SurveyScaleSelect,
  type SurveyScaleOption,
} from "@/features/student/components/SurveyScaleSelect";
import type { AssessmentFormValues } from "@/features/student/hooks/useExitAssessment";

/** 1-5 answer options per the learner-model survey spec. */
const CONFIDENCE_OPTIONS: readonly SurveyScaleOption[] = [
  { value: 1, label: "1 · Not sure at all" },
  { value: 2, label: "2 · A little sure" },
  { value: 3, label: "3 · Somewhat sure" },
  { value: 4, label: "4 · Mostly sure" },
  { value: 5, label: "5 · Very sure" },
];
const DIFFICULTY_OPTIONS: readonly SurveyScaleOption[] = [
  { value: 1, label: "1 · Very easy" },
  { value: 2, label: "2 · Easy" },
  { value: 3, label: "3 · Okay" },
  { value: 4, label: "4 · Difficult" },
  { value: 5, label: "5 · Very difficult" },
];

/**
 * One objective's SURVEY card — shown after the test questions, per objective
 * ("About Objective N: ..."), per the learner-model spec: Confidence(s,o) and
 * Difficulty(s,o) on 1-5 scales. The test questions themselves render as a flat
 * list with the objective hidden (see ExitAssessmentQuestionList).
 */
export function ExitAssessmentObjectiveCard({
  objective,
  objectiveNumber,
  surveyIndex,
  form,
}: {
  objective: ExitAssessmentObjective;
  objectiveNumber: number;
  surveyIndex: number;
  form: UseFormReturn<AssessmentFormValues>;
}) {
  return (
    <article className="rounded-2xl border border-(--line) bg-(--surface) p-5">
      <h3 className="mb-3 font-semibold text-(--ink)">
        About Objective {objectiveNumber}:{" "}
        {objective.objective_text ?? objective.lesson_objective_id}
      </h3>
      {/* One survey question per row — side-by-side selects read as one combined
          question and cramp on small screens. */}
      <div className="flex flex-col gap-4">
        <SurveyScaleSelect
          form={form}
          name={`survey.${surveyIndex}.confidence`}
          question="How sure are you that you can do this by yourself?"
          options={CONFIDENCE_OPTIONS}
        />
        <SurveyScaleSelect
          form={form}
          name={`survey.${surveyIndex}.perceived_difficulty`}
          question="How difficult was this for you?"
          options={DIFFICULTY_OPTIONS}
        />
      </div>
    </article>
  );
}
