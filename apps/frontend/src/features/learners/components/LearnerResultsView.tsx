import { Link } from "@/shared/router";

import { BAND_LABEL, STANDING_LABEL } from "../lib/bands";
import { buttonClass } from "@/shared/components/ui/Button";

import {
  lessonHref,
  noteHref,
  recentTests,
  scoreText,
  trendSentence,
} from "../lib/learnerResults";
import { LearnerLesson, LearnerResults } from "../types";

const OVERLINE =
  "text-[11px] font-semibold uppercase tracking-[0.12em] text-(--faint)";

function LessonLink({ title, periodId }: { title: string; periodId: string }) {
  return (
    <Link
      href={lessonHref(periodId)}
      className="underline underline-offset-2 hover:text-(--accent)"
    >
      {title}
    </Link>
  );
}

/** Where a lesson's revision note stands for the learner: a button to review it, or what it waits for. */
function RevisionNote({ lesson }: { lesson: LearnerLesson }) {
  if (lesson.revision_note === "to_review" && lesson.revision_note_id) {
    return (
      <Link
        href={noteHref(lesson.revision_note_id)}
        className={buttonClass({ variant: "secondary", size: "sm" })}
      >
        Review
      </Link>
    );
  }
  if (lesson.revision_note === "approved") return <span>✓ Approved</span>;
  if (lesson.revision_note === "waiting_for_test")
    return <span>○ Waits for the class test</span>;
  return <span>No note yet</span>;
}

function LessonsTable({ lessons }: { lessons: LearnerLesson[] }) {
  return (
    <section className="flex flex-col gap-2">
      <h2 className={OVERLINE}>Lessons</h2>
      <table className="w-full border border-(--line) bg-(--surface) text-left text-sm">
        <thead className="bg-(--sunken) text-[11px] uppercase tracking-[0.12em] text-(--faint)">
          <tr>
            <th className="px-4 py-2 font-semibold">Lesson</th>
            <th className="px-4 py-2 font-semibold">Test</th>
            <th className="px-4 py-2 font-semibold">Band</th>
            <th className="px-4 py-2 font-semibold">Revision note</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-(--line)">
          {lessons.map((lesson) => (
            <tr key={lesson.lesson_period_id}>
              <td className="px-4 py-3 text-(--ink)">
                <LessonLink
                  title={lesson.lesson_title}
                  periodId={lesson.lesson_period_id}
                />
              </td>
              <td className="whitespace-nowrap px-4 py-3 text-(--ink-2)">
                {lesson.band ? scoreText(lesson.correct, lesson.out_of) : ""}
              </td>
              <td className="px-4 py-3 text-(--ink-2)">
                {lesson.band ? BAND_LABEL[lesson.band] : ""}
              </td>
              <td className="whitespace-nowrap px-4 py-3 text-(--ink-2)">
                <RevisionNote lesson={lesson} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}

/** How a learner is doing: the latest scores, every objective, then each lesson and its revision note. */
export function LearnerResultsView({ results }: { results: LearnerResults }) {
  if (results.tests.length === 0) {
    return (
      <div className="flex flex-col gap-6">
        <p className="text-sm text-(--ink-2)">
          This learner has not sat a class test for this subject yet.
        </p>
        {results.lessons.length > 0 ? (
          <LessonsTable lessons={results.lessons} />
        ) : null}
      </div>
    );
  }
  const recent = recentTests(results.tests);
  const trend = trendSentence(recent);

  return (
    <div className="flex flex-col gap-6">
      <section className="flex flex-col gap-2">
        <h2 className={OVERLINE}>Recent scores</h2>
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
          {recent.map((test) => (
            <div
              key={test.lesson_period_id}
              className="flex flex-col gap-1 border border-(--line) bg-(--surface) p-4"
            >
              <span className="text-sm">
                <LessonLink
                  title={test.lesson_title}
                  periodId={test.lesson_period_id}
                />
              </span>
              <span className="text-base font-semibold text-(--ink)">
                {scoreText(test.correct, test.out_of)}
              </span>
              <span className="text-xs text-(--ink-2)">
                {BAND_LABEL[test.band]}
              </span>
            </div>
          ))}
        </div>
        {trend ? <p className="text-xs text-(--ink-2)">{trend}</p> : null}
      </section>

      <section className="flex flex-col gap-2">
        <h2 className={OVERLINE}>By objective</h2>
        <table className="w-full border border-(--line) bg-(--surface) text-left text-sm">
          <thead className="bg-(--sunken) text-[11px] uppercase tracking-[0.12em] text-(--faint)">
            <tr>
              <th className="px-4 py-2 font-semibold">Objective</th>
              <th className="px-4 py-2 font-semibold">Standing</th>
              <th className="px-4 py-2 font-semibold">Correct</th>
              <th className="px-4 py-2 font-semibold">Lesson</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-(--line)">
            {results.objectives.map((objective, index) => (
              <tr key={`${objective.lesson_period_id}-${index}`}>
                <td className="px-4 py-3 font-semibold text-(--ink)">
                  {objective.objective_text}
                </td>
                <td className="px-4 py-3 text-(--ink-2)">
                  {STANDING_LABEL[objective.band]}
                </td>
                <td className="px-4 py-3 text-(--ink-2)">
                  {scoreText(objective.correct, objective.out_of)}
                </td>
                <td className="px-4 py-3 text-(--ink-2)">
                  <LessonLink
                    title={objective.lesson_title}
                    periodId={objective.lesson_period_id}
                  />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      {results.lessons.length > 0 ? (
        <LessonsTable lessons={results.lessons} />
      ) : null}
    </div>
  );
}
