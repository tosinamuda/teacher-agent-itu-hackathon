import { Link } from "@/shared/router";
import { useRouter } from "@/shared/router";
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";

import { LessonPlanManualEditor } from "@/features/lesson-plan/components/LessonPlanManualEditor";
import { ContentChat } from "@/features/content-chat/ContentChat";
import { SessionPlanView } from "@/features/lesson-plan/components/SessionPlanView";
import { useManualEdit } from "@/features/lesson-plan/hooks/useManualEdit";
import { useTextSelection } from "@/features/lesson-plan/hooks/useTextSelection";
import {
  PlanGenerationResponse,
  usePlanGenerator,
} from "@/features/lesson-plan/hooks/usePlanGenerator";
import { apiFetch } from "@/shared/api/client";
import { Button } from "@/shared/components/ui/Button";
import { Card } from "@/shared/components/ui/Card";

import { useExperimentSummary, useFreezeExperimentPlan } from "../hooks/useExperiments";
import { lessonHeading } from "../lib/lessonHeading";

/**
 * Teacher's review-and-accept step for one lesson plan draft. Closes the
 * original "Author → ??? → Freeze" gap where the freeze action was offered
 * without any way to see what was being approved, and lets the teacher refine
 * the draft with AI feedback before accepting.
 *
 * Reuses the production lesson-plan components verbatim — SessionPlanView
 * (rendering) + RevisionChatPanel (select-and-instruct AI revision) — so the
 * teacher's authoring loop here is the same one they use in production. Accept
 * is the experiment ``freeze``, which now re-binds to whatever revised head
 * version the teacher arrived at.
 *
 * Surfaces no research-condition terminology (C0–C3, C4, hypothesis, study
 * pack) — to the teacher this is just "your lesson plan".
 */
export function TeacherExperimentPlanReviewPage({
  experimentId,
}: {
  experimentId: string;
}) {
  const experimentQuery = useExperimentSummary(experimentId);
  const experiment = experimentQuery.data;
  const planVersionId = experiment?.plan_version_id ?? null;
  const isAccepted = Boolean(experiment?.baseline_approved_by);

  // Resolve the plan_id from the bound version so the workspace below can key
  // its cache on plan_id — the key RevisionChatPanel writes revised versions to.
  const resolveQuery = useQuery({
    queryKey: ["plan", planVersionId],
    queryFn: () =>
      apiFetch<PlanGenerationResponse>(`/artefacts/lesson-plans/${planVersionId}`),
    enabled: Boolean(planVersionId),
  });
  const planId = resolveQuery.data?.plan_id ?? null;

  if (experimentQuery.isLoading) {
    return <Shell>{<Loading label="Loading lesson…" />}</Shell>;
  }
  if (!experiment) {
    return (
      <Shell>
        <Card padding="lg">
          <p className="text-sm text-(--muted)">Lesson not found.</p>
        </Card>
      </Shell>
    );
  }
  if (!planVersionId) {
    return (
      <Shell>
        <Card padding="lg" className="space-y-2">
          <h1 className="text-xl font-semibold text-(--ink)">No draft to review</h1>
          <p className="text-sm text-(--muted)">
            This lesson doesn&apos;t have a draft plan yet — author it from your
            lessons list and you&apos;ll land here.
          </p>
        </Card>
      </Shell>
    );
  }

  const heading = lessonHeading(experiment);

  return (
    <Shell>
      <header className="space-y-1">
        <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-(--accent)">
          Teacher · review &amp; refine
        </p>
        <h1 className="text-2xl font-semibold text-(--ink)">{heading.name}</h1>
        <p className="text-xs text-(--muted)">{heading.where}</p>
        <p className="text-sm text-(--muted)">
          Read the draft below. Edit it directly, or ask the assistant to revise it
          — then accept it when you&apos;re satisfied and study packs begin preparing
          for your students.
        </p>
      </header>

      {resolveQuery.isLoading || !planId ? (
        <Loading label="Loading draft plan…" />
      ) : (
        <PlanReviewWorkspace
          experimentId={experimentId}
          planId={planId}
          isAccepted={isAccepted}
        />
      )}
    </Shell>
  );
}

/**
 * The plan body + revision loop, keyed entirely on ``planId`` so a chat turn that changes the
 * plan refreshes ``["plan", planId]`` and re-renders it.
 */
function PlanReviewWorkspace({
  experimentId,
  planId,
  isAccepted,
}: {
  experimentId: string;
  planId: string;
  isAccepted: boolean;
}) {
  const router = useRouter();
  const { planData, isFetching } = usePlanGenerator(planId);
  const freeze = useFreezeExperimentPlan(experimentId);
  const manualEdit = useManualEdit(planId);
  const [editing, setEditing] = useState(false);
  const { selection, clear } = useTextSelection();

  const handleAccept = async () => {
    // Pass the current head version so the feedback-loop / manual revisions are
    // the ones that get frozen (not the version bound at first author).
    await freeze.mutateAsync(planData?.version_id ?? null);
    // Return to the lesson hub so the teacher sees the checklist advance.
    router.push(`/research/teacher/experiment-plans/${experimentId}`);
  };

  const handleSaveEdits = async (next: NonNullable<typeof planData>["session_plan"]) => {
    await manualEdit.mutateAsync(next);
    setEditing(false);
  };

  if (isFetching || !planData) {
    return <Loading label="Loading draft plan…" />;
  }

  if (editing) {
    return (
      <Card padding="lg" className="space-y-4">
        <div className="flex items-center justify-between border-b border-(--line) pb-3">
          <h3 className="text-base font-semibold text-(--ink)">Editing the plan</h3>
          <span className="text-xs text-(--muted)">
            Edits save as a new draft you can still refine or accept.
          </span>
        </div>
        <LessonPlanManualEditor
          sessionPlan={planData.session_plan}
          isSaving={manualEdit.isPending}
          error={
            manualEdit.isError
              ? manualEdit.error instanceof Error
                ? manualEdit.error.message
                : "Couldn't save your edits."
              : null
          }
          onSave={(next) => void handleSaveEdits(next)}
          onCancel={() => setEditing(false)}
        />
      </Card>
    );
  }

  return (
    <div className="space-y-5">
      <Card padding="lg" className="space-y-6">
        {!isAccepted ? (
          <div className="flex justify-end gap-2">
            <ContentChat contentId={planId} highlight={selection} onSent={clear} />
            <Button size="sm" variant="secondary" onClick={() => setEditing(true)}>
              Edit the plan
            </Button>
          </div>
        ) : null}
        <SessionPlanView sessionPlan={planData.session_plan} />
      </Card>

      {!isAccepted && planData.unmet_requirements?.length ? (
        <section className="space-y-2">
          <h2 className="text-sm font-semibold text-(--ink)">Not yet met</h2>
          <p className="text-sm text-(--muted)">
            Ask the agent in the chat to fix these, or accept the plan as it is.
          </p>
          <ul className="list-disc space-y-1 pl-5 text-sm text-(--ink-2)">
            {planData.unmet_requirements.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </section>
      ) : null}

      <div className="sticky bottom-4 z-10 flex flex-wrap items-center justify-between gap-3 border border-(--accent)/40 bg-(--accent-soft) px-4 py-3">
        {isAccepted ? (
          <p className="text-sm font-medium text-(--ink)">
            Accepted — study packs are now preparing for your students.
          </p>
        ) : (
          <p className="text-sm text-(--ink)">
            Once accepted, the plan locks in and study packs start preparing for your
            students.
          </p>
        )}
        <div className="flex items-center gap-3">
          {!isAccepted ? (
            <Button isLoading={freeze.isPending} onClick={() => void handleAccept()}>
              Accept the plan
            </Button>
          ) : null}
          <Link
            href={`/research/teacher/experiment-plans/${experimentId}`}
            className="text-sm font-semibold text-(--accent-deep) hover:underline"
          >
            Back to lesson
          </Link>
        </div>
      </div>
      {freeze.isError ? (
        <p className="text-sm text-(--danger-ink)">
          {freeze.error instanceof Error ? freeze.error.message : "Couldn't accept the plan."}
        </p>
      ) : null}
    </div>
  );
}

function Shell({ children }: { children: React.ReactNode }) {
  return (
    <main className="mx-auto flex w-full max-w-3xl flex-col gap-5 px-6 py-8">
      <Link
        href="/research/teacher/experiment-plans"
        className="self-start text-sm text-(--accent-deep) hover:underline"
      >
        ← Back to your lessons
      </Link>
      {children}
    </main>
  );
}

function Loading({ label }: { label: string }) {
  return (
    <Card padding="lg">
      <p className="text-sm text-(--muted)">{label}</p>
    </Card>
  );
}
