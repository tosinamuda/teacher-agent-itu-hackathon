import { ReactNode } from "react";

import { Button } from "@/shared/components/ui/Button";

import { formatRaterDisplayName } from "../services/raterPresentation";

type PacketIntroProgress = {
  packetPosition: number | null;
  queueLength: number;
  completedCount: number;
  remainingCount: number;
};

/**
 * Provides the shared orientation frame shown before each packet review begins.
 */
export function PacketIntroFrame({
  continueLabel,
  criteria,
  description,
  extraSection,
  headline,
  laneLabel,
  middleColumn,
  objectivesColumn,
  onContinue,
  progress,
  secondaryAction,
  sessionName,
}: {
  continueLabel: string;
  criteria: string[];
  description: string;
  /** Optional full-width section below the 3-column grid (e.g. the H2 per-objective state card). */
  extraSection?: ReactNode;
  headline: string;
  laneLabel: string;
  middleColumn: ReactNode;
  objectivesColumn: ReactNode;
  onContinue: () => void;
  progress: PacketIntroProgress;
  secondaryAction?: ReactNode;
  sessionName: string;
}) {
  const welcomeName = formatRaterDisplayName(sessionName);

  return (
    <div className="flex min-h-0 flex-col gap-4 px-4 py-4 min-[1200px]:h-full min-[1200px]:overflow-hidden min-[1200px]:px-6">
      <section className="rounded-none border border-[color:var(--line)] bg-white p-6 min-[1200px]:flex-1 min-[1200px]:overflow-y-auto">
        <div className="flex flex-wrap items-center gap-2 border-b border-[color:var(--line)] pb-4">
          <StatusPill>{laneLabel}</StatusPill>
          {progress.packetPosition !== null && progress.queueLength > 0 ? (
            <StatusPill>
              Revision note {progress.packetPosition} of {progress.queueLength}
            </StatusPill>
          ) : null}
          <StatusPill>
            {progress.completedCount} done · {progress.remainingCount} left
          </StatusPill>
        </div>

        <div className="grid gap-6 pt-6 min-[1200px]:[grid-template-columns:minmax(0,1fr)_22rem_18rem]">
          <div className="space-y-4">
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[color:var(--muted)]">
              Expert rater
            </p>
            <h1 className="text-3xl font-semibold leading-tight text-[color:var(--ink)]">
              Welcome, {welcomeName}
            </h1>
            <p className="max-w-xl text-base leading-7 text-[color:var(--muted)]">{headline}</p>
            <p className="max-w-xl text-sm leading-6 text-[color:var(--muted)]">{description}</p>

            <div className="space-y-3 rounded-none border border-[color:var(--line)] bg-[color:var(--panel)] px-4 py-4">
              <p className="text-xs font-semibold uppercase tracking-[0.16em] text-[color:var(--muted)]">
                You will rate
              </p>
              <ul className="grid gap-2 text-sm text-[color:var(--ink)] sm:grid-cols-2">
                {criteria.map((criterion) => (
                  <li
                    key={criterion}
                    className="rounded-none border border-[color:var(--line)] bg-white px-3 py-2"
                  >
                    {criterion}
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="space-y-4 min-[1200px]:border-l min-[1200px]:border-[color:var(--line)] min-[1200px]:pl-6">
            {middleColumn}
          </div>

          <div className="space-y-4 min-[1200px]:border-l min-[1200px]:border-[color:var(--line)] min-[1200px]:pl-6">
            {objectivesColumn}
          </div>
        </div>

        {extraSection ? <div className="mt-6">{extraSection}</div> : null}
      </section>

      <div className="flex flex-wrap justify-end gap-2">
        {secondaryAction}
        <Button onClick={onContinue} type="button">
          {continueLabel}
        </Button>
      </div>
    </div>
  );
}

function StatusPill({ children }: { children: ReactNode }) {
  return (
    <span className="inline-flex rounded-none border border-[color:var(--line)] bg-[color:var(--panel)] px-3 py-1.5 text-xs font-semibold text-[color:var(--ink)]">
      {children}
    </span>
  );
}
