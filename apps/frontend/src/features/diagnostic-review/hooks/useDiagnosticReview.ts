import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { useGenerateContent } from "@/features/content/hooks/useContent";

import { createDiagnosticThread, submitDiagnosticTurn } from "../api/diagnosticReview";

/**
 * Drives the teacher's diagnostic review: loads/creates the revision thread (whose
 * seed carries the current MCQ items + turns), generates the diagnostic if a lesson
 * has none yet, and submits revision-feedback turns. After any change the thread is
 * refetched so the rendered items + turn history stay in sync with the DB.
 */
export function useDiagnosticReview(planVersionId: string | undefined) {
  const queryClient = useQueryClient();
  const threadKey = ["diagnosticThread", planVersionId];

  const threadQuery = useQuery({
    queryKey: threadKey,
    queryFn: () => createDiagnosticThread(planVersionId as string),
    enabled: Boolean(planVersionId),
  });

  const threadId = threadQuery.data?.revision_thread_id;
  const refresh = () => queryClient.invalidateQueries({ queryKey: threadKey });

  const submitMutation = useMutation({
    mutationFn: (payload: { instruction: string }) =>
      submitDiagnosticTurn(threadId as string, payload),
    onSuccess: refresh,
  });

  // Writing the items is the class test's generation, run as a job the page follows.
  const generation = useGenerateContent(planVersionId ?? null, "class-test");

  return {
    items: threadQuery.data?.current_session_plan?.items ?? [],
    turns: threadQuery.data?.turns ?? [],
    isLoading: threadQuery.isLoading,
    isError: threadQuery.isError,
    submit: submitMutation.mutate,
    isSubmitting: submitMutation.isPending,
    submitFailed: submitMutation.isError,
    canSubmit: Boolean(threadId),
    generate: () => void generation.createAsync({}).then(refresh).catch(() => undefined),
    isGenerating: generation.isPending,
    generateFailed: generation.isError,
  };
}
