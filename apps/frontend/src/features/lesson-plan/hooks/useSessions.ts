import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "@/shared/api/client";

export type SessionSummary = {
  session_id: string;
  subject: string;
  track: string;
  grade: string;
  term: string;
  week: number;
  day_index: number;
  topic_key: string;
  subtopic_id: string;
  subtopic_title?: string;
  session_objectives: string[];
};

type UseSessionsParams = {
  subject: string;
  grade: string;
  term: string;
  week: number;
};

export const useSessions = ({
  subject,
  grade,
  term,
  week,
}: UseSessionsParams) => {
  const track = subject.includes("Further") ? "Further" : "General";

  return useQuery({
    queryKey: ["sessions", subject, term, track, week, grade],
    queryFn: () =>
      apiFetch<SessionSummary[]>(
        `/curriculum/sessions?subject=${encodeURIComponent(
          subject,
        )}&track=${track}&grade=${encodeURIComponent(
          grade,
        )}&term=${encodeURIComponent(term)}&week=${week}`,
      ),
  });
};
