import { Controller, type UseFormReturn } from "react-hook-form";

import { ClassTestText } from "@/shared/components/renderer/ClassTestText";

import type { ExitAssessmentObjective } from "@/features/student/api/exitAssessment";
import type { AssessmentFormValues } from "@/features/student/hooks/useExitAssessment";

/**
 * The MCQ items as ONE flat, continuously numbered list — the objective each
 * question assesses stays backend metadata (learner-model UI note: visible
 * objective grouping can hint the tested skill and makes the quiz feel heavier).
 * The post-class survey, by contrast, IS shown per objective.
 */
export function ExitAssessmentQuestionList({
  objectives,
  itemOffsets,
  form,
}: {
  objectives: ExitAssessmentObjective[];
  itemOffsets: number[];
  form: UseFormReturn<AssessmentFormValues>;
}) {
  const { control } = form;
  return (
    <ol className="flex flex-col gap-4">
      {objectives.flatMap((objective, objectiveIndex) =>
        objective.items.map((item, itemIndex) => {
          const fieldIndex = (itemOffsets[objectiveIndex] ?? 0) + itemIndex;
          return (
            <li
              key={item.item_id}
              className="rounded-2xl border border-(--line) bg-(--surface) p-5"
            >
              <div className="flex gap-1 text-sm font-medium text-(--ink)">
                <span className="font-semibold">{fieldIndex + 1}.</span>
                <ClassTestText text={item.stem} />
              </div>
              <Controller
                control={control}
                name={`answers.${fieldIndex}.selected_option`}
                render={({ field }) => (
                  <div className="mt-2 flex flex-col gap-1">
                    {Object.entries(item.options).map(([key, text]) => (
                      <label
                        key={key}
                        className={`flex cursor-pointer items-start gap-2 rounded-lg border px-3 py-2 text-sm ${field.value === key ? "border-(--accent) bg-(--accent-soft)" : "border-(--line)"}`}
                      >
                        <input
                          type="radio"
                          name={field.name}
                          value={key}
                          className="mt-1"
                          checked={field.value === key}
                          onChange={() => field.onChange(key)}
                        />
                        <span className="flex gap-1 text-(--ink)">
                          <span className="font-semibold">{key}.</span>
                          <ClassTestText text={text} />
                        </span>
                      </label>
                    ))}
                  </div>
                )}
              />
            </li>
          );
        })
      )}
    </ol>
  );
}
