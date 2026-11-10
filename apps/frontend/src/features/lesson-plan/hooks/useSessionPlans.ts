import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "@/shared/api/client";

export interface PlanVersionSummary {
  plan_id: string;
  version_id: string;
  session_id: string;
  subject: string;
  grade: string;
  term?: string;
  week?: number;
  day_index?: number;
  topic?: string;
  subtopic?: string;
  status: string;
  /** How the version came to be: `generated`, `manual`, `revised`, `document_import`. */
  source_type?: string | null;
  approved_at?: string;
  approved_by?: string;
  created_at: string;
  artefact_id?: string;
}

export const useSessionPlans = (sessionId?: string) => {
  return useQuery({
    queryKey: ["sessionPlans", sessionId],
    queryFn: async () => {
      if (!sessionId) return [];
      // List versions filtered strictly by session_id
      return apiFetch<PlanVersionSummary[]>(
        `/artefacts/lesson-plans?session_id=${sessionId}&limit=50`,
      );
    },
    enabled: !!sessionId,
  });
};
