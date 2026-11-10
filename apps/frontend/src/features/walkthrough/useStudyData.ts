import { useQuery } from "@tanstack/react-query";

import { getLessonTranscripts, getStudyDesign } from "./studyData";

export function useLessonTranscripts(experimentId: string | undefined) {
  return useQuery({
    queryKey: ["lessonTranscripts", experimentId],
    queryFn: () => getLessonTranscripts(experimentId ?? ""),
    enabled: Boolean(experimentId),
  });
}

export function useStudyDesign(investigationId: string) {
  return useQuery({
    queryKey: ["studyDesign", investigationId],
    queryFn: () => getStudyDesign(investigationId),
  });
}
