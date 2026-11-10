import { useMutation, useQuery } from "@tanstack/react-query";

import {
  createExperimentManualClasswork,
  deriveMisconceptions,
  fetchClassworkContext,
  fetchClassworkCoverage,
  type ClassworkItemPayload,
  type DeriveMisconceptionsItem,
} from "../api/manualClasswork";

/** The objectives + knowledge components + already-entered items the form needs. */
export function useClassworkContext(planVersionId: string) {
  return useQuery({
    queryKey: ["classworkContext", planVersionId],
    queryFn: () => fetchClassworkContext(planVersionId),
    enabled: Boolean(planVersionId),
  });
}

export function useClassworkCoverage(planVersionId: string, enabled = true) {
  return useQuery({
    queryKey: ["classworkCoverage", planVersionId],
    queryFn: () => fetchClassworkCoverage(planVersionId),
    enabled: enabled && Boolean(planVersionId),
  });
}

export function useCreateExperimentManualClasswork() {
  return useMutation({
    mutationFn: (input: { experimentId: string; items: ClassworkItemPayload[] }) =>
      createExperimentManualClasswork(input.experimentId, input.items),
  });
}

export function useDeriveMisconceptions() {
  return useMutation({
    mutationFn: (input: { planVersionId: string; items: DeriveMisconceptionsItem[] }) =>
      deriveMisconceptions(input.planVersionId, input.items),
  });
}
