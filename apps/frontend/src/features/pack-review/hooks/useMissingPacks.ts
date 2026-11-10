import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { listMissingPacks, regenerateStudentPack } from "../api/packReview";

/**
 * Lists students who submitted a lesson's exit assessment but have no pack yet
 * (generation pending or failed), and exposes a regenerate mutation that re-runs the
 * same per-student worker. While a regeneration is in flight the list polls so a
 * student drops off as soon as their pack lands.
 */
export const useMissingPacks = (planVersionId: string | null) => {
  const queryClient = useQueryClient();
  const key = ["missingPacks", planVersionId ?? "none"];

  const query = useQuery({
    queryKey: key,
    queryFn: () => listMissingPacks(planVersionId ?? ""),
    enabled: Boolean(planVersionId),
  });

  const regenerate = useMutation({
    mutationFn: (studentId?: string) =>
      regenerateStudentPack(planVersionId ?? "", studentId),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: key });
      void queryClient.invalidateQueries({ queryKey: ["pendingPacks"] });
      // Refresh the generation-status badges so the just-queued attempt shows as
      // "generating…" immediately (polling only runs while something is in flight).
      void queryClient.invalidateQueries({
        queryKey: ["generationStatuses", planVersionId ?? "none"],
      });
    },
  });

  return {
    students: query.data ?? [],
    isLoading: query.isLoading,
    isError: query.isError,
    refetch: query.refetch,
    regenerate,
  };
};
