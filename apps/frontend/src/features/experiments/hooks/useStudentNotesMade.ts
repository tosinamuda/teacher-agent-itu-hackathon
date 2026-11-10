import { useQuery } from "@tanstack/react-query";

import { findLearnerRevisionNotes } from "@/features/content/api/content";

import { studentsWithNotes } from "../services/studentNotes";

/**
 * How many students have their own revision note, per lesson (plan version), across the
 * teacher's lessons. The per-student review step is done only once there are some.
 */
export const useStudentNotesMade = (enabled: boolean) =>
  useQuery({
    queryKey: ["studentNotesMade"],
    queryFn: findLearnerRevisionNotes,
    enabled,
    select: studentsWithNotes,
  });
