import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "@/shared/api/client";

export interface PlanStatusSummary {
  plan_id: string;
  session_id: string;
  status: string;
  version_id: string;
}

interface UseCoursePlanStatusesParams {
  subject?: string;
  grade?: string;
  term?: string;
  teacherId?: string;
}

export const useCoursePlanStatuses = ({
  subject,
  grade,
  term,
  teacherId,
}: UseCoursePlanStatusesParams) => {
  return useQuery({
    queryKey: ["coursePlanStatuses", subject, grade, term, teacherId],
    queryFn: async () => {
      // If we don't have enough context, return empty or try fetching all if backend allows?
      // Backend list_plan_versions allows optional filters.
      // We should ideally have at least subject/grade or term.
      if (!subject && !term) return [];

      const params = new URLSearchParams();
      if (subject) params.append("subject", subject);
      if (grade) params.append("grade", grade);
      if (term) params.append("term", term);
      if (teacherId) params.append("teacher_id", teacherId);
      // We want distinct plans per session. list_plan_versions returns PlanVersionSummary.
      // We should grab them all.
      params.append("limit", "200"); // Valid limit
      params.append("latest_only", "true");

      // NOTE: backend api path for 'list_plan_versions' is /artefacts/lesson-plans
      // But we need to use apiFetch.
      return apiFetch<PlanStatusSummary[]>(
        `/artefacts/lesson-plans?${params.toString()}`
      );
    },
    // Only fetch if we have some context
    enabled: !!(subject || term),
  });
};
