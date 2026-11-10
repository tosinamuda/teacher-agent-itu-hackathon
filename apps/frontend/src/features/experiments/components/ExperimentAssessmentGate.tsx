import { Link } from "@/shared/router";

import { Button } from "@/shared/components/ui/Button";
import { Card } from "@/shared/components/ui/Card";

import { useCreateAssessment, useSendAssessment } from "../hooks/useExperiments";
import type { ExperimentSummary } from "../lib/experiments";

/**
 * The teacher's assessment steps, after plan acceptance: first create the short
 * exit assessment (with AI) or enter the real classwork by hand (FD-02), then send
 * (release) it so students can take it. Renders nothing until the plan is accepted
 * or once the assessment has been sent.
 */
export function ExperimentAssessmentGate({
  experiment,
  assessment,
}: {
  experiment: ExperimentSummary;
  assessment: { ready: boolean; sent: boolean };
}) {
  const planFrozen = Boolean(experiment.plan_version_id && experiment.baseline_approved_by);
  const create = useCreateAssessment(experiment.plan_version_id);
  const send = useSendAssessment(experiment.experiment_id, experiment.plan_version_id);

  if (!planFrozen || assessment.sent) return null;

  if (!assessment.ready) {
    return (
      <Card padding="lg" className="space-y-3 border border-(--line) bg-(--surface)">
        <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-(--accent-deep)">
          Assessment · ready to create
        </p>
        <p className="text-sm text-(--ink)">
          Create the short assessment your students will take. Their answers shape each
          student&apos;s personalised revision note.
        </p>
        {create.isError ? (
          <p className="text-sm text-(--danger-ink)">Couldn&apos;t create it — please try again.</p>
        ) : null}
        <div className="flex items-center gap-4">
          <Button variant="secondary" isLoading={create.isPending} onClick={() => create.mutate()}>
            Create the assessment
          </Button>
          <Link
            href={`/research/teacher/experiment-plans/${experiment.experiment_id}/classwork`}
            className="text-sm font-semibold text-(--accent-deep) hover:underline"
          >
            or enter the real classwork →
          </Link>
        </div>
      </Card>
    );
  }

  return (
    <Card padding="lg" className="space-y-3 border border-(--warning-ink)/30 bg-(--warning-tint)/30">
      <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-(--warning-ink)">
        Assessment · ready to send
      </p>
      <p className="text-sm text-(--ink)">
        Your assessment is ready. Send it to your students when you want them to take it —
        until then it stays hidden from them.
      </p>
      {send.isError ? (
        <p className="text-sm text-(--danger-ink)">Couldn&apos;t send it — please try again.</p>
      ) : null}
      <div className="flex items-center gap-4">
        <Button isLoading={send.isPending} onClick={() => send.mutate()}>
          Send the assessment to students
        </Button>
        <Link
          href={`/research/teacher/experiment-plans/${experiment.experiment_id}/responses`}
          className="text-sm font-semibold text-(--accent-deep) hover:underline"
        >
          or record results on paper →
        </Link>
      </div>
    </Card>
  );
}
