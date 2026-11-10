import { useQueries } from "@tanstack/react-query";

import { findContent } from "@/features/content/api/content";
import { useContentTypes } from "@/features/content/hooks/useContent";
import { useSchemeOfWork } from "@/features/curriculum/hooks/useSchemeOfWork";
import { usePendingStudentNotes } from "@/features/experiments/hooks/usePendingStudentNotes";
import { useStudentNotesMade } from "@/features/experiments/hooks/useStudentNotesMade";
import { useStudyResults } from "@/features/class-evidence/hooks/useStudyResults";
import { useSessionPlans } from "@/features/lesson-plan/hooks/useSessionPlans";
import { useTeachingWorkspace } from "@/features/teaching-workspace/context/TeachingWorkspaceContext";

import {
  approvedVersionOf,
  learnerRows,
  lessonOf,
  materialRows,
  planRow,
  versionsWithMaterials,
} from "../lib/lessonHome";

/** Everything a lesson's home shows, read from the lesson's plan, its content and its learners. */
export function useLessonHome(lessonPeriodId: string) {
  const { currentWorkspace } = useTeachingWorkspace();
  const scheme = useSchemeOfWork(currentWorkspace?.term_class_subject_id);
  const plans = useSessionPlans(lessonPeriodId);
  const types = useContentTypes();
  const approved = approvedVersionOf(plans.data ?? []);
  const planVersionId = approved?.version_id ?? null;
  // Materials stay with the version they were made from, so every version that was ever approved
  // is read, and the newest of each type is the lesson's.
  const contents = useQueries({
    queries: versionsWithMaterials(plans.data ?? []).map((versionId) => ({
      queryKey: ["content", "lesson", versionId],
      queryFn: () => findContent(versionId),
    })),
  });
  const studyResults = useStudyResults(lessonPeriodId);
  const pending = usePendingStudentNotes(true);
  const made = useStudentNotesMade(true);

  const loaded = contents
    .flatMap((query) => query.data ?? [])
    .sort((a, b) => (b.created_at ?? "").localeCompare(a.created_at ?? ""));
  const rows = {
    plan: planRow(plans.data ?? [], lessonPeriodId),
    materials: materialRows(types.data ?? [], loaded, planVersionId, lessonPeriodId),
    learners: learnerRows(
      loaded,
      lessonPeriodId,
      {
        made: planVersionId ? (made.data?.get(planVersionId) ?? 0) : 0,
        awaiting: (pending.data ?? []).filter((note) => note.plan_version_id === planVersionId).length,
      },
      {
        planApproved: planVersionId !== null,
        importedLearners: studyResults.data?.imported ? studyResults.data.learners.length : 0,
      },
    ),
  };

  return {
    lesson: lessonOf(scheme.data, lessonPeriodId),
    planVersionId,
    rows,
    isLoading: plans.isLoading || types.isLoading || scheme.isLoading,
    isError: plans.isError || types.isError,
  };
}
