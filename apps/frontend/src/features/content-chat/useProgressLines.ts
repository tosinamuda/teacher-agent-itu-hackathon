import { useEffect, useState } from "react";

import { apiFetch } from "@/shared/api/client";

/** One thing an agent said or did, as the chat keeps it. */
export type ProgressLine = {
  id: number;
  kind: string;
  data: Record<string, unknown>;
};

type Progress = { lines: ProgressLine[]; next: number };

/** What a progress read carries besides the lines: whatever the page that reads it asks for. */
type Extra<E> = Omit<Progress, "lines" | "next"> & E;

const POLL_MS = 2000;
const KEPT = 300;

/**
 * The lines already read with the fresh ones after them, newest last, none twice. A run that
 * starts is not a continuation of the one before, so what came before its start is dropped.
 */
export function appendLines(
  kept: ProgressLine[],
  fresh: ProgressLine[],
): ProgressLine[] {
  const seen = new Set(kept.map((line) => line.id));
  const added = fresh.filter((line) => !seen.has(line.id));
  const starts = added.map((line) => line.kind).lastIndexOf("start");
  const lines = starts < 0 ? [...kept, ...added] : added.slice(starts);
  return lines.slice(-KEPT);
}

/**
 * What an agent is doing, read from `path` now and then while `running`. Empty when nothing is
 * running, so a finished run's lines are never shown against the next. A null `path` reads nothing.
 * With `keep`, a run that stopped is read once and its lines stay, to show where it stopped.
 */
export function useProgressLines(
  path: string | null,
  params: Record<string, string>,
  running: boolean,
  keep = false,
): ProgressLine[] {
  return useProgress(path, params, running, keep).lines;
}

/** The same read as `useProgressLines`, with the rest of what the server sent besides the lines. */
export function useProgress<E extends object = object>(
  path: string | null,
  params: Record<string, string>,
  running: boolean,
  keep = false,
): { lines: ProgressLine[]; extra: Extra<E> | null } {
  const [lines, setLines] = useState<ProgressLine[]>([]);
  const [extra, setExtra] = useState<Extra<E> | null>(null);
  const [wasRunning, setWasRunning] = useState(running);
  const key = JSON.stringify(params);

  // A run that starts is not a continuation of the one before: its lines begin from nothing.
  if (running !== wasRunning) {
    setWasRunning(running);
    if (running) {
      setLines([]);
      setExtra(null);
    }
  }

  useEffect(() => {
    if (!(running || keep) || !path) return;
    const controller = new AbortController();
    let kept: ProgressLine[] = [];
    let after = 0;
    const read = async () => {
      try {
        const query = new URLSearchParams({
          ...JSON.parse(key),
          after: String(after),
        });
        const progress = await apiFetch<Progress & E>(
          `${path}?${query.toString()}`,
          {
            signal: controller.signal,
          },
        );
        const { lines: fresh, next, ...rest } = progress;
        after = next;
        kept = appendLines(kept, fresh);
        setLines(kept);
        setExtra(rest as unknown as Extra<E>);
      } catch {
        // The next read tries again; the page already shows that the agent is at work.
      }
    };
    void read();
    const timer = running ? setInterval(() => void read(), POLL_MS) : undefined;
    return () => {
      controller.abort();
      clearInterval(timer);
    };
  }, [path, key, running, keep]);

  return running || keep ? { lines, extra } : { lines: [], extra: null };
}
