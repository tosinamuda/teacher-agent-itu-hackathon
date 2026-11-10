import { useMutation, useQuery } from "@tanstack/react-query";

import { approveLessonPlan } from "@/features/content/api/content";

import {
  createManualExperimentPlan,
  createManualPlan,
  fetchManualPlanContext,
} from "../api/manualCreate";

/** Load the lesson identity + curriculum objectives the manual form maps onto. */
export function useManualPlanContext(sessionId: string) {
  return useQuery({
    queryKey: ["manualPlanContext", sessionId],
    queryFn: () => fetchManualPlanContext(sessionId),
    enabled: Boolean(sessionId),
  });
}

export function useCreateManualPlan() {
  return useMutation({
    mutationFn: (input: {
      sessionId: string;
      sessionPlan: Record<string, unknown>;
      teacherId?: string;
    }) => createManualPlan(input.sessionId, input.sessionPlan, input.teacherId),
  });
}

export function useCreateExperimentManualPlan() {
  return useMutation({
    mutationFn: (input: {
      experimentId: string;
      sessionPlan: Record<string, unknown>;
      originalDocumentAttachmentId?: string | null;
    }) =>
      createManualExperimentPlan(
        input.experimentId,
        input.sessionPlan,
        input.originalDocumentAttachmentId,
      ),
  });
}

/** Freeze the plan the teacher just entered; they add their own classwork, so no class test. */
export function useApprovePlan() {
  return useMutation({
    mutationFn: (input: { versionId: string }) =>
      approveLessonPlan(input.versionId),
  });
}
