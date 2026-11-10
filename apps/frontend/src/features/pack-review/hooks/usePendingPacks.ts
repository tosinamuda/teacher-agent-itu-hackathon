import { useQuery } from "@tanstack/react-query";

import { listPendingPacks } from "../api/packReview";

/**
 * Loads the teacher review queue: per-student packs awaiting approval, newest
 * first. Optionally scoped to one lesson (plan_version_id).
 */
export function usePendingPacks(planVersionId?: string, status: "pending" | "approved" = "pending") {
  const query = useQuery({
    queryKey: ["pendingPacks", planVersionId ?? "all", status],
    queryFn: () => listPendingPacks(planVersionId, status),
  });

  return {
    packs: query.data ?? [],
    isLoading: query.isLoading,
    isError: query.isError,
    refetch: query.refetch,
  };
}
