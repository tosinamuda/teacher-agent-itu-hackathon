import { Link } from "@/shared/router";
import { useMemo } from "react";

import { Card } from "@/shared/components/ui/Card";
import { Section } from "@/shared/components/ui/Section";

import { ExperimentConditionGrid } from "../components/ExperimentConditionGrid";
import { ExperimentExecutionHistory } from "../components/ExperimentExecutionHistory";
import { ExperimentFocalLearnerPicker } from "../components/ExperimentFocalLearnerPicker";
import { ExperimentGenerationPanel } from "../components/ExperimentGenerationPanel";
import { ExperimentPlanGate } from "../components/ExperimentPlanGate";
import { ExperimentPacketTable } from "../components/ExperimentPacketTable";
import { H2LearnerTable } from "../components/H2LearnerTable";
import { StudyDraws } from "../components/StudyDraws";
import {
  useExperiment,
  useExportExperimentPackets,
  useFollowExecution,
  useLaunchExperimentExecution,
  useRetryExperimentCondition,
  useUpdateExperimentFocalLearners,
} from "../hooks/useExperiments";
import { useDownloadPackPdf } from "../hooks/useDownloadLessonPlanPdf";
import { useSyntheticProgress } from "../hooks/useSyntheticProgress";
import { Hypothesis } from "../lib/experiments";
import { studyDraws, studyRunOf } from "../lib/studyRecord";

type ExperimentHypothesisLabPageProps = {
  experimentId: string;
  hypothesis: Hypothesis;
};

/**
 * One researcher lab lane (H1 or H2). Reframed around the *generation flow*:
 * one canonical generation (latest attempt), its teacher-gate state, and the
 * produced condition packs — not a repeatable "launch" button that piles up
 * attempts. Prior attempts are demoted to a collapsed history.
 */
export function ExperimentHypothesisLabPage({
  experimentId,
  hypothesis,
}: ExperimentHypothesisLabPageProps) {
  const experimentQuery = useExperiment(experimentId);
  const experiment = experimentQuery.data ?? null;

  // Latest-first so [0] is the canonical "current" generation, deterministically.
  const executions = useMemo(
    () =>
      (experiment?.executions ?? [])
        .filter((item) => item.hypothesis === hypothesis)
        .slice()
        .sort((a, b) => (b.attempt_number ?? 0) - (a.attempt_number ?? 0)),
    [experiment?.executions, hypothesis],
  );
  const latest = executions[0] ?? null;

  // Conditions that failed with NO succeeded run for the same code — drives the
  // partial-vs-full failure messaging on the panel (a partial run is recovered
  // per condition, not by re-running the whole set). Computed before any early
  // return so the hook order stays stable.
  const failedConditions = useMemo(() => {
    const succeeded = new Set<string>();
    const failed = new Set<string>();
    for (const run of latest?.condition_runs ?? []) {
      if (/succeed|complete|done/i.test(run.status)) succeeded.add(run.condition_code);
      else if (run.status.toLowerCase().includes("fail")) failed.add(run.condition_code);
    }
    return [...failed].filter((code) => !succeeded.has(code)).sort();
  }, [latest?.condition_runs]);

  const launchMutation = useLaunchExperimentExecution(experimentId);
  const exportMutation = useExportExperimentPackets(latest?.execution_id ?? null);
  const retryMutation = useRetryExperimentCondition(experimentId);
  const packDownload = useDownloadPackPdf();
  // Live per-condition generation progress over the websocket (the same stream
  // the Live tab uses). The page learns that generation ended from its job, so it
  // refreshes even when the socket cannot connect.
  const liveProgress = useSyntheticProgress(experimentId).generation;
  useFollowExecution(experimentId, latest?.execution_id ?? null);
  const focalMutation = useUpdateExperimentFocalLearners(experimentId);
  const selectedFocalLearnerIds = useMemo(
    () => (experiment?.selected_focal_learners ?? []).map((item) => item.learner_id),
    [experiment?.selected_focal_learners],
  );

  if (experimentQuery.isLoading) {
    return (
      <main className="w-full py-8">
        <p className="text-sm text-[color:var(--muted)]">Loading {hypothesis} lab…</p>
      </main>
    );
  }

  if (experimentQuery.isError || !experiment) {
    return (
      <main className="w-full py-8">
        <Card padding="lg">
          <h1 className="text-2xl font-semibold text-[color:var(--ink)]">Experiment not found</h1>
          <p className="mt-2 text-sm text-[color:var(--muted)]">
            We could not load the requested {hypothesis} lab.
          </p>
          <Link
            className="mt-4 inline-flex text-sm font-semibold text-[color:var(--accent-deep)] hover:underline"
            href="/research"
          >
            Back to research
          </Link>
        </Card>
      </main>
    );
  }

  const baseHref = `/research/experiments/${experiment.experiment_id}`;
  const conditionRuns = latest?.condition_runs ?? [];
  const packets = latest?.packets ?? [];
  // The experiment's own plan must be authored + frozen by the teacher before H1
  // can generate. H2 always follows a frozen plan, so its gate is implicitly met.
  const planFrozen = Boolean(experiment.plan_version_id && experiment.baseline_approved_by);
  // An ended experiment's lesson is concluded: its record is read, never regenerated.
  const concluded = experiment.lifecycle_status === "ended";
  const draws = hypothesis === "H1" ? studyDraws(executions) : null;
  const fromTheStudy = (experiment.executions ?? []).some((item) => studyRunOf(item) !== null);

  const generate = () => {
    void launchMutation.mutateAsync({ hypothesis });
  };

  return (
    <div className="flex w-full flex-col gap-6 py-4">
      {concluded ? null : (
        <p className="text-sm text-(--muted)">
          {hypothesis === "H1"
            ? "Curriculum alignment: C0–C3 against the approved baseline; C4 is the teacher-reviewed class note."
            : "Personalisation: each focal learner's P0 base against their P1."}
        </p>
      )}

      {concluded ? (
        hypothesis === "H2" && !latest ? (
          <p className="text-sm text-(--ink-2)">
            {fromTheStudy ? "Not in the study's Part 2." : "H2 was not run before this experiment ended."}
          </p>
        ) : null
      ) : hypothesis === "H1" && !planFrozen ? (
        <ExperimentPlanGate
          experimentId={experiment.experiment_id}
          planVersionId={experiment.plan_version_id}
          baselineApprovedBy={experiment.baseline_approved_by}
        />
      ) : (
        <ExperimentGenerationPanel
          hypothesis={hypothesis}
          readiness={experiment.readiness}
          latest={latest}
          baseHref={baseHref}
          isGenerating={launchMutation.isPending}
          isExporting={exportMutation.isPending}
          exportedPackets={exportMutation.data?.packet_count ?? null}
          exportFailed={exportMutation.isError}
          liveProgress={liveProgress}
          failedConditions={failedConditions}
          onGenerate={generate}
          onExport={() => exportMutation.mutate()}
        />
      )}

      {hypothesis === "H2" && !concluded ? (
        <ExperimentFocalLearnerPicker
          candidates={experiment.focal_learner_candidates ?? []}
          isSaving={focalMutation.isPending}
          onSave={(learnerIds) => focalMutation.mutateAsync(learnerIds).then(() => undefined)}
          selectedLearnerIds={selectedFocalLearnerIds}
        />
      ) : null}

      {hypothesis === "H2" && latest ? (
        <H2LearnerTable
          focalCases={latest.focal_cases ?? []}
          runs={conditionRuns}
          experimentBaseHref={baseHref}
        />
      ) : null}

      {/* H1's condition packs — full width, no wasted column. */}
      {draws ? (
        <StudyDraws
          draws={draws}
          experimentBaseHref={baseHref}
          onExportPack={(artefactId) => packDownload.mutate(artefactId)}
          exportingArtefactId={packDownload.isPending ? packDownload.variables : null}
        />
      ) : hypothesis === "H1" && conditionRuns.length > 0 ? (
        <Section title="Conditions" aside="C0–C3, and C4 once the teacher has reviewed it">
          <ExperimentConditionGrid
            runs={conditionRuns}
            experimentBaseHref={baseHref}
            onRetry={(code) => retryMutation.mutate(code)}
            retryingCode={retryMutation.isPending ? retryMutation.variables : null}
            onExportPack={(artefactId) => packDownload.mutate(artefactId)}
            exportingArtefactId={packDownload.isPending ? packDownload.variables : null}
            c4Approved={experiment.readiness.base_pack_approved}
          />
        </Section>
      ) : null}

      {packets.length > 0 ? (
        <Section title={`${hypothesis} evaluation packets`} aside={`${packets.length} packets`}>
          <ExperimentPacketTable packets={packets} experimentBaseHref={baseHref} />
        </Section>
      ) : null}

      {/* Prior attempts demoted to a collapsed disclosure (not a prominent list). */}
      {executions.length > 1 && !draws ? (
        <details className="rounded-none border border-dashed border-(--line) px-4 py-2 text-sm">
          <summary className="cursor-pointer font-semibold text-(--ink)">
            Previous attempts ({executions.length - 1})
          </summary>
          <p className="mt-1 mb-2 text-xs text-(--muted)">
            Only the latest attempt is used for results. Older attempts are kept for provenance.
          </p>
          <ExperimentExecutionHistory
            executions={executions.slice(1)}
            onSelect={() => undefined}
            selectedExecutionId={null}
            title="Older attempts"
          />
        </details>
      ) : null}
    </div>
  );
}
