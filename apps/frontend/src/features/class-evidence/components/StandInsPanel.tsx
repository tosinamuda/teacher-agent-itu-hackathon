import { useState } from "react";

import { BAND_LABEL } from "@/features/learners/lib/bands";
import { buttonClass } from "@/shared/components/ui/Button";
import { Link } from "@/shared/router";

import type { StudyLearnerResult } from "../api/studyResults";
import { useStandIns } from "../hooks/useStudyResults";
import { importErrorText } from "../lib/importErrors";
import { suggestStandIns } from "../lib/standIns";

type ClassLearner = { student_id: string; full_name: string; answered: boolean };
type Choice = { student?: string; study?: string };

const SELECT = "min-w-0 max-w-full border border-(--line-2) bg-(--surface) px-2 py-1.5 text-sm text-(--ink)";

/**
 * Class learners who have not answered take the marks of study learners, so their own notes can
 * be made from them. A suggestion is filled in: a strength, a middle and a gap.
 */
export function StandInsPanel({
  lessonPeriodId,
  classLearners,
  studyLearners,
}: {
  lessonPeriodId: string;
  classLearners: ClassLearner[];
  studyLearners: StudyLearnerResult[];
}) {
  const standIns = useStandIns(lessonPeriodId);
  const [chosen, setChosen] = useState<Record<number, Choice>>({});
  const rows = suggestStandIns(classLearners, studyLearners).map((suggested, at) => ({
    student: chosen[at]?.student ?? suggested.studentId,
    study: chosen[at]?.study ?? suggested.studyStudentId,
  }));
  const choose = (at: number, change: Choice) => setChosen((now) => ({ ...now, [at]: { ...now[at], ...change } }));
  const free = classLearners.filter((learner) => !learner.answered);

  if (rows.length === 0) return null;
  if (standIns.isSuccess) {
    return (
      <p className="text-sm text-(--ink)">
        Notes are being made for {standIns.data.made.length} learners.{" "}
        <Link href="/research/teacher/pack-reviews" className="underline">
          Review them
        </Link>
      </p>
    );
  }
  return (
    <div className="flex flex-col gap-3 border border-(--line) bg-(--surface) p-4">
      <p className="text-sm text-(--ink)">
        Make a learner&apos;s own revision note from a study learner&apos;s marks. The learner takes those results as theirs.
      </p>
      <ul className="flex flex-col gap-2">
        {rows.map((row, at) => (
          <li key={at} className="flex flex-wrap items-center gap-2">
            <select aria-label={`Learner ${at + 1}`} value={row.student} onChange={(e) => choose(at, { student: e.target.value })} className={SELECT}>
              {free.map((learner) => (
                <option key={learner.student_id} value={learner.student_id}>
                  {learner.full_name}
                </option>
              ))}
            </select>
            <span className="text-xs text-(--ink-2)">takes the marks of</span>
            <select aria-label={`Study learner ${at + 1}`} value={row.study} onChange={(e) => choose(at, { study: e.target.value })} className={SELECT}>
              {studyLearners.map((learner) => (
                <option key={learner.student_id} value={learner.student_id}>
                  {learner.full_name} · {BAND_LABEL[learner.band]} · {learner.correct} of {learner.out_of}
                </option>
              ))}
            </select>
          </li>
        ))}
      </ul>
      <div>
        <button
          type="button"
          disabled={standIns.isPending}
          onClick={() => standIns.mutate(rows.map((row) => ({ student_id: row.student, study_student_id: row.study })))}
          className={buttonClass({ variant: "primary", size: "sm" })}
        >
          {standIns.isPending ? "Making their results…" : "Make their notes"}
        </button>
      </div>
      {standIns.isError ? (
        <p role="alert" className="text-sm text-(--danger)">
          {importErrorText(standIns.error.message)}
        </p>
      ) : null}
    </div>
  );
}
