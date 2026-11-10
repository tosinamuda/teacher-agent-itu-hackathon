import type { CurriculumChoice, UnmappedObjective } from "../api/reusePlan";

const FIELD =
  "rounded-md border border-(--line) bg-(--surface) px-2 py-1.5 text-sm text-(--ink)";

/** For each lesson objective with no curriculum objective yet, choose one of this lesson's. */
export function CurriculumChoices({
  unmapped,
  choices,
  chosen,
  onChoose,
}: {
  unmapped: UnmappedObjective[];
  choices: CurriculumChoice[];
  chosen: Record<string, string>;
  onChoose: (lessonObjectiveId: string, curriculumObjectiveId: string) => void;
}) {
  return (
    <section className="space-y-3 rounded-2xl border border-(--line) bg-(--surface) p-5">
      <h2 className="text-base font-semibold text-(--ink)">
        Which curriculum objective does each objective serve?
      </h2>
      <p className="text-sm text-(--ink-2)">
        This lesson has more than one curriculum objective, so the plan&apos;s
        objectives need one each.
      </p>
      <ul className="space-y-3">
        {unmapped.map((objective) => (
          <li key={objective.lesson_objective_id} className="space-y-1">
            <label className="block text-sm text-(--ink)">
              {objective.objective_text || objective.lesson_objective_id}
              <select
                className={`${FIELD} mt-1 block w-full`}
                value={chosen[objective.lesson_objective_id] ?? ""}
                onChange={(event) =>
                  onChoose(objective.lesson_objective_id, event.target.value)
                }
              >
                <option value="">Choose one</option>
                {choices.map((choice) => (
                  <option
                    key={choice.curriculum_objective_id}
                    value={choice.curriculum_objective_id}
                  >
                    {choice.objective_text || choice.curriculum_objective_id}
                  </option>
                ))}
              </select>
            </label>
          </li>
        ))}
      </ul>
    </section>
  );
}
