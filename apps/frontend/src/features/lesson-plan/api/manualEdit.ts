import { apiFetch } from "@/shared/api/client";

import type { PlanGenerationResponse } from "../hooks/usePlanGenerator";

/** The editable session-plan shape sent back on a manual edit (the full plan). */
export type EditableSessionPlan = PlanGenerationResponse["session_plan"];

/** Persist a teacher's hand-edited plan as a new chained draft version.
 *  ``planOrVersionId`` may be the plan_id or any version_id of the plan. */
export const manualEditPlan = (
  planOrVersionId: string,
  sessionPlan: EditableSessionPlan,
): Promise<PlanGenerationResponse> =>
  apiFetch<PlanGenerationResponse>(
    `/artefacts/lesson-plans/${encodeURIComponent(planOrVersionId)}/manual-edit`,
    {
      method: "POST",
      body: JSON.stringify({ session_plan: sessionPlan }),
    },
  );
