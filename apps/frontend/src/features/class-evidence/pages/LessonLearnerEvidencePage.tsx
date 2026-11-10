import { useLessonHome } from "@/features/lesson-home/hooks/useLessonHome";
import { BAND_LABEL, STANDING_LABEL } from "@/features/learners/lib/bands";
import { noteHref, scoreText } from "@/features/learners/lib/learnerResults";
import { useLearnerResults } from "@/features/learners/hooks/useLearnerResults";
import { buttonClass } from "@/shared/components/ui/Button";
import { RightPanel } from "@/shared/components/workspace/RightPanel";
import { WorkspacePage } from "@/shared/components/workspace/WorkspacePage";
import { Link } from "@/shared/router";

import { LearnerAnswersSection } from "../components/LearnerAnswersSection";
import { resultsForLesson } from "../lib/lessonLearnerResult";

const NOTE_STATUS: Record<string, string> = {
  to_review: "Waiting for your review",
  approved: "Approved",
  waiting_for_test: "Opens after the class test",
  not_made: "Not made yet",
};

/** One learner's result on one lesson, reached from the lesson's class evidence. */
export function LessonLearnerEvidencePage({
  lessonPeriodId,
  studentId,
}: {
  lessonPeriodId: string;
  studentId: string;
}) {
  const home = useLessonHome(lessonPeriodId);
  const learner = useLearnerResults(studentId);
  const found = learner.data ? resultsForLesson(learner.data, lessonPeriodId) : null;
  const evidenceHref = `/research/teacher/lessons/${lessonPeriodId}/evidence`;

  const panel = (
    <RightPanel
      needs={[]}
      agent={<p className="text-xs text-(--faint)">Each material has its own chat with the agent. Open a material to talk to it.</p>}
    />
  );

  return (
    <WorkspacePage panel={panel}>
      <div className="flex flex-col gap-5">
        <Link href={evidenceHref} className="text-sm text-(--ink-2) hover:text-(--ink)">
          ‹ Class evidence
        </Link>
        <header className="flex flex-col gap-1">
          <h1 className="text-2xl font-semibold text-(--ink)">{learner.data?.full_name ?? "Learner"}</h1>
          <p className="text-xs text-(--ink-2)">
            {home.lesson?.title ?? ""}
            {home.lesson ? ` · week ${home.lesson.week}` : ""}
          </p>
        </header>

        {learner.isLoading ? <p className="text-sm text-(--ink-2)">Loading…</p> : null}
        {learner.isError ? <p className="text-sm text-(--danger)">Couldn&apos;t load this learner.</p> : null}

        {found && !found.test ? (
          <p className="text-sm text-(--ink-2)">This learner has no result on this lesson yet.</p>
        ) : null}

        {found?.test ? (
          <section aria-label="Result on this lesson" className="flex flex-col gap-3">
            <p className="text-sm text-(--ink)">
              <span className="font-semibold">Scored {scoreText(found.test.correct, found.test.out_of)}</span>
              <span className="text-(--ink-2)"> · {BAND_LABEL[found.test.band]}</span>
            </p>
            {found.test.entered_by ? (
              <p className="text-xs text-(--ink-2)">Entered on their behalf: {found.test.entered_by}</p>
            ) : null}
            {found.objectives.length > 0 ? (
              <ul className="border border-(--line) bg-(--surface)">
                {found.objectives.map((objective) => (
                  <li
                    key={objective.objective_text}
                    className="flex items-center gap-4 border-t border-(--line) px-4 py-3 first:border-t-0"
                  >
                    <span className="flex min-w-0 flex-1 flex-col">
                      <span className="text-sm text-(--ink)">{objective.objective_text}</span>
                      <span className="text-xs text-(--ink-2)">
                        {scoreText(objective.correct, objective.out_of)}
                      </span>
                    </span>
                    <span className="text-sm text-(--ink-2)">{STANDING_LABEL[objective.band]}</span>
                  </li>
                ))}
              </ul>
            ) : null}
          </section>
        ) : null}

        {found?.test ? <LearnerAnswersSection lessonPeriodId={lessonPeriodId} studentId={studentId} /> : null}

        {found?.lesson ? (
          <section aria-label="Revision note" className="flex items-center gap-4 border border-(--line) bg-(--surface) px-4 py-3">
            <span className="flex min-w-0 flex-1 flex-col">
              <span className="text-sm font-semibold text-(--ink)">Their revision note</span>
              <span className="text-xs text-(--ink-2)">{NOTE_STATUS[found.lesson.revision_note] ?? ""}</span>
            </span>
            {found.lesson.revision_note_id ? (
              <Link
                href={noteHref(found.lesson.revision_note_id)}
                className={buttonClass({ variant: "secondary", size: "sm" })}
              >
                Open note
              </Link>
            ) : null}
          </section>
        ) : null}

        <Link
          href={`/research/teacher/learners/${studentId}`}
          className="self-start text-xs text-(--ink-2) underline hover:text-(--ink)"
        >
          All of {learner.data?.full_name ?? "this learner"}&apos;s results
        </Link>
      </div>
    </WorkspacePage>
  );
}
