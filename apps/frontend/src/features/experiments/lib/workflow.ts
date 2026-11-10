/**
 * TypeScript shapes for the `/experiments/{id}/workflow` endpoint.
 *
 * Mirrors `apps/backend/src/app/domains/experiments/api/workflow_schemas.py`. The
 * derivation logic that used to live in `services/workflow.ts` has moved to
 * the Python `workflow_service.py` — this file only types the wire payload.
 */

export type WorkflowStatusKind =
  | "done"
  | "in_progress"
  | "ready"
  | "pending"
  | "failed"
  | "not_applicable";

/** One row inside a phase. */
export type WorkflowItem = {
  id: string;
  label: string;
  status: WorkflowStatusKind;
  count?: string | null;
  /** ISO datetime string of last activity for this row. */
  timestamp?: string | null;
  /** Drill-through target relative to the experiment base path. */
  href?: string | null;
  /** Verb-specific button label (e.g. "Preview C0 pack", "Review decisions").
   *  Wire field name is snake_case to match the rest of the API surface. */
  action_label?: string | null;
  reason?: string | null;
};

/** One phase of the protocol — typically grouped 1–5 items. */
export type WorkflowPhase = {
  id: string;
  title: string;
  description?: string | null;
  items: WorkflowItem[];
};

/** Backend-computed "what should the researcher do next" suggestion. */
export type WorkflowNextAction = {
  label: string;
  href?: string | null;
};

/** Top-level rollup feeding the progress bar above the accordion. */
export type WorkflowSummary = {
  done: number;
  total: number;
  pct: number;
};

/** The complete workflow view, one HTTP round-trip. */
export type WorkflowSnapshot = {
  experiment_id: string;
  phases: WorkflowPhase[];
  summary: WorkflowSummary;
  next_action?: WorkflowNextAction | null;
  attention: WorkflowItem[];
};
