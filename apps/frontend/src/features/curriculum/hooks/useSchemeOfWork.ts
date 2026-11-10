import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "@/shared/api/client";

export type LessonPeriod = {
  id: string;
  scheme_of_work_id: string;
  period_number: number;
  title: string | null;
  subtopic_id: string | null;
  subtopic_title: string | null;
};

export type SchemeOfWork = {
  id: string;
  term_class_subject_id: string;
  week_number: number;
  /** ISO date the week starts, when the school has set the term's dates. */
  starts_on?: string | null;
  title: string;
  objectives: Record<string, unknown> | null;
  lesson_periods: LessonPeriod[];
};

export type TermClassSubject = {
  id: string;
  course_id: string;
  term: string;
  year: string;
  weeks: SchemeOfWork[];
  current_week_number?: number | null;
};

/**
 * Fetch scheme-of-work data by TermClassSubject ID.
 */
export const useSchemeOfWork = (tcsId: string | undefined) => {
  return useQuery({
    queryKey: ["teaching", "term-class-subject", tcsId],
    queryFn: () => {
      if (!tcsId) throw new Error("TCS ID required");
      return apiFetch<TermClassSubject>(`/teaching/term-class-subjects/by-id/${tcsId}`);
    },
    enabled: !!tcsId,
  });
};
