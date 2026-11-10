import { currentContent } from "../status";
import { LessonNoteManifest } from "../types";
import { useContent, useLessonContent } from "./useContent";

/** A plan version's lesson note: its summary, and its sections once loaded. */
export function useLessonNote(planVersionId: string | null | undefined) {
  const lessonContent = useLessonContent(planVersionId ?? null);
  const summary = currentContent(lessonContent.data ?? [], "lesson-note");
  const note = useContent(summary?.id ?? "");
  return {
    summary,
    manifest: note.data
      ? (note.data.content as unknown as LessonNoteManifest)
      : undefined,
    isLoading: lessonContent.isLoading || Boolean(summary && note.isLoading),
  };
}
