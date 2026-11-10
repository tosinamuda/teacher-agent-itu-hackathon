import type { ExperimentExecution } from "../lib/experiments";

/**
 * Map the backend's structured `error_category` to a user-facing message.
 *
 * The category is classified server-side by exception *type* at the moment
 * of failure (see `app/domains/experiments/application/execution_errors.py`),
 * so the UI never inspects the raw `error_message` string. Older failed rows
 * (recorded before the column existed) have no category and fall back to a
 * generic message.
 */
const CATEGORY_MESSAGE: Record<string, string> = {
  inputs_missing:
    "Missing required inputs — the lesson plan or its approved version wasn't available.",
  persistence:
    "Couldn't save the generated packs — a database error. This is usually transient; try running the test again.",
  generation: "The generation pipeline failed. Try running the test again.",
  cancelled:
    "The run was interrupted before it finished (worker restart or timeout). Try running the test again.",
};

/** Whether an execution ended in failure — read from `status`, not the message. */
export function executionFailed(execution: ExperimentExecution): boolean {
  return execution.status === "failed";
}

/**
 * User-facing reason for a failed execution, from the structured category.
 * Returns null when the execution didn't fail (so callers can branch on it).
 */
export function executionErrorMessage(execution: ExperimentExecution): string | null {
  if (!executionFailed(execution)) return null;
  const category = execution.error_category ?? "";
  return CATEGORY_MESSAGE[category] ?? "This run didn't complete. See technical details below.";
}

/**
 * Friendly one-line summary for a FAILED condition run's raw error.
 *
 * Condition runs store the raw exception text (e.g. a litellm/openrouter dump),
 * not a structured category — so we pattern-match the common causes into plain
 * language. The raw text stays available behind a "details" disclosure.
 */
export function conditionErrorSummary(raw: string | null | undefined): string {
  if (!raw) return "This condition's generation failed.";
  const lower = raw.toLowerCase();
  if (/cannot connect|connection|timed out|timeout|ssl|unreachable|getaddrinfo|nodename/.test(lower)) {
    return "Couldn't reach the generation service (network/LLM connection). Retry this condition.";
  }
  if (/rate.?limit|\b429\b|quota|overloaded/.test(lower)) {
    return "The generation service was rate-limited or overloaded. Retry in a moment.";
  }
  if (/timeout|deadline/.test(lower)) {
    return "The generation timed out. Retry this condition.";
  }
  return "This condition's generation failed — retry it.";
}

/** Short id form (`EXE-xxxxxxxx…xxxx`) with the full id available via a tooltip. */
export function shortExecutionId(id: string): string {
  if (id.length <= 18) return id;
  return `${id.slice(0, 10)}…${id.slice(-6)}`;
}
