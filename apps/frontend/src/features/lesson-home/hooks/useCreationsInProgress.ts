import { useQueries } from "@tanstack/react-query";

import {
  GENERATE_CONTENT,
  contentGenerationSubject,
} from "@/features/content/api/content";
import {
  useContentTypes,
  useLessonContent,
} from "@/features/content/hooks/useContent";
import { currentContent } from "@/features/content/status";
import type { ContentTypeInfo } from "@/features/content/types";
import { isUnfinished, latestJob } from "@/shared/api/jobs";
import { followedJobKey } from "@/shared/hooks/useFollowJob";

import { materialsToMake } from "../lib/lessonHome";

const POLL_MS = 2000;

export type Creation = {
  info: ContentTypeInfo;
  /** The agent is writing it now. */
  running: boolean;
  /** The agent stopped before it was made, and nothing of that type exists yet. */
  stopped: boolean;
};

/**
 * What the agent is writing from a lesson's approved plan, and what stopped short, by material.
 * A job that failed once stops mattering when the material exists, so an old failure does not stay.
 * Each job is the one a button follows, so asking again here asks the server nothing new.
 */
export function useCreationsInProgress(
  planVersionId: string | null,
): Creation[] {
  const types = materialsToMake(useContentTypes().data ?? []);
  const made = useLessonContent(planVersionId).data ?? [];
  const jobs = useQueries({
    queries: types.map((info) => {
      const subject = planVersionId
        ? contentGenerationSubject(planVersionId, info.type)
        : null;
      return {
        queryKey: followedJobKey(GENERATE_CONTENT, subject),
        queryFn: () => latestJob(GENERATE_CONTENT, subject as string),
        enabled: Boolean(subject),
        refetchInterval: (current: {
          state: { data?: Awaited<ReturnType<typeof latestJob>> };
        }) => (isUnfinished(current.state.data) ? POLL_MS : false),
      };
    }),
  });
  return types
    .map((info, at) => {
      const job = jobs[at].data;
      const running = isUnfinished(job);
      const failed = job?.state === "failed" || job?.state === "cancelled";
      return {
        info,
        running,
        stopped: failed && !currentContent(made, info.type),
      };
    })
    .filter((creation) => creation.running || creation.stopped);
}
