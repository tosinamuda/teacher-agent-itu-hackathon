import { useQuery } from "@tanstack/react-query";

import { apiFetch } from "@/shared/api/client";

import { LearnerClasswork } from "./types";

export function useLearnerClasswork(planVersionId: string | null, studentId: string) {
  return useQuery({
    queryKey: ["studyClasswork", planVersionId, studentId],
    queryFn: () =>
      apiFetch<LearnerClasswork>(
        `/assessments/study-classwork?plan_version_id=${encodeURIComponent(
          planVersionId as string
        )}&student_id=${encodeURIComponent(studentId)}`
      ),
    enabled: Boolean(planVersionId && studentId),
  });
}
