import { apiFetch } from "@/shared/api/client";

import { DiagnosticRevisionThread, PlanObjective, SubmitDiagnosticTurnResult } from "../types";

/** The lesson's plan as the class-test review reads it: its name and its objectives. */
export type ReviewedPlan = { title: string; objectives: PlanObjective[] };

type PlanResponse = {
  session_plan: {
    topic?: string | null;
    subtopic?: string | null;
    lesson_plan_objectives?: PlanObjective[];
  };
};

export const getReviewedPlan = async (planVersionId: string): Promise<ReviewedPlan> => {
  const { session_plan: plan } = await apiFetch<PlanResponse>(
    `/artefacts/lesson-plans/${encodeURIComponent(planVersionId)}`
  );
  return {
    title: plan.subtopic || plan.topic || "",
    objectives: plan.lesson_plan_objectives ?? [],
  };
};

/** Get or create the diagnostic revision thread for a lesson, with its items seed. */
export const createDiagnosticThread = (
  planVersionId: string
): Promise<DiagnosticRevisionThread> =>
  apiFetch<DiagnosticRevisionThread>("/artefact-revisions/threads", {
    method: "POST",
    body: JSON.stringify({ artefact_type: "diagnostic", subject_id: planVersionId }),
  });

/** Submit a teacher instruction; returns the new turn + the revised items. */
export const submitDiagnosticTurn = (
  threadId: string,
  payload: { instruction: string }
): Promise<SubmitDiagnosticTurnResult> =>
  apiFetch<SubmitDiagnosticTurnResult>(`/artefact-revisions/threads/${threadId}/turns`, {
    method: "POST",
    body: JSON.stringify(payload),
  });

