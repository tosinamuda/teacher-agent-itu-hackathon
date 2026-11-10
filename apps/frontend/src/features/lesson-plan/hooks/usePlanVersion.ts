import { useQuery } from "@tanstack/react-query";

import { apiFetch } from "@/shared/api/client";

import type { PlanGenerationResponse } from "./usePlanGenerator";

/** One frozen plan version, as the lesson-plan endpoint returns it. */
export function usePlanVersion(planVersionId: string | null | undefined) {
  return useQuery({
    queryKey: ["plan", planVersionId],
    queryFn: () =>
      apiFetch<PlanGenerationResponse>(
        `/artefacts/lesson-plans/${planVersionId}`,
      ),
    enabled: Boolean(planVersionId),
  });
}
