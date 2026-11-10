import type { Mark } from "../api/onBehalf";
import {
  NOT_MARKED,
  type WorkMark,
  type WorkedQuestion,
} from "../lib/markedWork";

const fieldClass =
  "w-full border border-(--line-2) bg-(--surface) px-2 py-1.5 text-sm text-(--ink) outline-none focus:border-(--accent)";

const MARKS: { value: Mark; label: string }[] = [
  { value: "correct", label: "Correct" },
  { value: "incorrect", label: "Incorrect" },
  { value: "unmarked", label: "Not marked" },
];

/** One student's work on each question: the mark, their working, and the mistake it shows. */
export function MarkedWorkForm({
  questions,
  marks,
  onMark,
}: {
  questions: WorkedQuestion[];
  marks: Record<string, WorkMark>;
  onMark: (questionId: string, mark: WorkMark) => void;
}) {
  const ready = questions.filter((found) => found.question.trim());
  if (ready.length === 0) {
    return (
      <p className="text-sm text-(--muted)">
        Add a question above to mark this student&apos;s work.
      </p>
    );
  }
  return (
    <div className="space-y-4">
      {ready.map((found, index) => {
        const given = marks[found.id] ?? NOT_MARKED;
        const set = (next: Partial<WorkMark>) =>
          onMark(found.id, { ...given, ...next });
        return (
          <fieldset
            key={found.id}
            className="space-y-2 border border-(--line-2) bg-(--surface) p-3"
          >
            <legend className="text-sm text-(--ink-2)">
              {index + 1}. {found.question}
            </legend>
            <div
              role="radiogroup"
              aria-label={`Mark for question ${index + 1}`}
              className="flex gap-4"
            >
              {MARKS.map((option) => (
                <label
                  key={option.value}
                  className="flex items-center gap-1 text-sm text-(--ink-2)"
                >
                  <input
                    type="radio"
                    name={`mark-${found.id}`}
                    checked={given.mark === option.value}
                    onChange={() => set({ mark: option.value })}
                  />
                  {option.label}
                </label>
              ))}
            </div>
            {given.mark !== "unmarked" ? (
              <textarea
                className={fieldClass}
                rows={2}
                aria-label={`Working for question ${index + 1}`}
                placeholder="The student's working (optional)"
                value={given.working}
                onChange={(event) => set({ working: event.target.value })}
              />
            ) : null}
            {given.mark === "incorrect" ? (
              <div className="grid gap-2 sm:grid-cols-2">
                <input
                  className={fieldClass}
                  aria-label={`Mistake in question ${index + 1}`}
                  placeholder="The mistake, in a few words"
                  value={given.misconception}
                  onChange={(event) =>
                    set({ misconception: event.target.value })
                  }
                />
                <input
                  className={fieldClass}
                  aria-label={`Explanation for question ${index + 1}`}
                  placeholder="In your words (optional)"
                  value={given.explanation}
                  onChange={(event) => set({ explanation: event.target.value })}
                />
              </div>
            ) : null}
          </fieldset>
        );
      })}
    </div>
  );
}
