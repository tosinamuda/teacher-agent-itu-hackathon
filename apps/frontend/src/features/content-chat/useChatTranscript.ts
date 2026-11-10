import { useQueryClient } from "@tanstack/react-query";
import { useCallback, useEffect, useReducer, useState } from "react";

import { followChat } from "./chatApi";
import type { ServerEvent } from "./sse";
import { empty, reduce, type Transcript } from "./transcript";

type Action = { type: "reset" } | { type: "event"; event: ServerEvent };

const step = (state: Transcript, action: Action): Transcript =>
  action.type === "reset" ? empty : reduce(state, action.event);

/** How long to wait before following a chat again after the connection drops. */
const RETRY_MS = 2000;

const pause = (ms: number, signal: AbortSignal) =>
  new Promise<void>((resolve) => {
    const timer = setTimeout(resolve, ms);
    signal.addEventListener("abort", () => (clearTimeout(timer), resolve()), {
      once: true,
    });
  });

/**
 * A chat as it happens: its kept events replayed, then what comes next, drawn as it arrives. A
 * dropped connection is followed again from the last kept event, so nothing is missed or
 * repeated. A message sent and not yet started is shown as queued.
 */
export function useChatTranscript(contentId: string, chatId: string | null) {
  const queryClient = useQueryClient();
  const [state, dispatch] = useReducer(step, empty);
  const [queued, setQueued] = useState<string[]>([]);

  useEffect(() => {
    dispatch({ type: "reset" });
    setQueued([]);
    if (chatId === null) return;
    const controller = new AbortController();
    let last = 0;
    const onEvent = (event: ServerEvent) => {
      if (event.seq !== null) last = Math.max(last, event.seq);
      if (event.kind === "user_message") {
        const said = String(event.data.text ?? "");
        setQueued((waiting) => {
          const at = waiting.indexOf(said);
          return at < 0 ? waiting : waiting.filter((_, index) => index !== at);
        });
      }
      if (event.kind === "turn_done" && event.data.changed !== false) {
        void queryClient.invalidateQueries({ queryKey: ["content"] });
        void queryClient.invalidateQueries({ queryKey: ["plan"] });
        void queryClient.invalidateQueries({ queryKey: ["sessionPlans"] });
      }
      if (["turn_done", "turn_failed", "turn_stopped"].includes(event.kind)) {
        void queryClient.invalidateQueries({
          queryKey: ["contentChats", contentId],
        });
      }
      dispatch({ type: "event", event });
    };
    void (async () => {
      while (!controller.signal.aborted) {
        try {
          await followChat(contentId, chatId, last, controller.signal, onEvent);
        } catch {
          // The connection dropped or was refused: follow again from where it stopped.
        }
        await pause(RETRY_MS, controller.signal);
      }
    })();
    return () => controller.abort();
  }, [contentId, chatId, queryClient]);

  const addQueued = useCallback(
    (text: string) => setQueued((waiting) => [...waiting, text]),
    [],
  );
  const dropQueued = useCallback(
    (text: string) =>
      setQueued((waiting) => {
        const at = waiting.lastIndexOf(text);
        return waiting.filter((_, index) => index !== at);
      }),
    [],
  );

  const clearQueued = useCallback(() => setQueued([]), []);

  return { transcript: state, queued, addQueued, dropQueued, clearQueued };
}
