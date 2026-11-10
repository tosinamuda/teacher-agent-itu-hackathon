import { Link } from "@/shared/router";

import { BAND_LABEL } from "../lib/bands";
import { ClassLearner } from "../types";

function Chevron() {
  return (
    <svg
      viewBox="0 0 16 16"
      width="16"
      height="16"
      aria-hidden="true"
      className="text-(--ink-2)"
    >
      <path
        d="M6 3.5L10.5 8 6 12.5"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.5"
      />
    </svg>
  );
}

const lastTestScore = (test: NonNullable<ClassLearner["last_test"]>): string =>
  test.correct === null ? "Taken" : `${test.correct} of ${test.out_of}`;

/** Where a learner's notes stand: some to review, all approved, or none made yet. */
function Notes({ learner }: { learner: ClassLearner }) {
  if (learner.notes_to_review > 0) {
    return (
      <span className="flex items-center gap-2">
        <span
          aria-hidden="true"
          className="size-2 rounded-full bg-(--accent)"
        />
        {learner.notes_to_review} to review
      </span>
    );
  }
  return (
    <span>{learner.notes_approved > 0 ? "All approved" : "No notes yet"}</span>
  );
}

/** A class's learners. A row is the way into the learner, so it carries no button of its own. */
export function LearnerTable({
  learners,
  isLoading,
}: {
  learners: ClassLearner[];
  isLoading: boolean;
}) {
  if (isLoading) {
    return (
      <p className="py-8 text-center text-sm text-(--ink-2)">
        Loading learners…
      </p>
    );
  }
  if (learners.length === 0) {
    return (
      <p className="py-8 text-center text-sm text-(--ink-2)">
        No learners to show. Add one, or clear the search.
      </p>
    );
  }

  return (
    <table className="w-full border border-(--line) bg-(--surface) text-left text-sm">
      <thead className="bg-(--sunken) text-[11px] uppercase tracking-[0.12em] text-(--faint)">
        <tr>
          <th className="px-4 py-2 font-semibold">Name</th>
          <th className="px-4 py-2 font-semibold">Band</th>
          <th className="px-4 py-2 font-semibold">Last test</th>
          <th className="px-4 py-2 font-semibold">Notes</th>
          <th className="w-10" />
        </tr>
      </thead>
      <tbody className="divide-y divide-(--line)">
        {learners.map((learner) => (
          <tr key={learner.student_id} className="relative hover:bg-(--sunken)">
            <td className="px-4 py-3 font-semibold text-(--ink)">
              <Link
                href={`/research/teacher/learners/${learner.student_id}`}
                className="after:absolute after:inset-0 focus-visible:outline-2 focus-visible:outline-(--accent)"
              >
                {learner.full_name}
              </Link>
            </td>
            <td className="px-4 py-3 text-(--ink-2)">
              {learner.last_test
                ? BAND_LABEL[learner.last_test.band]
                : "Not answered"}
            </td>
            <td className="px-4 py-3 text-(--ink-2)">
              {learner.last_test ? lastTestScore(learner.last_test) : "—"}
            </td>
            <td className="px-4 py-3 text-(--ink-2)">
              <Notes learner={learner} />
            </td>
            <td className="pr-4">
              <Chevron />
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
