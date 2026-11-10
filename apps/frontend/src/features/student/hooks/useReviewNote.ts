import { useQuery } from "@tanstack/react-query";

import { fetchReviewNote } from "../api/reviewNote";

/** Load a student's revision note by artefact id. */
export const useReviewNote = (artefactId?: string | null) =>
  useQuery({
    queryKey: ["reviewNote", artefactId],
    queryFn: () => fetchReviewNote(artefactId as string),
    enabled: Boolean(artefactId),
  });
