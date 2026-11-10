import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { runJob } from "@/shared/api/jobs";
import { followedJobKey, useFollowJob } from "@/shared/hooks/useFollowJob";

import {
  GENERATE_CONTENT,
  approveContent,
  rejectContent,
  reviseContent,
  contentGenerationSubject,
  findContent,
  generateContent,
  getContent,
  getSpec,
  listApprovals,
  listContentTypes,
  listRevisions,
  setDefaultGenerator,
} from "../api/content";
import { ContentTypeSlug, ExpertSources, Level } from "../types";

const keys = {
  types: ["contentTypes"] as const,
  spec: (type: ContentTypeSlug, revision: number) =>
    ["contentSpec", type, revision] as const,
  lesson: (planVersionId: string | null) =>
    ["content", "lesson", planVersionId] as const,
  one: (contentId: string) => ["content", "one", contentId] as const,
  revisions: (contentId: string) =>
    ["content", "revisions", contentId] as const,
  approvals: (contentId: string) =>
    ["content", "approvals", contentId] as const,
};

export function useContentTypes() {
  return useQuery({ queryKey: keys.types, queryFn: listContentTypes });
}

/** Switching the default changes what the types list says, so it is read again. */
export function useSetDefaultGenerator() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (choice: {
      type: ContentTypeSlug;
      level: Level;
      generator: string;
    }) => setDefaultGenerator(choice.type, choice.level, choice.generator),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: keys.types }),
  });
}

/** A spec revision never changes once stored, so it is read once. */
export function useSpec(type: ContentTypeSlug, revision: number | undefined) {
  return useQuery({
    queryKey: keys.spec(type, revision ?? 0),
    queryFn: () => getSpec(type, revision as number),
    enabled: revision !== undefined,
    staleTime: Infinity,
  });
}

export function useLessonContent(planVersionId: string | null) {
  return useQuery({
    queryKey: keys.lesson(planVersionId),
    queryFn: () => findContent(planVersionId as string),
    enabled: Boolean(planVersionId),
  });
}

export function useContent(contentId: string) {
  return useQuery({
    queryKey: keys.one(contentId),
    queryFn: () => getContent(contentId),
    enabled: Boolean(contentId),
  });
}

export function useContentRevisions(contentId: string) {
  return useQuery({
    queryKey: keys.revisions(contentId),
    queryFn: () => listRevisions(contentId),
  });
}

export function useContentApprovals(contentId: string) {
  return useQuery({
    queryKey: keys.approvals(contentId),
    queryFn: () => listApprovals(contentId),
  });
}

/**
 * Generate one type of class content for a lesson, as a job the page follows.
 *
 * `isPending` holds from the click until the content exists, and across a reload: the
 * page picks up the job still making it. Asking again while it runs follows the same job.
 */
export function useGenerateContent(
  planVersionId: string | null,
  type: ContentTypeSlug,
) {
  const queryClient = useQueryClient();
  const subject = planVersionId
    ? contentGenerationSubject(planVersionId, type)
    : null;
  const refresh = () => {
    void queryClient.invalidateQueries({ queryKey: ["content"] });
    void queryClient.invalidateQueries({ queryKey: ["assessmentStatus"] });
    void queryClient.invalidateQueries({ queryKey: ["experiment"] });
    void queryClient.invalidateQueries({ queryKey: ["experiments"] });
  };
  const followed = useFollowJob(GENERATE_CONTENT, subject, refresh);
  const mutation = useMutation({
    mutationFn: ({
      sources,
      instructions,
    }: { sources?: ExpertSources; instructions?: string } = {}) =>
      runJob<{ content_id: string }>(async () => {
        const accepted = await generateContent(
          planVersionId as string,
          type,
          "class",
          sources,
          instructions,
        );
        void queryClient.invalidateQueries({
          queryKey: followedJobKey(GENERATE_CONTENT, subject),
        });
        return accepted;
      }),
    onSuccess: refresh,
  });
  const job = followed.job;
  const stopped = job?.state === "failed" || job?.state === "cancelled";
  return {
    create: mutation.mutate,
    createAsync: mutation.mutateAsync,
    isPending: mutation.isPending || followed.running,
    isError: mutation.isError,
    error: mutation.error,
    /** Why the latest attempt stopped, when it did; it stays until the next attempt. */
    failure: stopped ? (job.error ?? `job_${job.state}`) : null,
  };
}

export function useReviseContent(contentId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (feedback: string) => reviseContent(contentId, feedback),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["content"] }),
  });
}

export function useRejectContent(contentId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      expectedVersion,
      reason,
    }: {
      expectedVersion: number;
      reason: string;
    }) => rejectContent(contentId, expectedVersion, reason),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["content"] });
    },
  });
}

export function useApproveContent(contentId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (expectedVersion: number) =>
      approveContent(contentId, expectedVersion),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["content"] });
      void queryClient.invalidateQueries({ queryKey: ["assessmentStatus"] });
      void queryClient.invalidateQueries({ queryKey: ["experiment"] });
      void queryClient.invalidateQueries({ queryKey: ["experiments"] });
    },
  });
}
