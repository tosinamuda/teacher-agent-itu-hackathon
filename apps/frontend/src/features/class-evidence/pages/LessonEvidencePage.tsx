import { useState } from "react";

import { useLessonHome } from "@/features/lesson-home/hooks/useLessonHome";
import { waitingOn } from "@/features/lesson-home/lib/lessonHome";
import { BAND_LABEL } from "@/features/learners/lib/bands";
import { scoreText } from "@/features/learners/lib/learnerResults";
import { buttonClass } from "@/shared/components/ui/Button";
import { RightPanel, type NeedsItem } from "@/shared/components/workspace/RightPanel";
import { WorkspacePage } from "@/shared/components/workspace/WorkspacePage";
import { Link } from "@/shared/router";

import { StudyResultsSection } from "../components/StudyResultsSection";
import { useLessonEvidence } from "../hooks/useLessonEvidence";
import { FILTERS, evidenceCounts, filterEvidence, type EvidenceFilter } from "../lib/evidence";

function Chevron() {
  return (
    <svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true" className="text-(--ink-2)">
      <path d="M6 3.5L10.5 8 6 12.5" fill="none" stroke="currentColor" strokeWidth="1.5" />
    </svg>
  );
}

/** How the class answered one lesson's class test: each learner's score and band. */
export function LessonEvidencePage({ lessonPeriodId }: { lessonPeriodId: string }) {
  const [filter, setFilter] = useState<EvidenceFilter>("all");
  const evidence = useLessonEvidence(lessonPeriodId);
  const home = useLessonHome(lessonPeriodId);
  const counts = evidenceCounts(evidence.learners);
  const shown = filterEvidence(evidence.learners, filter);

  const needs: NeedsItem[] = waitingOn(home.rows.learners).map((row) => ({
    id: row.key,
    title: row.title,
    detail: row.detail,
    actions: row.action ? (
      <Link href={row.action.href} className={buttonClass({ variant: "secondary", size: "sm" })}>
        {row.action.label}
      </Link>
    ) : undefined,
  }));
  const panel = (
    <RightPanel
      needs={needs}
      agent={<p className="text-xs text-(--faint)">Each material has its own chat with the agent. Open a material to talk to it.</p>}
    />
  );

  return (
    <WorkspacePage panel={panel}>
      <div className="flex flex-col gap-5">
        <header className="flex flex-col gap-1">
          <h1 className="text-2xl font-semibold text-(--ink)">Class test evidence</h1>
          <p className="text-xs text-(--ink-2)">{home.lesson?.title ?? ""}</p>
        </header>

        <StudyResultsSection
          lessonPeriodId={lessonPeriodId}
          planApproved={Boolean(home.planVersionId)}
          lesson={home.lesson}
          classLearners={evidence.learners.map((learner) => ({
            student_id: learner.student_id,
            full_name: learner.full_name,
            answered: learner.last_test !== null,
          }))}
        />

        <div className="flex flex-wrap gap-2" role="group" aria-label="Show">
          {FILTERS.map(({ key, label }) => (
            <button
              key={key}
              type="button"
              aria-pressed={filter === key}
              onClick={() => setFilter(key)}
              className={`border px-3 py-1.5 text-xs ${
                filter === key ? "border-(--ink) bg-(--surface) text-(--ink)" : "border-(--line-2) text-(--ink-2)"
              }`}
            >
              {label} <span className="text-(--faint)">{counts[key]}</span>
            </button>
          ))}
        </div>

        {evidence.isError ? <p className="text-sm text-(--danger)">Couldn&apos;t load the evidence.</p> : null}
        {evidence.isLoading ? <p className="text-sm text-(--ink-2)">Loading…</p> : null}
        {shown.length > 0 ? (
          <ul className="border border-(--line) bg-(--surface)">
            {shown.map((learner) => (
              <li key={learner.student_id}>
                <Link
                  href={`/research/teacher/lessons/${lessonPeriodId}/evidence/${learner.student_id}`}
                  className="flex items-center gap-4 border-t border-(--line) px-4 py-3 first:border-t-0 hover:bg-(--sunken)"
                >
                  <span className="flex min-w-0 flex-1 flex-col">
                    <span className="text-sm font-semibold text-(--ink)">{learner.full_name}</span>
                    {learner.last_test ? (
                      <span className="text-xs text-(--ink-2)">
                        Scored {scoreText(learner.last_test.correct, learner.last_test.out_of)}
                      </span>
                    ) : null}
                  </span>
                  <span className="text-sm text-(--ink-2)">
                    {learner.last_test ? BAND_LABEL[learner.last_test.band] : "Not answered"}
                  </span>
                  <Chevron />
                </Link>
              </li>
            ))}
          </ul>
        ) : evidence.isLoading ? null : (
          <p className="text-sm text-(--ink-2)">Nobody to show for this filter.</p>
        )}
      </div>
    </WorkspacePage>
  );
}
