import { useExperiment } from "@/features/experiments/hooks/useExperiments";
import { useExperimentStory } from "@/features/experiments/hooks/useExperimentStory";
import type {
  ExperimentConditionRun,
  ExperimentExecution,
  ExperimentFocalCase,
} from "@/features/experiments/lib/experiments";

const succeeded = (run: ExperimentConditionRun) =>
  Boolean(run.artefact_id) && /succeed|complete|done/i.test(run.status);

const ofHypothesis = (executions: ExperimentExecution[], hypothesis: string) =>
  executions.filter((execution) => execution.hypothesis === hypothesis);

/**
 * One lesson's record as the walkthrough reads it: its draws, the note each condition and
 * draw produced, and its focal learners with their two notes.
 */
export function useLessonRecord(experimentId: string | undefined) {
  const experiment = useExperiment(experimentId ?? "").data;
  const executions = experiment?.executions ?? [];
  const h1 = ofHypothesis(executions, "H1").sort((a, b) => a.attempt_number - b.attempt_number);
  const h2Runs = ofHypothesis(executions, "H2").flatMap(
    (execution) => execution.condition_runs ?? [],
  );
  const learners: ExperimentFocalCase[] = ofHypothesis(executions, "H2")
    .flatMap((execution) => execution.focal_cases ?? [])
    .sort((a, b) => a.learner_id.localeCompare(b.learner_id));

  const noteOf = (condition: string, draw: number): string | undefined =>
    h1
      .find((execution) => execution.attempt_number === draw)
      ?.condition_runs?.find((run) => run.condition_code === condition && succeeded(run))
      ?.artefact_id ?? undefined;
  const learnerNote = (learnerId: string, condition: "P0" | "P1"): string | undefined =>
    h2Runs.find(
      (run) => run.learner_id === learnerId && run.condition_code === condition && succeeded(run),
    )?.artefact_id ?? undefined;

  return {
    experiment,
    draws: h1.map((execution) => execution.attempt_number),
    conditions: [
      ...new Set(
        h1.flatMap((execution) => (execution.condition_runs ?? []).map((r) => r.condition_code)),
      ),
    ].sort(),
    learners,
    noteOf,
    learnerNote,
  };
}

export type LessonRecord = ReturnType<typeof useLessonRecord>;

/** The lesson's objectives as the study's plan states them. */
export function useLessonObjectives(experimentId: string | undefined) {
  const story = useExperimentStory(experimentId).data;
  return story?.lesson_plan?.lesson_plan_objectives?.map((objective) => ({
    id: objective.lesson_objective_id ?? "",
    text: objective.objective_text ?? "",
  })) ?? (story ? [] : undefined);
}
