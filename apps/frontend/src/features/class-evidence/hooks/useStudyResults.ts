import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { useTeachingWorkspace } from "@/features/teaching-workspace/context/TeachingWorkspaceContext";

import {
  getLearnerAnswers,
  getStudyResults,
  getStudySources,
  importStudyResults,
  standInStudents,
} from "../api/studyResults";

const resultsKey = (workspaceId: string, lessonPeriodId: string) => [
  "study-results",
  workspaceId,
  lessonPeriodId,
];

/** The evaluation's class results on one lesson, once imported. */
export function useStudyResults(lessonPeriodId: string) {
  const { currentWorkspace } = useTeachingWorkspace();
  const workspaceId = currentWorkspace?.id ?? "";
  return useQuery({
    queryKey: resultsKey(workspaceId, lessonPeriodId),
    queryFn: () => getStudyResults(workspaceId, lessonPeriodId),
    enabled: Boolean(workspaceId && lessonPeriodId),
  });
}

/** The evaluation's lessons that have marked classwork to bring in. Read only when asked for. */
export function useStudySources(lessonPeriodId: string, enabled: boolean) {
  return useQuery({
    queryKey: ["study-results", "sources", lessonPeriodId],
    queryFn: () => getStudySources(lessonPeriodId),
    enabled,
  });
}

/** Brings one evaluation lesson's marked classwork onto this lesson. */
export function useImportStudyResults(lessonPeriodId: string) {
  const { currentWorkspace } = useTeachingWorkspace();
  const workspaceId = currentWorkspace?.id ?? "";
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (fromPlanVersionId: string) =>
      importStudyResults(workspaceId, lessonPeriodId, fromPlanVersionId),
    onSuccess: (results) => {
      queryClient.setQueryData(
        resultsKey(workspaceId, lessonPeriodId),
        results,
      );
    },
  });
}

/** Has the chosen class learners' notes made from the marks of the study learners who stand in. */
export function useStandIns(lessonPeriodId: string) {
  const { currentWorkspace } = useTeachingWorkspace();
  const workspaceId = currentWorkspace?.id ?? "";
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (pairs: { student_id: string; study_student_id: string }[]) =>
      standInStudents(workspaceId, lessonPeriodId, pairs),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["lesson-evidence", workspaceId, lessonPeriodId] });
      void queryClient.invalidateQueries({ queryKey: ["pendingStudentNotes"] });
    },
  });
}

/** What one learner answered on one lesson, question by question. */
export function useLearnerAnswers(lessonPeriodId: string, studentId: string) {
  const { currentWorkspace } = useTeachingWorkspace();
  const workspaceId = currentWorkspace?.id ?? "";
  return useQuery({
    queryKey: ["learner-answers", workspaceId, lessonPeriodId, studentId],
    queryFn: () => getLearnerAnswers(workspaceId, lessonPeriodId, studentId),
    enabled: Boolean(workspaceId && lessonPeriodId && studentId),
  });
}
