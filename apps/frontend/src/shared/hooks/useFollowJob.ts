import { useEffect, useEffectEvent, useRef } from "react";
import { useQuery } from "@tanstack/react-query";

import { isUnfinished, latestJob } from "@/shared/api/jobs";

const POLL_MS = 2000;

/** The query key of the caller's latest job of `kind` for `subject`. */
export const followedJobKey = (kind: string, subject: string | null) =>
  ["job", kind, subject] as const;

/**
 * Follow the caller's latest job of `kind` for `subject`, so a page reloaded while its
 * generation runs still shows it running, and refreshes what it made once it ends.
 *
 * `onFinished` runs once, when a job this page saw unfinished comes to an end.
 */
export function useFollowJob(kind: string, subject: string | null, onFinished: () => void) {
  const query = useQuery({
    queryKey: followedJobKey(kind, subject),
    queryFn: () => latestJob(kind, subject as string),
    enabled: Boolean(subject),
    refetchInterval: (current) => (isUnfinished(current.state.data) ? POLL_MS : false),
  });
  const running = isUnfinished(query.data);
  const wasRunning = useRef(false);
  const finish = useEffectEvent(onFinished);

  useEffect(() => {
    if (wasRunning.current && !running) finish();
    wasRunning.current = running;
  }, [running]);

  return { job: query.data ?? null, running };
}
