import { apiFetch } from "@/shared/api/client";

import type { CurriculumObjectiveOption } from "../manualDraft";
import type { PlanGenerationResponse } from "../hooks/usePlanGenerator";

/** Lesson identity + curriculum objectives for the manual-entry form (FD-01). */
export type ManualPlanContext = {
  session_id: string;
  subject: string;
  grade: string;
  term: string;
  week: number;
  topic: string;
  subtopic: string;
  curriculum_objectives: CurriculumObjectiveOption[];
};

export const fetchManualPlanContext = (
  sessionId: string,
): Promise<ManualPlanContext> =>
  apiFetch<ManualPlanContext>(
    `/artefacts/lesson-plans/manual/context?session_id=${encodeURIComponent(sessionId)}`,
  );

/** Persist a hand-entered plan as a new draft version. The server forces lesson
 *  identity + curriculum objectives; `sessionPlan` carries only the content. */
export const createManualPlan = (
  sessionId: string,
  sessionPlan: Record<string, unknown>,
  teacherId?: string,
): Promise<PlanGenerationResponse> =>
  apiFetch<PlanGenerationResponse>("/artefacts/lesson-plans/manual", {
    method: "POST",
    body: JSON.stringify({
      session_id: sessionId,
      teacher_id: teacherId ?? null,
      session_plan: sessionPlan,
    }),
  });

/** Author an EXPERIMENT's plan from hand-entered content — creates + links it to
 *  the experiment (so the H1 C0–C3 run picks it up), mirroring the automated
 *  POST /experiments/{id}/plan. Returns the updated experiment summary. */
export const createManualExperimentPlan = (
  experimentId: string,
  sessionPlan: Record<string, unknown>,
  originalDocumentAttachmentId?: string | null,
): Promise<{ experiment_id: string; plan_version_id: string | null }> =>
  apiFetch(`/experiments/${encodeURIComponent(experimentId)}/plan/manual`, {
    method: "POST",
    body: JSON.stringify({
      session_plan: sessionPlan,
      original_document_attachment_id: originalDocumentAttachmentId ?? null,
    }),
  });
