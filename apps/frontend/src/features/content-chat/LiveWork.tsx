import { useEffect, useMemo, useState } from "react";

import { ChatTranscript } from "./ChatTranscript";
import { empty, reduce } from "./transcript";
import type { ProgressLine } from "./useProgressLines";

/** Seconds as minutes and seconds, such as 2:05. */
export const clock = (seconds: number): string =>
  `${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, "0")}`;

/** How long the agent has been at it, counted from when this is shown. */
export function Elapsed() {
  const [seconds, setSeconds] = useState(0);
  useEffect(() => {
    const started = Date.now();
    const timer = setInterval(
      () => setSeconds(Math.floor((Date.now() - started) / 1000)),
      1000,
    );
    return () => clearInterval(timer);
  }, []);
  return <span className="tabular-nums">{clock(seconds)}</span>;
}

/** The transcript of an agent's work from the lines of its progress. A `stopped` agent is idle. */
function useLiveTranscript(events: readonly ProgressLine[], stopped: boolean) {
  // The progress channel carries no status: an agent that has not stopped is at work.
  return useMemo(
    () => ({
      ...events.reduce(
        (state, event) =>
          reduce(state, { seq: event.id, kind: event.kind, data: event.data }),
        empty,
      ),
      working: !stopped,
    }),
    [events, stopped],
  );
}

/**
 * An agent's work as a thread, for a panel: a line saying it is at work, then what it thought,
 * said and did.
 */
export function LiveThread({
  events,
  stopped = false,
}: {
  events: readonly ProgressLine[];
  stopped?: boolean;
}) {
  const transcript = useLiveTranscript(events, stopped);
  return (
    <section aria-label="The agent at work" className="flex flex-col gap-3">
      <p className="flex items-center gap-2 text-sm font-semibold text-(--ink)">
        <span
          aria-hidden
          className={`h-2 w-2 rounded-full ${stopped ? "bg-(--danger)" : "animate-pulse bg-(--accent)"}`}
        />
        {stopped ? (
          "Stopped"
        ) : (
          <>
            Working · <Elapsed />
          </>
        )}
      </p>
      {events.length === 0 ? null : (
        <ChatTranscript transcript={transcript} queued={[]} />
      )}
    </section>
  );
}

/**
 * What an agent that is writing something does, drawn as a chat is, from the moment it starts.
 * `footer` says what the teacher can do meanwhile. A `stopped` agent is no longer at work: the
 * panel keeps what it did, and `footer` says why it stopped.
 */
export function LiveWork({
  events,
  title,
  footer,
  stopped = false,
}: {
  events: readonly ProgressLine[];
  title: string;
  footer: string;
  stopped?: boolean;
}) {
  const transcript = useLiveTranscript(events, stopped);
  return (
    <section
      aria-label="The agent at work"
      className="flex max-h-[30rem] min-h-[12rem] flex-col border border-(--line) bg-(--surface)"
    >
      <header className="flex items-center justify-between gap-3 border-b border-(--line) px-4 py-3">
        <div className="flex items-center gap-2.5">
          <span
            aria-hidden
            className={`h-2 w-2 rounded-full ${stopped ? "bg-(--danger)" : "animate-pulse bg-(--accent)"}`}
          />
          <h3 className="text-sm font-semibold text-(--ink)">{title}</h3>
        </div>
        {stopped ? null : (
          <span className="text-xs text-(--muted)">
            <Elapsed />
          </span>
        )}
      </header>
      <div className="flex min-h-0 flex-1 flex-col px-4 py-3">
        {events.length === 0 ? (
          <p className="text-sm text-(--muted)">Starting the agent…</p>
        ) : (
          <ChatTranscript transcript={transcript} queued={[]} />
        )}
      </div>
      <footer
        className={`border-t border-(--line) px-4 py-2 text-xs ${stopped ? "text-(--danger-ink)" : "text-(--muted)"}`}
      >
        {footer}
      </footer>
    </section>
  );
}
