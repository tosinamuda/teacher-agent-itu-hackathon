import { ClassTestText } from "@/shared/components/renderer/ClassTestText";
import { Badge } from "@/shared/components/ui/Badge";

import { DiagnosticObjectiveQuestions } from "../lib/experiments";

/** Renders the lesson's MCQ diagnostic (the questions the student answered). */
export function JourneyDiagnostic({
  objectives,
}: {
  objectives: DiagnosticObjectiveQuestions[];
}) {
  if (objectives.length === 0) {
    return <p className="text-sm italic text-(--muted)">No diagnostic generated for this lesson.</p>;
  }
  return (
    <div className="space-y-4">
      {objectives.map((objective) => (
        <div key={objective.lesson_objective_id} className="space-y-2">
          <p className="text-xs font-semibold uppercase tracking-wide text-(--muted)">
            {objective.objective_text ?? objective.lesson_objective_id}
          </p>
          {objective.items.map((item, index) => (
            <div key={item.item_id} className="rounded-xl border border-(--line) bg-stone-50/50 p-3">
              <div className="flex items-start justify-between gap-2">
                <div className="flex gap-1 text-sm font-medium text-(--ink)">
                  <span>Q{index + 1}.</span>
                  <ClassTestText text={item.stem} />
                </div>
                {item.difficulty ? <Badge variant="outline">{item.difficulty}</Badge> : null}
              </div>
              <ul className="mt-2 space-y-1 text-sm text-(--ink)">
                {Object.entries(item.options).map(([key, text]) => (
                  <li key={key} className="flex gap-1">
                    <span className="font-semibold">{key}.</span>
                    <ClassTestText text={text} />
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}
