import { useQuery } from "@tanstack/react-query";

import { listPendingStudentNotes } from "../lib/api";

/**
 * The teacher's pending per-student revision notes (across all their lessons),
 * used by the lesson-prep queue to light up the per-student review steps and
 * keep a lesson in view while its students' notes await approval.
 */
export const usePendingStudentNotes = (enabled: boolean) =>
  useQuery({
    queryKey: ["pendingStudentNotes"],
    queryFn: listPendingStudentNotes,
    enabled,
  });
