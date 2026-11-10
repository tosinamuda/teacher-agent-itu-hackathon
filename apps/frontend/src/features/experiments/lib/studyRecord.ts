import { ExperimentExecution } from "./experiments";

/** The published study run an execution was imported from, or null for one generated here. */
export function studyRunOf(execution: ExperimentExecution): string | null {
  const run = execution.runtime_snapshot?.study_run;
  return typeof run === "string" ? run : null;
}

/**
 * An imported study's executions, oldest first, when every one came from the study record.
 * The study's executions are its draws, each rated in full, so none supersedes another.
 */
export function studyDraws(executions: ExperimentExecution[]): ExperimentExecution[] | null {
  if (executions.length === 0 || !executions.every((execution) => studyRunOf(execution))) {
    return null;
  }
  return [...executions].sort((a, b) => a.attempt_number - b.attempt_number);
}
