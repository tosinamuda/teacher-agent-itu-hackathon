import { useState } from "react";
import { Link } from "@/shared/router";

import { Button } from "@/shared/components/ui/Button";
import { Card } from "@/shared/components/ui/Card";

import {
  ExperimentExecution,
  ExperimentReadiness,
  Hypothesis,
  SyntheticProgressEvent,
} from "../lib/experiments";
import {
  executionErrorMessage,
  executionFailed,
  shortExecutionId,
} from "../services/executionError";

type ExperimentGenerationPanelProps = {
  hypothesis: Hypothesis;
  readiness: ExperimentReadiness;
  /** The canonical (latest) execution for this hypothesis, or null if none. */
  latest: ExperimentExecution | null;
  baseHref: string;
  isGenerating: boolean;
  isExporting: boolean;
  /** How many packets the last export made ready for raters; null before one finishes. */
  exportedPackets?: number | null;
  exportFailed?: boolean;
  /** Live generation progress over the websocket (latest per-condition event). */
  liveProgress?: SyntheticProgressEvent | null;
  /** Condition codes that failed with no succeeded run — drives partial messaging. */
  failedConditions?: string[];
  onGenerate: () => void;
  onExport: () => void;
};

/** Why generation can't run yet (null = ready). */
function blockedReason(
  hypothesis: Hypothesis,
  readiness: ExperimentReadiness,
): string | null {
  if (hypothesis === "H1") {
    return readiness.h1_ready ? null : "Approve the lesson baseline first.";
  }
  if (!readiness.h2_base_approved) return "Run H1 first: H2 personalises its first draw's C3 pack.";
  if (!readiness.learner_evidence_ready) return "Collect learner evidence first.";
  return null;
}

/**
 * State-aware generation control. H1's C0–C3 are NOT researcher-triggered here:
 * they generate together with the class revision note when the *teacher* runs
 * "Create the class revision note" on their lesson-prep page (create_review_note →
 * the H1 build), so this researcher lab only *reports* H1 state — it offers no
 * launch or retry. H2 (personalisation) IS researcher-triggered. Once generated,
 * C0–C3 are frozen (only C4 re-iterates, via the teacher gate); H2 keeps a
 * guarded re-generate.
 */
export function ExperimentGenerationPanel({
  hypothesis,
  readiness,
  latest,
  baseHref,
  isGenerating,
  isExporting,
  exportedPackets = null,
  exportFailed = false,
  liveProgress,
  failedConditions = [],
  onGenerate,
  onExport,
}: ExperimentGenerationPanelProps) {
  const [confirmRerun, setConfirmRerun] = useState(false);
  const blocked = blockedReason(hypothesis, readiness);
  // H1 produces C0–C3; C4 is NOT a 5th generation — it's C3's pack put in front
  // of the teacher to review/approve (the C4 gate), shown below.
  const conditionLabel = hypothesis === "H1" ? "C0–C3" : "P0 / P1";

  const status = latest?.status ?? null;
  const inFlight = status != null && /queue|run|pending|created/i.test(status);
  const failed = latest != null && executionFailed(latest);
  // Partial: the run failed but specific conditions are the cause — recover
  // those per condition (in the table below), not by re-running the whole set.
  const isPartial = failed && failedConditions.length > 0;
  // Trust the conditions, not just the execution status: treat as generated when
  // the execution succeeded OR every present condition succeeded (a stale failed
  // status — e.g. after a re-dispatch — must not override real, usable packs).
  const anyConditionSucceeded = (latest?.condition_runs ?? []).some((run) =>
    /succeed|complete|done/i.test(run.status),
  );
  const succeeded =
    status === "succeeded" ||
    (!inFlight && anyConditionSucceeded && failedConditions.length === 0);

  // --- Not generated yet ---
  if (latest == null) {
    // H1 is teacher-owned: this lab observes it but never launches it — the
    // teacher's "Create the class revision note" step runs the H1 build. Only H2
    // (personalisation) is researcher-triggered here.
    const teacherOwned = hypothesis === "H1";
    return (
      <Card padding="lg" className="space-y-3">
        <Header
          hypothesis={hypothesis}
          state={teacherOwned ? "Awaiting the teacher" : "Not generated yet"}
        />
        <p className="text-sm text-(--muted)">
          {teacherOwned
            ? "C0–C3 generate together with the class revision note when the teacher runs “Create the class revision note.” C3’s pack then goes to the teacher to review/approve — that approval is the C4 gate."
            : `Generate ${conditionLabel} for each focal learner.`}
        </p>
        {blocked ? (
          <p className="text-sm text-(--danger-ink)">{blocked}</p>
        ) : teacherOwned ? null : (
          <Button onClick={onGenerate} isLoading={isGenerating}>
            Generate {conditionLabel}
          </Button>
        )}
      </Card>
    );
  }

  return (
    <Card padding="lg" className="space-y-3">
      <Header
        hypothesis={hypothesis}
        state={
          succeeded
            ? `${conditionLabel} generated`
            : inFlight
              ? `Generating ${conditionLabel}…`
              : isPartial
                ? `${failedConditions.join(", ")} failed`
                : failed
                  ? "Generation failed"
                  : (status ?? "—")
        }
        tone={succeeded ? "ok" : failed ? "bad" : "neutral"}
      />
      <p className="font-mono text-xs text-(--muted)" title={latest.execution_id}>
        Attempt {latest.attempt_number} · {shortExecutionId(latest.execution_id)}
      </p>

      {inFlight ? (
        <div className="space-y-1">
          {liveProgress?.total ? (
            <div className="h-1.5 w-full overflow-hidden rounded-none bg-(--sunken)">
              <div
                className="h-full bg-(--accent) transition-[width]"
                style={{
                  width: `${Math.round(((liveProgress.done ?? 0) / liveProgress.total) * 100)}%`,
                }}
              />
            </div>
          ) : null}
          <p className="text-xs text-(--muted)">
            {liveProgress?.total ? `${liveProgress.done ?? 0} / ${liveProgress.total} · ` : ""}
            {liveProgress?.message ?? "Working… live per-condition updates appear here."}
          </p>
        </div>
      ) : null}

      {isPartial ? (
        <p className="border border-(--danger-ink)/30 bg-(--danger-tint)/40 px-3 py-2 text-sm text-(--ink)">
          <span className="font-semibold text-(--danger-ink)">
            {failedConditions.join(", ")} failed to generate
          </span>{" "}
          — retry {failedConditions.length === 1 ? "it" : "them"} in the conditions table below. The
          other conditions succeeded and are frozen, so the whole set is not re-run.
        </p>
      ) : failed && !succeeded ? (
        <div className="space-y-2">
          <p className="text-sm text-(--danger-ink)">{executionErrorMessage(latest)}</p>
          {hypothesis === "H1" ? (
            // H1 is teacher-owned — recovery is the teacher re-running "Create the
            // class revision note", not a researcher relaunch from this lab.
            <p className="text-xs text-(--muted)">
              Ask the teacher to re-run “Create the class revision note” to regenerate C0–C3.
            </p>
          ) : (
            <Button onClick={onGenerate} isLoading={isGenerating} variant="secondary" size="sm">
              Try again
            </Button>
          )}
        </div>
      ) : null}

      {succeeded && hypothesis === "H1" ? (
        <div className="border border-(--line) bg-(--sunken)/40 px-3 py-2 text-sm">
          {readiness.base_pack_approved ? (
            <p className="text-emerald-800">
              ✓ Teacher accepted the class-level pack (C4).
            </p>
          ) : (
            <p className="text-(--ink)">
              <span className="font-semibold text-(--accent-deep)">Teacher gate (C4):</span>{" "}
              the class-level pack is awaiting teacher review.{" "}
              <Link className="font-semibold text-(--accent-deep) hover:underline" href={`${baseHref}/results`}>
                Open review →
              </Link>
            </p>
          )}
        </div>
      ) : null}

      {succeeded ? (
        <div className="space-y-2 pt-1">
          <div className="flex flex-wrap items-center gap-2">
            <Button onClick={onExport} isLoading={isExporting} variant="secondary" size="sm">
              Export packets
            </Button>
            {exportedPackets != null ? (
              <span className="text-xs text-(--muted)">
                {exportedPackets} {exportedPackets === 1 ? "packet" : "packets"} ready for raters
              </span>
            ) : null}
            {exportFailed ? (
              <span className="text-xs text-(--danger-ink)">Couldn&apos;t export — try again.</span>
            ) : null}
            {/* H2 isn't frozen — re-personalising is legitimate. H1's C0–C3 are
                frozen for reproducibility, so no re-generate is offered there. */}
            {hypothesis === "H2" ? (
              confirmRerun ? (
                <span className="inline-flex items-center gap-2 text-xs text-(--muted)">
                  Replace the current generation?
                  <button
                    type="button"
                    className="font-semibold text-(--danger-ink) hover:underline"
                    onClick={() => {
                      setConfirmRerun(false);
                      onGenerate();
                    }}
                  >
                    Re-generate
                  </button>
                  <button type="button" className="hover:underline" onClick={() => setConfirmRerun(false)}>
                    Cancel
                  </button>
                </span>
              ) : (
                <button
                  type="button"
                  className="text-xs text-(--muted) underline hover:text-(--ink)"
                  onClick={() => setConfirmRerun(true)}
                >
                  Re-generate (replaces current)
                </button>
              )
            ) : null}
          </div>
          {hypothesis === "H1" ? (
            <p className="text-[11px] text-(--muted)">
              C0–C3 are frozen for reproducibility — only C4 re-iterates, via the teacher gate.
            </p>
          ) : null}
        </div>
      ) : null}
    </Card>
  );
}

function Header({
  hypothesis,
  state,
  tone = "neutral",
}: {
  hypothesis: Hypothesis;
  state: string;
  tone?: "ok" | "bad" | "neutral";
}) {
  const toneClass =
    tone === "ok"
      ? "text-emerald-700"
      : tone === "bad"
        ? "text-(--danger-ink)"
        : "text-(--ink)";
  return (
    <div className="flex items-baseline justify-between gap-3">
      <p className="text-xs font-semibold uppercase tracking-[0.18em] text-(--muted)">
        {hypothesis} generation
      </p>
      <p className={`text-sm font-semibold ${toneClass}`}>{state}</p>
    </div>
  );
}
