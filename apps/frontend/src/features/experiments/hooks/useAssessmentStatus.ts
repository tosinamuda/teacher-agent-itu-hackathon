import { useQuery } from "@tanstack/react-query";

import { listAssessmentStatus } from "../lib/api";

/**
 * Which of the given lessons already have an exit assessment (batched). Drives
 * the lesson-prep "create assessment" step state and keeps a lesson in the queue
 * until its assessment has been created.
 */
export const useAssessmentStatus = (planVersionIds: string[], enabled: boolean) =>
  useQuery({
    queryKey: ["assessmentStatus", [...planVersionIds].sort()],
    queryFn: () => listAssessmentStatus(planVersionIds),
    enabled: enabled && planVersionIds.length > 0,
  });
