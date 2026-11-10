import { useEffect, useState } from "react";
import { useQueryClient } from "@tanstack/react-query";

import { syntheticProgressWsUrl } from "../lib/api";
import { SyntheticProgressEvent } from "../lib/experiments";

/** Latest progress event per synthetic flow, keyed by flow name. */
export type SyntheticProgressState = {
  generation: SyntheticProgressEvent | null;
  students: SyntheticProgressEvent | null;
  teacher_review: SyntheticProgressEvent | null;
  loop: SyntheticProgressEvent | null;
  ratings: SyntheticProgressEvent | null;
  connected: boolean;
};

const EMPTY: SyntheticProgressState = {
  generation: null,
  students: null,
  teacher_review: null,
  loop: null,
  ratings: null,
  connected: false,
};

const parse = (raw: string): SyntheticProgressEvent | null => {
  try {
    return JSON.parse(raw) as SyntheticProgressEvent;
  } catch {
    return null;
  }
};

/**
 * Subscribes to an experiment's synthetic-test progress WebSocket and exposes the
 * latest event for each flow (students + ratings) live. On a flow's "done" event it
 * refreshes the dependent result caches (ratings + statistics) so the dashboard updates
 * without a manual reload. Replaces the old fire-and-refresh pattern.
 */
export const useSyntheticProgress = (experimentId: string | null) => {
  const [state, setState] = useState<SyntheticProgressState>(EMPTY);
  const queryClient = useQueryClient();

  useEffect(() => {
    if (!experimentId) return;
    const socket = new WebSocket(syntheticProgressWsUrl(experimentId));

    socket.onopen = () => setState((prev) => ({ ...prev, connected: true }));
    socket.onclose = () => setState((prev) => ({ ...prev, connected: false }));
    socket.onerror = () => setState((prev) => ({ ...prev, connected: false }));

    socket.onmessage = (event) => {
      const payload = parse(event.data);
      if (!payload?.flow) return;
      setState((prev) => ({ ...prev, [payload.flow]: payload }));
      // A flow ends in exactly one terminal event: "done" when it succeeded, "error"
      // when it did not. A partially failed generation still wrote packs, so both
      // refresh the dependent caches.
      if (payload.type === "done" || payload.type === "error") {
        void queryClient.invalidateQueries({ queryKey: ["experimentRatings", experimentId] });
        void queryClient.invalidateQueries({ queryKey: ["experimentStatistics", experimentId] });
        void queryClient.invalidateQueries({ queryKey: ["experiment", experimentId] });
      }
    };

    return () => socket.close();
  }, [experimentId, queryClient]);

  return state;
};
