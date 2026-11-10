import { apiFetch, apiFetchBlob } from "@/shared/api/client";
import { ReviewNoteSection } from "@/shared/types/review-note";

/** A student's rendered revision note (the post-class review pack manifest). */
export type ReviewNoteManifest = {
  artefact_id: string;
  plan_version_id: string;
  subject?: string | null;
  grade?: string | null;
  topic?: string | null;
  subtopic?: string | null;
  term?: string | null;
  week?: number | null;
  steps: ReviewNoteSection[];
};

/** Fetch a revision note by artefact id. */
export const fetchReviewNote = (artefactId: string) =>
  apiFetch<{ manifest: ReviewNoteManifest }>(
    `/artefacts/post-class-review-packs/${artefactId}`,
  ).then((response) => response.manifest);

/** Fetch the server-rendered PDF of a revision note (WeasyPrint), with its filename. */
export const fetchReviewNotePdf = async (
  artefactId: string,
): Promise<{ blob: Blob; filename: string }> => {
  const { blob, response } = await apiFetchBlob(
    `/artefacts/post-class-review-packs/${artefactId}/pack.pdf`,
  );
  const disposition = response.headers.get("Content-Disposition") ?? "";
  const filename = /filename="?([^"]+)"?/.exec(disposition)?.[1] ?? "review-note.pdf";
  return { blob, filename };
};
