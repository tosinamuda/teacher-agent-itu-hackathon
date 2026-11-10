import { useMutation, useQueryClient } from "@tanstack/react-query";

import { EditableSessionPlan, manualEditPlan } from "../api/manualEdit";
import { PlanGenerationResponse } from "./usePlanGenerator";

/**
 * Persist a teacher's hand-edited plan as a new version, then mirror the result
 * into the ``["plan", planId]`` cache so the read-only view re-renders in place —
 * exactly how the revision chat updates the plan after an AI turn.
 */
export function useManualEdit(planId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (sessionPlan: EditableSessionPlan) =>
      manualEditPlan(planId, sessionPlan),
    onSuccess: (result: PlanGenerationResponse) => {
      queryClient.setQueryData<PlanGenerationResponse>(
        ["plan", planId],
        (old) =>
          old
            ? {
                ...old,
                session_plan: result.session_plan,
                version_id: result.version_id,
                version_status: "draft",
              }
            : result,
      );
      // The edit is a new version of the lesson's plan: its list of versions is read again.
      void queryClient.invalidateQueries({ queryKey: ["sessionPlans"] });
      // What the edited plan still leaves unmet is worked out on the server.
      void queryClient.invalidateQueries({ queryKey: ["plan", planId] });
      // A manual edit forks the revision history's head; drop the thread cache so
      // the next AI turn re-seeds from the edited version.
      void queryClient.invalidateQueries({
        queryKey: ["revisionThread", planId],
      });
    },
  });
}
