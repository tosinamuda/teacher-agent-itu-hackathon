import { Link } from "@/shared/router";

import { Card } from "@/shared/components/ui/Card";
import { Part2Review } from "@/features/study-review/Part2Review";

import { useExperiment } from "../hooks/useExperiments";
import { objectiveStates } from "../lib/learnerState";

/**
 * One focal learner's two revision notes compared, read only, as the study's raters compared
 * them: objective by objective, for the objectives the learner has marked class work for.
 */
export function LearnerPackComparePage({
  experimentId,
  learnerId,
}: {
  experimentId: string;
  learnerId: string;
}) {
  const experimentQuery = useExperiment(experimentId);
  const execution = (experimentQuery.data?.executions ?? [])
    .filter((item) => item.hypothesis === "H2")
    .sort((a, b) => (b.attempt_number ?? 0) - (a.attempt_number ?? 0))[0];
  const focalCase = execution?.focal_cases?.find((item) => item.learner_id === learnerId);
  const runs = (execution?.condition_runs ?? []).filter((run) => run.learner_id === learnerId);
  const p0 = runs.find((run) => run.condition_code === "P0");
  const p1 = runs.find((run) => run.condition_code === "P1");
  const states = objectiveStates(focalCase?.learner_state_snapshot);

  if (experimentQuery.isLoading) {
    return <p className="py-4 text-sm text-(--muted)">Loading…</p>;
  }
  if (!execution || !focalCase) {
    return (
      <Card padding="lg" className="space-y-2">
        <p className="text-sm text-(--muted)">
          This learner is not a focal learner of this experiment.
        </p>
        <Link
          href={`/research/experiments/${experimentId}/h2`}
          className="text-sm font-semibold text-(--accent-deep) hover:underline"
        >
          ← Back to H2
        </Link>
      </Card>
    );
  }

  return (
    <main className="flex w-full flex-col gap-8 py-6">
      <div className="space-y-1">
        <Link
          href={`/research/experiments/${experimentId}/h2`}
          className="text-sm text-(--muted) hover:text-(--ink)"
        >
          ← Focal learners
        </Link>
        <h2 className="text-lg font-semibold text-(--ink)">
          {focalCase.learner_name ?? focalCase.learner_id}
          <span className="ml-2 font-normal text-(--muted) capitalize">{focalCase.focal_type}</span>
        </h2>
      </div>

      {experimentQuery.data?.plan_version_id && p0?.artefact_id && p1?.artefact_id ? (
        <Part2Review
          planVersionId={experimentQuery.data.plan_version_id}
          learnerId={learnerId}
          p0Id={p0.artefact_id}
          p1Id={p1.artefact_id}
          states={states}
        />
      ) : (
        <Card padding="lg">
          <p className="text-sm text-(--muted)">
            This learner&apos;s two notes were not both made.
          </p>
        </Card>
      )}
    </main>
  );
}
