import { useQuery } from "@tanstack/react-query";

import {
  getStudyInstrument,
  getStudyLessonResults,
  getStudyRaterSchedule,
  getStudyRatings,
  getStudyRatingsTally,
  getStudyWideResults,
} from "./api";

export function useStudyRatings(noteId: string | undefined) {
  return useQuery({
    queryKey: ["studyRatings", noteId],
    queryFn: () => getStudyRatings(noteId as string),
    enabled: Boolean(noteId),
  });
}

export function useStudyRatingsTally(planVersionIds: string[]) {
  return useQuery({
    queryKey: ["studyRatingsTally", planVersionIds],
    queryFn: () => getStudyRatingsTally(planVersionIds),
    enabled: planVersionIds.length > 0,
  });
}

export function useStudyRaterSchedule(experimentId: string) {
  return useQuery({
    queryKey: ["studyRaterSchedule", experimentId],
    queryFn: () => getStudyRaterSchedule(experimentId),
  });
}

export function useStudyLessonResults(experimentId: string) {
  return useQuery({
    queryKey: ["studyLessonResults", experimentId],
    queryFn: () => getStudyLessonResults(experimentId),
  });
}

export function useStudyWideResults(investigationId: string, enabled: boolean) {
  return useQuery({
    queryKey: ["studyWideResults", investigationId],
    queryFn: () => getStudyWideResults(investigationId),
    enabled,
  });
}

export function useStudyInstrument() {
  return useQuery({ queryKey: ["studyInstrument"], queryFn: getStudyInstrument, staleTime: Infinity });
}
