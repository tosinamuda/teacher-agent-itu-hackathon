import { useLearnerAnswers } from "../hooks/useStudyResults";

const MISSED_ONLY = "Only the questions this learner got wrong were kept, so the ones they got right are not shown.";

/** Every question the learner met on the lesson, with what they answered and what was right. */
export function LearnerAnswersSection({
  lessonPeriodId,
  studentId,
}: {
  lessonPeriodId: string;
  studentId: string;
}) {
  const answers = useLearnerAnswers(lessonPeriodId, studentId);
  if (answers.isLoading) return <p className="text-sm text-(--ink-2)">Loading their answers…</p>;
  if (answers.isError) return <p className="text-sm text-(--danger)">Couldn&apos;t load their answers.</p>;
  if (!answers.data || answers.data.answers.length === 0) return null;

  return (
    <section aria-label="Their answers" className="flex flex-col gap-3">
      <h2 className="text-sm font-semibold text-(--ink)">Their answers</h2>
      {answers.data.source === "missed_only" ? <p className="text-xs text-(--ink-2)">{MISSED_ONLY}</p> : null}
      <ol className="flex flex-col gap-3">
        {answers.data.answers.map((answer, index) => (
          <li
            key={`${index}-${answer.question}`}
            className="flex flex-col gap-2 border border-(--line) bg-(--surface) px-4 py-3"
          >
            <p className="text-xs text-(--ink-2)">{answer.objective_text}</p>
            <p className="text-sm text-(--ink)">{answer.question}</p>
            <p className="text-sm text-(--ink)">
              <span className="font-semibold">{answer.correct ? "Right: " : "Wrong: "}</span>
              {answer.student_answer || "No answer kept"}
            </p>
            {answer.correct ? null : (
              <p className="text-sm text-(--ink-2)">Should be: {answer.correct_answer}</p>
            )}
            {answer.misconception ? (
              <p className="text-xs text-(--ink-2)">Mistake shown: {answer.misconception}</p>
            ) : null}
          </li>
        ))}
      </ol>
    </section>
  );
}
