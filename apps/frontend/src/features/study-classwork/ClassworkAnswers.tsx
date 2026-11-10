import { Badge } from "@/shared/components/ui/Badge";
import { NoteText } from "@/features/content/components/NoteText";

import { ClassworkAnswer, LearnerClasswork } from "./types";

const MARK_VARIANT: Record<string, "success" | "warning" | "default"> = {
  correct: "success",
  incorrect: "warning",
};

function Mark({ answer }: { answer: ClassworkAnswer | undefined }) {
  if (!answer) return <Badge variant="default">not attempted</Badge>;
  return (
    <Badge variant={MARK_VARIANT[answer.mark] ?? "default"}>
      {answer.mark}
      {answer.uncertain ? " (mark unclear)" : ""}
    </Badge>
  );
}

/**
 * A learner's classwork on one objective, read only: each question on it, the answer the study
 * took as right, the learner's working as the teacher marked it, and the misconception the
 * researcher read in it.
 */
export function ClassworkAnswers({
  classwork,
  objectiveId,
}: {
  classwork: LearnerClasswork;
  objectiveId: string;
}) {
  const questions = classwork.questions.filter((q) => q.lesson_objective_id === objectiveId);
  const answers = new Map((classwork.script?.answers ?? []).map((answer) => [answer.n, answer]));
  if (questions.length === 0) {
    return <p className="text-sm text-(--muted)">No class work question was set on it.</p>;
  }
  return (
    <ol className="space-y-3">
      {questions.map((question) => {
        const answer = answers.get(question.n);
        return (
          <li key={question.n} className="space-y-1 border-t border-(--line) pt-2 first:border-t-0 first:pt-0">
            <div className="flex flex-wrap items-center justify-between gap-2">
              <p className="text-xs text-(--muted)">Question {question.n}</p>
              <Mark answer={answer} />
            </div>
            <NoteText text={question.text} />
            {question.answer ? (
              <div className="text-xs text-(--muted)">
                Expected answer:
                <NoteText text={question.answer} />
              </div>
            ) : null}
            {answer?.working ? (
              <div className="rounded-md bg-(--sunken) p-2">
                <NoteText text={answer.working} />
              </div>
            ) : null}
            {answer?.misconception_code ? (
              <p className="text-sm text-(--ink-2)">
                <span className="font-mono text-xs">{answer.misconception_code}</span>
                {answer.misconception_why ? ` — ${answer.misconception_why}` : ""}
              </p>
            ) : null}
          </li>
        );
      })}
    </ol>
  );
}
