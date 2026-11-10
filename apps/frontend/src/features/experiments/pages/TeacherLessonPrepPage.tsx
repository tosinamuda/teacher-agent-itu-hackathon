import { Link } from "@/shared/router";

import { Card } from "@/shared/components/ui/Card";

import { LessonContentCard } from "@/features/content/components/LessonContentCard";

import { ExperimentAssessmentGate } from "../components/ExperimentAssessmentGate";
import { ExperimentBasePackGate } from "../components/ExperimentBasePackGate";
import { ExperimentLessonNoteGate } from "../components/ExperimentLessonNoteGate";
import { ExperimentPlanGate } from "../components/ExperimentPlanGate";
import { LessonPrepChecklist } from "../components/LessonPrepChecklist";
import { useAssessmentStatus } from "../hooks/useAssessmentStatus";
import { useExperimentSummary } from "../hooks/useExperiments";
import { usePendingStudentNotes } from "../hooks/usePendingStudentNotes";
import { useStudentNotesMade } from "../hooks/useStudentNotesMade";
import { lessonHeading } from "../lib/lessonHeading";

/** The class revision note of an experiment's lesson is its C4 pack, which step 5 builds. */
const MADE_BY_THE_JOURNEY = {
  "revision-note": "Made by “Create the class revision note” above, once your lesson note is accepted.",
} as const;

/**
 * One lesson's preparation workspace: the full step-by-step checklist plus the
 * action card for whichever step is current (author/accept the plan, review the
 * class revision note). Reached by opening a lesson from the "Lessons to prepare"
 * list. The research conditions run in the background and never surface here.
 */
export function TeacherLessonPrepPage({ experimentId }: { experimentId: string }) {
  const experimentQuery = useExperimentSummary(experimentId);
  const pendingNotesQuery = usePendingStudentNotes(true);
  const notesMadeQuery = useStudentNotesMade(true);
  const experiment = experimentQuery.data;
  const planVersionId = experiment?.plan_version_id ?? null;
  const assessmentQuery = useAssessmentStatus(planVersionId ? [planVersionId] : [], true);

  const studentNotes = {
    made: planVersionId != null ? (notesMadeQuery.data?.get(planVersionId) ?? 0) : 0,
    awaiting:
      planVersionId != null
        ? (pendingNotesQuery.data ?? []).filter((note) => note.plan_version_id === planVersionId)
            .length
        : 0,
  };
  const assessmentRow = (assessmentQuery.data ?? []).find(
    (row) => row.plan_version_id === planVersionId,
  );
  const assessment = {
    ready: Boolean(assessmentRow?.has_assessment),
    sent: Boolean(assessmentRow?.released),
  };

  return (
    <main className="mx-auto flex w-full max-w-3xl flex-col gap-5 px-6 py-8">
      <Link
        href="/research/teacher/experiment-plans"
        className="text-sm text-(--accent-deep) hover:underline"
      >
        ← All lessons to prepare
      </Link>

      {experimentQuery.isLoading || !experiment ? (
        <Card padding="lg">
          <p className="text-sm text-(--muted)">Loading lesson…</p>
        </Card>
      ) : (
        <>
          <header className="space-y-1">
            <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-(--accent-deep)">
              Lesson preparation
            </p>
            <h1 className="text-2xl font-semibold text-(--ink)">{lessonHeading(experiment).name}</h1>
            <p className="text-sm text-(--muted)">{lessonHeading(experiment).where}</p>
          </header>

          <Card padding="lg" className="space-y-5">
            <LessonPrepChecklist
              experiment={experiment}
              studentNotes={studentNotes}
              assessment={assessment}
            />
            <ExperimentPlanGate
              experimentId={experiment.experiment_id}
              planVersionId={experiment.plan_version_id}
              baselineApprovedBy={experiment.baseline_approved_by}
              navigateToReviewOnAuthor
            />
            <ExperimentLessonNoteGate experiment={experiment} />
            <ExperimentBasePackGate experiment={experiment} />
            <ExperimentAssessmentGate experiment={experiment} assessment={assessment} />
          </Card>
          {experiment.plan_version_id && experiment.baseline_approved_by ? (
            <LessonContentCard
              planVersionId={experiment.plan_version_id}
              madeElsewhere={MADE_BY_THE_JOURNEY}
            />
          ) : null}
        </>
      )}
    </main>
  );
}
