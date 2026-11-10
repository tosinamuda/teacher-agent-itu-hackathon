import { useEffect, useState } from "react";

import { syntheticProgressWsUrl } from "../lib/api";
import { SyntheticProgressEvent } from "../lib/experiments";

/** One streamed synthetic-progress event, stamped with arrival time. */
export type SyntheticLogEntry = SyntheticProgressEvent & { at: number };

/**
 * Accumulates the experiment's synthetic-progress WebSocket events into a rolling
 * log (last 200) for the Live tab — the realtime stream of what each flow is doing.
 */
export const useSyntheticLog = (experimentId: string | null) => {
  const [entries, setEntries] = useState<SyntheticLogEntry[]>([]);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    if (!experimentId) return;
    const socket = new WebSocket(syntheticProgressWsUrl(experimentId));
    socket.onopen = () => setConnected(true);
    socket.onclose = () => setConnected(false);
    socket.onerror = () => setConnected(false);
    socket.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data) as SyntheticProgressEvent;
        setEntries((prev) => [...prev.slice(-199), { ...payload, at: Date.now() }]);
      } catch {
        /* ignore malformed frames */
      }
    };
    return () => socket.close();
  }, [experimentId]);

  return { entries, connected };
};
