import { useProgress } from "@/features/content-chat/useProgressLines";
import type { ProgressLine } from "@/features/content-chat/useProgressLines";

/** What of the plan is written so far. */
export type PlanOutline = {
  objectives: string[];
  steps: { title: string; minutes: number | null }[];
  written: number;
  total: number;
};

/**
 * What the agent drafting a lesson's plan is doing, and the plan as written so far, read now and
 * then while `running`. Empty when nothing is running, so a finished run's lines are never shown
 * against the next.
 */
export function useDraftingProgress(
  sessionId: string | null | undefined,
  running: boolean,
): { lines: ProgressLine[]; outline: PlanOutline | null } {
  const { lines, extra } = useProgress<{ outline: PlanOutline | null }>(
    sessionId ? "/artefacts/lesson-plans/drafting-progress" : null,
    { session_id: sessionId ?? "" },
    running,
  );
  return { lines, outline: extra?.outline ?? null };
}
