import type { OnBehalfObjective } from "../api/onBehalf";
import type { WorkedQuestion } from "../lib/markedWork";

const fieldClass =
  "w-full border border-(--line-2) bg-(--surface) px-2 py-1.5 text-sm text-(--ink) outline-none focus:border-(--accent)";

const newQuestion = (objectives: OnBehalfObjective[]): WorkedQuestion => ({
  id: crypto.randomUUID(),
  lesson_objective_id: objectives[0]?.lesson_objective_id ?? "",
  question: "",
  model_answer: "",
});

/**
 * The classwork's questions, entered once for the whole class: the question, its model answer,
 * and the objective it checks. Each student's work is then marked against them.
 */
export function ClassworkQuestions({
  questions,
  objectives,
  onChange,
}: {
  questions: WorkedQuestion[];
  objectives: OnBehalfObjective[];
  onChange: (questions: WorkedQuestion[]) => void;
}) {
  const change = (id: string, next: Partial<WorkedQuestion>) =>
    onChange(
      questions.map((found) =>
        found.id === id ? { ...found, ...next } : found,
      ),
    );

  return (
    <section className="space-y-3">
      <p className="text-xs text-(--muted)">
        Enter the classwork&apos;s questions once. They stay for every student
        you record.
      </p>
      {questions.map((found, index) => (
        <fieldset
          key={found.id}
          className="space-y-2 border border-(--line-2) bg-(--surface) p-3"
        >
          <legend className="text-sm font-semibold text-(--ink-2)">
            Question {index + 1}
          </legend>
          <textarea
            className={fieldClass}
            rows={2}
            aria-label={`Question ${index + 1}`}
            placeholder="The question, as the students saw it"
            value={found.question}
            onChange={(event) =>
              change(found.id, { question: event.target.value })
            }
          />
          <input
            className={fieldClass}
            aria-label={`Model answer ${index + 1}`}
            placeholder="The model answer"
            value={found.model_answer}
            onChange={(event) =>
              change(found.id, { model_answer: event.target.value })
            }
          />
          <div className="flex items-center justify-between gap-3">
            <select
              className={fieldClass}
              aria-label={`Objective ${index + 1}`}
              value={found.lesson_objective_id}
              onChange={(event) =>
                change(found.id, { lesson_objective_id: event.target.value })
              }
            >
              {objectives.map((objective) => (
                <option
                  key={objective.lesson_objective_id}
                  value={objective.lesson_objective_id}
                >
                  {objective.objective_text || objective.lesson_objective_id}
                </option>
              ))}
            </select>
            <button
              type="button"
              className="text-xs text-(--danger-ink) underline"
              onClick={() =>
                onChange(questions.filter((other) => other.id !== found.id))
              }
            >
              Remove
            </button>
          </div>
        </fieldset>
      ))}
      <button
        type="button"
        className="text-sm font-semibold text-(--accent-deep) hover:underline"
        onClick={() => onChange([...questions, newQuestion(objectives)])}
      >
        + Add a question
      </button>
    </section>
  );
}
