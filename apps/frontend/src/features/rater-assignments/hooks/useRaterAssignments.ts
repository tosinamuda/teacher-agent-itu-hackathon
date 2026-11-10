import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  assignRaterAudit,
  assignRaterBundle,
  assignRaterH1,
  assignRaterH2,
  getExperimentAssignments,
  listRaters,
} from "../api";

/** Every rater profile (cached 60s — picker reuses across slots). */
export function useRaters() {
  return useQuery({
    queryKey: ["evaluation-raters"],
    queryFn: () => listRaters(),
    staleTime: 60_000,
  });
}

/** The assignment view for one experiment. */
export function useExperimentAssignments(experimentId: string) {
  return useQuery({
    queryKey: ["experiment-assignments", experimentId],
    queryFn: () => getExperimentAssignments(experimentId),
    enabled: Boolean(experimentId),
  });
}

/** Assign a rater to a slot; invalidates the experiment view so it refetches. */
export function useAssignH1(experimentId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ raterId, lessonPeriodId }: { raterId: string; lessonPeriodId: string }) =>
      assignRaterH1(experimentId, raterId, lessonPeriodId),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: ["experiment-assignments", experimentId],
      });
    },
  });
}

export function useAssignH2(experimentId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ raterId, focalCaseId }: { raterId: string; focalCaseId: string }) =>
      assignRaterH2(experimentId, raterId, focalCaseId),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: ["experiment-assignments", experimentId],
      });
    },
  });
}

export function useAssignAudit(experimentId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      auditItemId,
      raterId,
      isAdjudicator,
    }: {
      auditItemId: string;
      raterId: string;
      isAdjudicator: boolean;
    }) => assignRaterAudit(auditItemId, raterId, isAdjudicator),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: ["experiment-assignments", experimentId],
      });
    },
  });
}

/** Assign a rater to the experiment's whole scope in one action (idempotent). */
export function useAssignBundle(experimentId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ raterId, includeAudit }: { raterId: string; includeAudit: boolean }) =>
      assignRaterBundle(experimentId, raterId, includeAudit),
    onSuccess: () => {
      void queryClient.invalidateQueries({
        queryKey: ["experiment-assignments", experimentId],
      });
    },
  });
}
