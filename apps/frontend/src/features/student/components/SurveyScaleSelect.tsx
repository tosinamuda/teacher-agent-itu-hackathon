import {
  Controller,
  type FieldPath,
  type UseFormReturn,
} from "react-hook-form";

import type { SurveyScale } from "@/features/student/api/exitAssessment";
import type { AssessmentFormValues } from "@/features/student/hooks/useExitAssessment";

export type SurveyScaleOption = {
  readonly value: SurveyScale;
  readonly label: string;
};

/** A 1-5 survey question that starts unanswered, so a 3 in the data is always a choice. */
export function SurveyScaleSelect({
  form,
  name,
  question,
  options,
}: {
  form: UseFormReturn<AssessmentFormValues>;
  name: FieldPath<AssessmentFormValues>;
  question: string;
  options: readonly SurveyScaleOption[];
}) {
  return (
    <Controller
      control={form.control}
      name={name}
      render={({ field }) => (
        <label className="flex flex-col text-sm text-(--muted)">
          {question}
          <select
            className="mt-1 w-full max-w-[24rem] rounded-xl border border-(--line) bg-(--surface) px-3 py-2 text-(--ink)"
            onChange={(event) => field.onChange(Number(event.target.value))}
            value={typeof field.value === "number" ? field.value : ""}
          >
            <option value="" disabled>
              Choose an answer
            </option>
            {options.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </label>
      )}
    />
  );
}
