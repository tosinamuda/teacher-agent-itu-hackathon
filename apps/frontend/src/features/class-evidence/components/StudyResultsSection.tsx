import { useState } from "react";

import { BAND_LABEL } from "@/features/learners/lib/bands";
import { buttonClass } from "@/shared/components/ui/Button";

import type { StudyLearnerResult, StudySource } from "../api/studyResults";
import {
  useImportStudyResults,
  useStudyResults,
  useStudySources,
} from "../hooks/useStudyResults";
import { importErrorText } from "../lib/importErrors";
import { StandInsPanel } from "./StandInsPanel";

const learnerCount = (n: number): string =>
  `${n} ${n === 1 ? "learner" : "learners"}`;

function ResultRow({ learner }: { learner: StudyLearnerResult }) {
  const codes = [
    ...new Set(
      learner.objectives.flatMap((objective) => objective.misconceptions),
    ),
  ];
  return (
    <li className="flex items-center gap-4 border-t border-(--line) px-4 py-3 first:border-t-0">
      <span className="flex min-w-0 flex-1 flex-col">
        <span className="text-sm font-semibold text-(--ink)">
          {learner.full_name}
        </span>
        <span className="text-xs text-(--ink-2)">
          Marked {learner.correct} of {learner.out_of} · teacher&apos;s total{" "}
          {learner.teacher_total}
          {codes.length > 0 ? ` · ${codes.join(", ")}` : ""}
        </span>
      </span>
      <span className="text-sm text-(--ink-2)">{BAND_LABEL[learner.band]}</span>
    </li>
  );
}

function ImportPanel({
  lessonPeriodId,
  lesson,
}: {
  lessonPeriodId: string;
  lesson: { title: string; week: number } | null;
}) {
  const sources = useStudySources(lessonPeriodId, true);
  const importResults = useImportStudyResults(lessonPeriodId);
  const [chosen, setChosen] = useState("");
  const list: StudySource[] = (sources.data ?? []).filter((source) => source.fits);
  const selected = chosen || list[0]?.plan_version_id || "";

  return (
    <div className="flex flex-col gap-3 border border-(--line) bg-(--surface) p-4">
      {lesson ? (
        <p className="text-sm text-(--ink)">
          <span className="text-(--ink-2)">Importing onto this lesson: </span>
          <span className="font-semibold">{lesson.title}</span>
          <span className="text-(--ink-2)"> · week {lesson.week}</span>
        </p>
      ) : null}
      <p className="text-sm text-(--ink)">
        Bring in the marks from the evaluation&apos;s classwork. Each learner is
        placed from how they did on this lesson&apos;s objectives. Only a lesson
        whose objectives this plan has is offered.
      </p>
      {sources.isError ? (
        <p className="text-sm text-(--danger)">
          Couldn&apos;t load the evaluation&apos;s lessons.
        </p>
      ) : null}
      {list.length > 0 ? (
        <div className="flex flex-wrap items-center gap-2">
          <label className="sr-only" htmlFor="study-source">
            Take the marks from
          </label>
          <select
            id="study-source"
            value={selected}
            onChange={(event) => setChosen(event.target.value)}
            className="max-w-full min-w-0 border border-(--line-2) bg-(--surface) px-2 py-1.5 text-sm text-(--ink)"
          >
            {list.map((source) => (
              <option key={source.plan_version_id} value={source.plan_version_id}>
                {source.lesson_title} · {learnerCount(source.learners)}
              </option>
            ))}
          </select>
          <button
            type="button"
            disabled={!selected || importResults.isPending}
            onClick={() => importResults.mutate(selected)}
            className={buttonClass({ variant: "primary", size: "sm" })}
          >
            {importResults.isPending ? "Importing…" : "Import class results"}
          </button>
        </div>
      ) : sources.isLoading ? null : (
        <p className="text-sm text-(--ink-2)">
          No lesson of the evaluation has the objectives of this lesson&apos;s plan. Reuse the plan
          of one of them first.
        </p>
      )}
      {importResults.isError ? (
        <p role="alert" className="text-sm text-(--danger)">
          {importErrorText(importResults.error.message)}
        </p>
      ) : null}
    </div>
  );
}

/** The evaluation's marked classwork on this lesson: each learner's band, or the way to bring it in. */
export function StudyResultsSection({
  lessonPeriodId,
  planApproved,
  classLearners,
  lesson = null,
}: {
  lessonPeriodId: string;
  planApproved: boolean;
  /** The lesson the marks are imported onto, named so the right evaluation lesson can be chosen. */
  lesson?: { title: string; week: number } | null;
  classLearners: { student_id: string; full_name: string; answered: boolean }[];
}) {
  const results = useStudyResults(lessonPeriodId);
  const imported = results.data?.imported ?? false;

  if (results.isLoading) return null;
  if (!imported && !planApproved) return null;

  return (
    <section
      className="flex flex-col gap-3"
      aria-label="Class results from the evaluation"
    >
      <h2 className="text-base font-semibold text-(--ink)">
        Class results from the evaluation
      </h2>
      {imported ? (
        <>
          <details className="group border border-(--line) bg-(--surface)">
            <summary className="flex cursor-pointer list-none items-center gap-3 px-4 py-3 text-sm text-(--ink) [&::-webkit-details-marker]:hidden">
              <span className="flex-1">
                Imported from the evaluation · {learnerCount(results.data?.learners.length ?? 0)}
              </span>
              <span className="text-xs text-(--ink-2) underline group-open:hidden">Show their marks</span>
              <span className="hidden text-xs text-(--ink-2) underline group-open:inline">Hide</span>
            </summary>
            <ul className="border-t border-(--line)">
              {results.data?.learners.map((learner) => (
                <ResultRow key={learner.student_id} learner={learner} />
              ))}
            </ul>
          </details>
          <StandInsPanel
            lessonPeriodId={lessonPeriodId}
            classLearners={classLearners}
            studyLearners={results.data?.learners ?? []}
          />
        </>
      ) : (
        <ImportPanel lessonPeriodId={lessonPeriodId} lesson={lesson} />
      )}
    </section>
  );
}
