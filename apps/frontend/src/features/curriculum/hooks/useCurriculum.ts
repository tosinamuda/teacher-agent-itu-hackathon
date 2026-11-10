import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "@/shared/api/client";

export type CurriculumTopic = {
  topic_key: string;
  subject: string;
  track: string;
  grade: string;
  term: string;
  week: number;
  topic: string;
  general_objectives: string[];
};

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

export const useCurriculumTopics = (params: {
  subject?: string;
  grade?: string;
  term?: string;
  week?: number;
}) => {
  return useQuery({
    queryKey: ["curriculum", "topics", params],
    queryFn: () => {
      const queryParams = new URLSearchParams();
      if (params.subject) queryParams.append("subject", params.subject);
      if (params.grade) queryParams.append("grade", params.grade);
      if (params.term) queryParams.append("term", params.term);
      if (params.week) queryParams.append("week", params.week.toString());

      if (params.subject?.includes("Further")) {
        queryParams.append("track", "Further");
      } else if (params.subject) {
        queryParams.append("track", "General");
      }

      return apiFetch<CurriculumTopic[]>(
        `/curriculum/topics?${queryParams.toString()}`
      );
    },
    enabled: !!params.subject && !!params.grade && !!params.term,
  });
};

export const useCurriculumSessions = (params: {
  subject: string;
  grade: string;
  term: string;
  week: number;
}) => {
  const track = params.subject.includes("Further") ? "Further" : "General";
  return useQuery({
    queryKey: ["curriculum", "sessions", params],
    queryFn: () =>
      apiFetch<SessionSummary[]>(
        `/curriculum/sessions?subject=${encodeURIComponent(
          params.subject
        )}&track=${track}&grade=${encodeURIComponent(
          params.grade
        )}&term=${encodeURIComponent(params.term)}&week=${params.week}`
      ),
    enabled:
      !!params.subject && !!params.grade && !!params.term && !!params.week,
  });
};

export const useCurriculum = () => {
  return {
    useCurriculumTopics,
    useCurriculumSessions,
  };
};
