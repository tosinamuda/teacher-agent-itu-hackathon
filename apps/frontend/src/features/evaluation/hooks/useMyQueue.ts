import { useQuery } from "@tanstack/react-query";

import { getMyQueue } from "../api";

/** Loads the actor-rater's assignments grouped by hypothesis (Phase H).
 *
 *  ``enabled`` lets the caller skip the fetch when the actor isn't a rater
 *  (e.g. a teacher or admin landed on the home — the queue endpoint exists
 *  but returns 403 for non-rater roles, and there's no point asking).
 */
export function useMyQueue(enabled: boolean) {
  return useQuery({
    queryKey: ["evaluation", "my-queue"],
    queryFn: getMyQueue,
    enabled,
    staleTime: 30_000,
  });
}
