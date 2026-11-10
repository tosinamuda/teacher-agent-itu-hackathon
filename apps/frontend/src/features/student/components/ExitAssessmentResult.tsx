import { Link } from "@/shared/router";

import { Button } from "@/shared/components/ui/Button";

import type { ExitAssessmentObjective } from "@/features/student/api/exitAssessment";

type Props = {
  objectives: ExitAssessmentObjective[];
  answeredByObjective: Record<string, { answered: number; total: number }>;
  /** The student took this assessment on an earlier visit. */
  alreadySubmitted?: boolean;
};

/**
 * Post-submit panel: per-objective recap + an "awaiting approval" notice. The
 * personalised revision note is generated automatically on submit and held for
 * teacher review — the student sees it later, only once a teacher approves it.
 */
export function ExitAssessmentSubmittedPanel({
  objectives,
  answeredByObjective,
  alreadySubmitted = false,
}: Props) {
  return (
    <div className="rounded-2xl border border-(--line) bg-(--surface) p-5">
      <p className="font-medium text-(--ink)">
        {alreadySubmitted
          ? "You have already taken this assessment."
          : "Recorded ✓ — your answers were graded."}
      </p>
      <ul className={alreadySubmitted ? "hidden" : "my-2 text-sm text-(--muted)"}>
        {objectives.map((objective, index) => {
          const tally = answeredByObjective[objective.lesson_objective_id];
          return tally ? (
            <li key={objective.lesson_objective_id}>
              {tally.answered}/{tally.total} answered:{" "}
              {objective.objective_text ?? `Objective ${index + 1}`}
            </li>
          ) : null;
        })}
      </ul>
      <p className="mt-3 text-sm text-(--muted)">
        {alreadySubmitted
          ? "Your personalised revision note appears in your lessons once your teacher approves it."
          : "Your personalised revision note is being prepared. It will appear in your lessons once your teacher has reviewed and approved it."}
      </p>
      <div className="mt-4">
        <Link href="/research/student">
          <Button variant="primary">Back to my lessons</Button>
        </Link>
      </div>
    </div>
  );
}
