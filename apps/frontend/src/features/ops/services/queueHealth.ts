import type { OpsHealth } from "../api";

/** How the job queue reads right now, and how alarming that is. */
export type QueueHealth = {
  state: "running" | "busy" | "stuck" | "no-runner";
  headline: string;
  detail: string;
  tone: "ok" | "warn" | "danger";
};

/**
 * A runner looks for work every second, so a job waiting this long beside a free slot is
 * not waiting its turn: the runner is failing to claim it.
 */
const STUCK_AFTER_SECONDS = 30;

/**
 * Read the runners and the queue into one verdict.
 *
 * Work not moving has two causes an operator must tell apart: nothing is taking jobs (no
 * runner online), or everything is (every slot full). A job waiting beside a free slot is a
 * third: a runner that is up but cannot claim.
 */
export function readQueueHealth(health: OpsHealth): QueueHealth {
  const online = health.runners.filter((runner) => runner.online);
  const waiting = describeWaiting(health);
  const oldest = health.oldest_queued_age_seconds;

  if (online.length === 0) {
    return {
      state: "no-runner",
      headline: "No runner online",
      detail: `Nothing is taking jobs — check that the API is up. ${waiting}`,
      tone: "danger",
    };
  }

  const slots = online.reduce((sum, runner) => sum + runner.slots, 0);
  const running = online.reduce((sum, runner) => sum + runner.running, 0);
  const capacity = `${running} of ${slots} slots in use.`;

  if (oldest !== null && running >= slots) {
    return {
      state: "busy",
      headline: "Every slot busy",
      detail: `${capacity} ${waiting}`,
      tone: "warn",
    };
  }
  if (oldest !== null && oldest > STUCK_AFTER_SECONDS) {
    return {
      state: "stuck",
      headline: "Jobs waiting beside a free slot",
      detail: `${capacity} ${waiting} The runner is up but not claiming — read its log.`,
      tone: "danger",
    };
  }
  return {
    state: "running",
    headline: online.length === 1 ? "1 runner online" : `${online.length} runners online`,
    detail: `${capacity} ${waiting}`,
    tone: "ok",
  };
}

function describeWaiting(health: OpsHealth): string {
  const age = health.oldest_queued_age_seconds;
  if (age === null) return "Nothing is waiting.";
  return `${health.counts.queued} waiting; the oldest for ${formatAge(age)}.`;
}

/** Coarse, because the distinction that matters is seconds versus hours. */
export function formatAge(seconds: number): string {
  const whole = Math.max(Math.round(seconds), 0);
  if (whole < 90) return `${whole}s`;
  const minutes = Math.round(whole / 60);
  if (minutes < 90) return `${minutes}m`;
  return `${Math.round(minutes / 60)}h`;
}
