import { useQuery } from "@tanstack/react-query";

import { getReviewedPlan } from "../api/diagnosticReview";

/** The lesson's plan, so the class test names its lesson and each question's objective. */
export const useReviewedPlan = (planVersionId: string) =>
  useQuery({
    queryKey: ["reviewedPlan", planVersionId],
    queryFn: () => getReviewedPlan(planVersionId),
    enabled: Boolean(planVersionId),
  });
