import { useState } from "react";

import { Button } from "@/shared/components/ui/Button";

import { ExperimentReadiness } from "../lib/experiments";
import { useLaunchExperimentExecution } from "../hooks/useExperiments";
import {
  useResearchDefaults,
  useSyntheticLoop,
  useSyntheticRate,
  useSyntheticStudents,
  useSyntheticTeacher,
} from "../hooks/useExperimentResults";
import { useSyntheticProgress } from "../hooks/useSyntheticProgress";
import { LessonContext, SyntheticContextStep } from "./SyntheticContextStep";
import { SyntheticRunStatus } from "./SyntheticRunStatus";

const LIVE = "Running live below — no need to refresh.";

/**
 * Research-only synthetic harness, sequenced as the teacher-in-the-loop flow:
 * (1) lesson context/subtopic → (2) generate the C0–C3 study packs from the approved
 * lesson plan → (3) synthetic teacher reviews C3 and finalises C4 → (4–5) the synthetic
 * class + survey seed H2 personalisation (P0/P1) → (6) synthetic raters score. A one-click
 * "full loop" runs teacher → export → rate. Streamed live over a WebSocket.
 */
export function SyntheticTestPanel({
  experimentId,
  readiness,
  context,
}: {
  experimentId: string;
  readiness?: ExperimentReadiness;
  context?: LessonContext;
}) {
  const [status, setStatus] = useState<string | null>(null);
  const syntheticStudents = useSyntheticStudents(experimentId);
  const syntheticTeacher = useSyntheticTeacher(experimentId);
  const syntheticRate = useSyntheticRate(experimentId);
  const syntheticLoop = useSyntheticLoop(experimentId);
  const launch = useLaunchExperimentExecution(experimentId);
  const progress = useSyntheticProgress(experimentId);
  const defaults = useResearchDefaults();

  const basePackApproved = readiness?.base_pack_approved ?? false;
  const note = (message: string) => setStatus(message);
  const fail = () => setStatus("Something went wrong — check the backend logs.");
  const busy =
    syntheticStudents.isPending ||
    syntheticTeacher.isPending ||
    syntheticRate.isPending ||
    syntheticLoop.isPending ||
    launch.isPending;

  const step = (
    label: string,
    n: number,
    onClick: () => void,
    pending: boolean,
    disabled = false
  ) => (
    <div className="flex items-center gap-3">
      <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-none bg-(--accent) text-xs font-semibold text-white">
        {n}
      </span>
      <Button
        size="sm"
        variant="secondary"
        onClick={onClick}
        disabled={busy || disabled}
        isLoading={pending}
      >
        {label}
      </Button>
    </div>
  );

  const phase = (label: string) => (
    <p className="pt-1 text-[11px] font-semibold uppercase tracking-[0.14em] text-(--accent-deep)">
      {label}
    </p>
  );

  return (
    <div className="space-y-4 rounded-2xl border border-(--line) bg-(--surface) p-4">
      <div className="space-y-1">
        <p className="text-xs font-semibold uppercase tracking-wide text-(--accent-deep)">
          Pre-test (synthetic) — dry run
        </p>
        <p className="text-[11px] text-(--muted)">
          A teacher-in-the-loop rehearsal of the pipeline with synthetic students + expert-teacher
          raters. Independent of the real focal learners and real raters.
        </p>
      </div>

      <SyntheticRunStatus progress={progress} />

      <div className="space-y-3">
        <SyntheticContextStep context={context} defaults={defaults.data} />

        {phase("Generate & validate · H1")}
        {step(
          "Generate study packs — C0–C3 (Run H1)",
          2,
          () =>
            launch.mutate(
              { hypothesis: "H1" },
              { onSuccess: () => note("H1 queued — compiling C0–C3 (C4 staged)."), onError: fail }
            ),
          launch.isPending
        )}
        <p className="pl-9 text-[11px] text-(--muted)">
          Compiles C0–C3 from the approved lesson plan and stages C4 (a copy of C3) for review.
        </p>

        {step(
          "Synthetic teacher reviews C3 → C4",
          3,
          () =>
            syntheticTeacher.mutate(undefined, {
              onSuccess: () => note(`Synthetic teacher review queued. ${LIVE}`),
              onError: fail,
            }),
          syntheticTeacher.isPending
        )}

        {phase("Personalise · H2")}
        {step(
          "Synthetic class answers the diagnostic (seeds H2)",
          4,
          () =>
            syntheticStudents.mutate(6, {
              onSuccess: () => note(`6 synthetic students queued. ${LIVE}`),
              onError: fail,
            }),
          syntheticStudents.isPending,
          !basePackApproved
        )}
        {!basePackApproved ? (
          <p className="pl-9 text-[11px] text-(--warning-ink)">
            Approve the class-level base pack first to unlock the synthetic class.
          </p>
        ) : null}

        {step(
          "Run H2 (P0/P1 personalisation per band)",
          5,
          () =>
            launch.mutate(
              { hypothesis: "H2" },
              { onSuccess: () => note("H2 execution queued."), onError: fail }
            ),
          launch.isPending
        )}
        {phase("Evaluate")}
        {step(
          "Synthetic rate (expert teachers)",
          6,
          () =>
            syntheticRate.mutate(undefined, {
              onSuccess: () => note(`Synthetic rating queued. ${LIVE}`),
              onError: fail,
            }),
          syntheticRate.isPending
        )}
      </div>

      <div className="space-y-2 border-t border-(--line) pt-3">
        <Button
          size="sm"
          variant="primary"
          onClick={() =>
            syntheticLoop.mutate(undefined, {
              onSuccess: () => note(`Full synthetic loop queued. ${LIVE}`),
              onError: fail,
            })
          }
          disabled={busy}
          isLoading={syntheticLoop.isPending}
        >
          Run full synthetic loop (teacher → export → rate)
        </Button>
        <p className="text-[11px] text-(--muted)">
          One click runs the teacher review + rating and auto-exports packets (C0–C3 ship
          immediately; C4 ships once the teacher approves it). Generate the packs (step 2) first.
        </p>
      </div>

      {status ? (
        <p className="rounded-xl border border-(--line) bg-(--panel)/50 px-3 py-2 text-xs text-(--muted)">
          {status}
        </p>
      ) : null}
    </div>
  );
}
