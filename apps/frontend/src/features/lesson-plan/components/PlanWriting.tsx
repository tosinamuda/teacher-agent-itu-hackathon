import { Elapsed } from "@/features/content-chat/LiveWork";
import { Button, buttonClass } from "@/shared/components/ui/Button";
import { Link } from "@/shared/router";

import type { PlanOutline } from "../hooks/useDraftingProgress";
import { writePlanPath } from "../lib/planPaths";

const LABEL =
  "text-[11px] font-semibold uppercase tracking-[0.12em] text-(--faint)";

/** A bar standing where text will be. */
const Pending = ({ width }: { width: string }) => (
  <div
    aria-hidden
    className="h-2.5 animate-pulse bg-(--sunken)"
    style={{ width }}
  />
);

/**
 * The plan being written: the objectives and steps already written, with bars where the rest will
 * come. The agent's own work is in the panel.
 */
export function PlanWriting({
  title,
  outline,
}: {
  title: string;
  outline: PlanOutline | null;
}) {
  const objectives = outline?.objectives ?? [];
  const steps = outline?.steps ?? [];
  return (
    <section aria-label="Writing the plan" className="flex flex-col gap-5">
      <header className="flex items-start justify-between gap-4">
        <div className="flex flex-col gap-1">
          <h1 className="text-2xl font-semibold text-(--ink)">{title}</h1>
          <p className="text-xs text-(--ink-2)">Writing the plan</p>
        </div>
        <span className="inline-flex items-center gap-2 border border-(--line-2) bg-(--surface) px-2.5 py-1 text-xs font-medium text-(--ink)">
          <span
            aria-hidden
            className="h-2 w-2 animate-pulse rounded-full bg-(--accent)"
          />
          <Elapsed />
        </span>
      </header>
      {objectives.length > 0 ? (
        <section aria-label="Objectives" className="flex flex-col gap-2">
          <h2 className={LABEL}>Objectives</h2>
          <ul className="flex flex-col gap-1 text-sm text-(--ink)">
            {objectives.map((objective) => (
              <li key={objective}>• {objective}</li>
            ))}
          </ul>
        </section>
      ) : null}
      <section aria-label="Steps" className="flex flex-col gap-2">
        {steps.length > 0 ? <h2 className={LABEL}>Steps</h2> : null}
        <ol className="border border-(--line) bg-(--surface)">
          {steps.map((step, index) => (
            <li
              key={`${index}-${step.title}`}
              className="flex items-center gap-3 border-t border-(--line) px-4 py-3 first:border-t-0"
            >
              <span className="text-xs text-(--faint)">{index + 1}</span>
              <span className="flex-1 text-sm font-semibold text-(--ink)">
                {step.title}
              </span>
              {step.minutes ? (
                <span className="text-xs text-(--faint)">
                  {step.minutes} min
                </span>
              ) : null}
            </li>
          ))}
          <li className="flex flex-col gap-2 border-t border-(--line) px-4 py-3 first:border-t-0">
            <Pending width="30%" />
            <Pending width="70%" />
          </li>
        </ol>
      </section>
    </section>
  );
}

/** The plan was not made: why, and the ways on. */
export function PlanFailed({
  lessonPeriodId,
  reason,
  onRetry,
}: {
  lessonPeriodId: string;
  reason: string;
  onRetry: () => void;
}) {
  return (
    <section
      role="alert"
      className="flex flex-col gap-3 border border-(--danger) bg-(--danger-tint) p-4"
    >
      <h2 className="text-sm font-semibold text-(--danger-ink)">
        The plan wasn&apos;t finished
      </h2>
      <p className="text-sm text-(--ink)">{reason}</p>
      <div className="flex flex-wrap gap-2">
        <Button onClick={onRetry}>Try again</Button>
        <Link
          href={writePlanPath(lessonPeriodId)}
          className={buttonClass({ variant: "ghost" })}
        >
          Write it by hand instead
        </Link>
      </div>
    </section>
  );
}
