import { Link } from "@/shared/router";

import { Card } from "@/shared/components/ui/Card";
import { LessonNoteSection } from "@/features/content/components/LessonNoteSection";
import { SessionPlanView } from "@/features/lesson-plan/components/SessionPlanView";
import { usePlanVersion } from "@/features/lesson-plan/hooks/usePlanVersion";

import { useDownloadLessonPlanPdf } from "../hooks/useDownloadLessonPlanPdf";
import { useExperiment } from "../hooks/useExperiments";

/**
 * Researcher-facing READ-ONLY preview of the lesson plan attached to an
 * experiment. Resolves the experiment's `plan_version_id`, fetches the plan
 * via the existing lesson-plan endpoint, and renders it with `SessionPlanView`
 * — the same component the teacher edit page uses, just without the edit
 * affordances around it.
 */
export function LessonPlanPreviewPage({ experimentId }: { experimentId: string }) {
  const experimentQuery = useExperiment(experimentId);
  const experiment = experimentQuery.data;
  const planVersionId = experiment?.plan_version_id;

  const planQuery = usePlanVersion(planVersionId);
  const downloadPdf = useDownloadLessonPlanPdf(planVersionId);

  if (experimentQuery.isLoading || planQuery.isLoading) {
    return (
      <main className="w-full py-4">
        <Card padding="lg">
          <p className="text-sm text-(--muted)">Loading lesson plan…</p>
        </Card>
      </main>
    );
  }

  if (!experiment) {
    return (
      <main className="w-full py-4">
        <Card padding="lg">
          <p className="text-sm text-(--muted)">Experiment not found.</p>
        </Card>
      </main>
    );
  }

  if (!planVersionId) {
    return (
      <main className="w-full py-4">
        <Card padding="lg" className="space-y-2">
          <h1 className="text-xl font-semibold text-(--ink)">No lesson plan attached</h1>
          <p className="text-sm text-(--muted)">
            This experiment doesn&apos;t reference a lesson-plan version yet.
          </p>
        </Card>
      </main>
    );
  }

  if (planQuery.isError || !planQuery.data) {
    return (
      <main className="w-full py-4">
        <Card padding="lg" className="space-y-2">
          <h1 className="text-xl font-semibold text-(--ink)">Couldn&apos;t load the lesson plan</h1>
          <p className="text-sm text-(--muted)">Plan version: {planVersionId}</p>
          <Link
            className="text-sm font-semibold text-(--accent-deep) hover:underline"
            href={`/research/experiments/${experimentId}`}
          >
            Back to Overview
          </Link>
        </Card>
      </main>
    );
  }

  const plan = planQuery.data;
  return (
    <main className="flex w-full flex-col gap-6 py-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <h2 className="text-lg font-semibold text-(--ink)" title={plan.version_id ?? planVersionId}>
          Lesson plan
        </h2>
        <button
          type="button"
          disabled={downloadPdf.isPending}
          onClick={() => downloadPdf.mutate()}
          className="text-sm text-(--muted) hover:text-(--ink) disabled:opacity-60"
        >
          {downloadPdf.isPending ? "Exporting…" : "PDF"}
        </button>
      </div>

      <SessionPlanView sessionPlan={plan.session_plan} />
      <LessonNoteSection planVersionId={planVersionId} steps={plan.session_plan.steps} />
    </main>
  );
}
