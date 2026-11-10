import { useQuery } from "@tanstack/react-query";

import { listGenerationStatuses } from "../api/packReview";
import { StudentPackGenerationStatusRow } from "../types";

const IN_FLIGHT_STATUSES = new Set(["queued", "running"]);

export const isGenerationInFlight = (status?: string | null): boolean =>
  status != null && IN_FLIGHT_STATUSES.has(status);

/**
 * The teacher's generation queue for a lesson: each student's current attempt
 * (queued / running / succeeded / failed). Polls while any generation is still in
 * flight so a "generating…" badge flips to ready/failed on its own. Returns the rows
 * plus a by-student lookup so a caller can annotate its own list.
 */
export const useGenerationStatuses = (planVersionId: string | null) => {
  const query = useQuery({
    queryKey: ["generationStatuses", planVersionId ?? "none"],
    queryFn: () => listGenerationStatuses(planVersionId ?? ""),
    enabled: Boolean(planVersionId),
    refetchInterval: (q) =>
      (q.state.data ?? []).some((row) => isGenerationInFlight(row.status))
        ? 4000
        : false,
  });

  const byStudent = new Map<string, StudentPackGenerationStatusRow>();
  for (const row of query.data ?? []) byStudent.set(row.student_id, row);

  return {
    statuses: query.data ?? [],
    byStudent,
    isLoading: query.isLoading,
    refetch: query.refetch,
  };
};
