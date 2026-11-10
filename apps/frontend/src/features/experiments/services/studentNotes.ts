import type { ContentSummary } from "@/features/content/types";

/** How many students have a revision note of their own, per plan version. */
export function studentsWithNotes(notes: ContentSummary[]): Map<string, number> {
  const students = new Map<string, Set<string>>();
  for (const note of notes) {
    if (note.type !== "revision-note" || note.level !== "learner" || !note.student_id) continue;
    const lesson = students.get(note.plan_version_id) ?? new Set<string>();
    lesson.add(note.student_id);
    students.set(note.plan_version_id, lesson);
  }
  return new Map([...students].map(([planVersionId, ids]) => [planVersionId, ids.size]));
}
