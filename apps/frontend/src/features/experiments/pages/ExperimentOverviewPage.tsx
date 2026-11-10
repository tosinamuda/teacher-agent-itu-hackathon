import { Link } from "@/shared/router";

import { Card } from "@/shared/components/ui/Card";
import { Section } from "@/shared/components/ui/Section";
import { formatRelativeTime, parseApiMoment } from "@/shared/utils/relativeTime";

import { ConcludedRecordCard } from "../components/ConcludedRecordCard";
import { ProvenanceSection } from "../components/ProvenanceSection";
import { WorkflowChecklist } from "../components/WorkflowChecklist";
import { useExperiment, useSetExperimentSandbox } from "../hooks/useExperiments";
import { useExperimentStatistics } from "../hooks/useExperimentResults";
import { useExperimentWorkflow } from "../hooks/useExperimentWorkflow";
import type {
  ExperimentDetail,
  ExperimentReadiness,
  ExperimentStatistics,
  SourceAuditDescriptives,
} from "../lib/experiments";
import type { WorkflowSnapshot } from "../lib/workflow";

type ExperimentOverviewPageProps = {
  experimentId: string;
};

/**
 * `baseline_version_label` arrives as `LPV-<uuid> · approved <date>`. Pull the
 * two halves apart so the KPI strip can show them as separate signals: the
 * version id (truncated) for identification, and the approval date for recency.
 */
function splitBaselineLabel(
  label: string | null | undefined,
): { versionId: string; approved: string } | null {
  if (!label) return null;
  const idx = label.indexOf(" · ");
  if (idx > 0 && /^lpv-/i.test(label)) {
    const id = label.slice(0, idx);
    const tail = label.slice(idx + 3).replace(/^approved\s+/i, "");
    const truncated = id.length > 18 ? `${id.slice(0, 10)}…${id.slice(-6)}` : id;
    return { versionId: truncated, approved: `baseline approved ${tail}` };
  }
  return { versionId: label, approved: "baseline" };
}

function lastActivityIso(experiment: ExperimentDetail): string | undefined {
  const candidates = (experiment.executions ?? [])
    .flatMap((execution) => [execution.updated_at, execution.created_at])
    .filter((value): value is string => Boolean(value));
  if (candidates.length === 0) return undefined;
  return candidates.sort((a, b) => parseApiMoment(a) - parseApiMoment(b)).slice(-1)[0];
}

/**
 * Three-item KPI strip — class size, baseline plan version id, baseline
 * approval recency. All the *count* signals (evidence, focal, conditions,
 * ratings) now live as phase rollups inside the workflow accordion, so they
 * are not duplicated here.
 */
function compactKpis(experiment: ExperimentDetail) {
  const baseline = splitBaselineLabel(experiment.baseline_version_label);
  return [
    {
      key: "learners",
      value: `${experiment.learner_count} learner${experiment.learner_count === 1 ? "" : "s"}`,
    },
    {
      key: "version",
      value: baseline?.versionId ?? "no baseline",
      title: experiment.baseline_version_label ?? undefined,
    },
    {
      key: "approved",
      value: baseline?.approved
        ? experiment.baseline_approved_by
          ? `${baseline.approved} · by ${experiment.baseline_approved_by}`
          : baseline.approved
        : "baseline not selected",
      title: experiment.baseline_approved_by ?? undefined,
    },
  ];
}

/** Translate readiness signal into the unmet preconditions for a hypothesis. */
function unmetPreconditions(
  readiness: ExperimentReadiness | undefined,
  hypothesis: "h1" | "h2",
): string[] {
  if (!readiness) return [];
  const missing: string[] = [];
  if (!readiness.lesson_approved) missing.push("lesson plan not approved");
  if (hypothesis === "h1" && !readiness.lesson_note_approved) {
    missing.push("lesson note not approved");
  }
  if (!readiness.baseline_selected) missing.push("baseline version not chosen");
  if (hypothesis === "h2") {
    if (!readiness.h2_base_approved) missing.push("first-draw C3 pack not ready");
    if (!readiness.learner_evidence_ready) missing.push("learner evidence not collected");
  }
  return missing;
}

type StreamStatus = "ready" | "blocked" | "in_progress" | "complete";

const STREAM_STYLE: Record<StreamStatus, string> = {
  ready: "border-(--accent-soft) bg-(--accent-soft)/40",
  blocked: "border-(--line)",
  in_progress: "border-(--accent) bg-(--accent-soft)/30",
  complete: "border-emerald-500/40 bg-emerald-50",
};

const STREAM_STATUS_LABEL: Record<StreamStatus, string> = {
  ready: "Ready",
  blocked: "Not ready",
  in_progress: "In progress",
  complete: "Complete",
};

function teacherStreamStatus(
  c3Available: boolean,
  basePackApproved: boolean,
): { status: StreamStatus; detail: string } {
  // C4 is the classroom teacher's gate ONLY: they review + edit the C3 base
  // pack (each edit logged) and approve it. Approval is the C4-ready signal
  // (base_pack_approved). The researcher observes — they don't record C4.
  if (!c3Available) {
    return { status: "blocked", detail: "Awaiting C3 packs for teacher review" };
  }
  if (basePackApproved) {
    return { status: "complete", detail: "Approved by the teacher" };
  }
  return { status: "ready", detail: "C3 pack ready — awaiting the teacher's review" };
}

function auditStreamStatus(
  audit: SourceAuditDescriptives | undefined,
  packsMade: boolean,
): { status: StreamStatus; detail: string } {
  if (!audit || audit.n_items === 0) {
    return packsMade
      ? { status: "blocked", detail: "C2/C3 packs made · no excerpts sampled yet" }
      : { status: "blocked", detail: "Awaiting C2/C3 packs to sample from" };
  }
  if (audit.n_ratings === 0) {
    return { status: "ready", detail: `${audit.n_items} items queued · 0 ratings` };
  }
  return {
    status: "in_progress",
    detail: `${audit.n_ratings} ratings on ${audit.n_items} items`,
  };
}

/**
 * One of the four evaluation streams the protocol defines. Sits ABOVE the
 * workflow accordion so the researcher sees the conceptual framing ("what is
 * each stream measuring?") before they walk the workflow rows for that
 * stream's per-step state.
 */
function StreamCard({
  letter,
  title,
  measures,
  href,
  status,
  detail,
}: {
  letter: string;
  title: string;
  measures: string;
  href: string;
  status: StreamStatus;
  detail: string;
}) {
  return (
    <Link
      href={href}
      className={`flex min-w-0 flex-col gap-2 border px-3 py-2 transition hover:bg-(--sunken) ${STREAM_STYLE[status]}`}
    >
      <div className="flex items-baseline justify-between gap-2 text-xs">
        <span className="font-semibold uppercase tracking-[0.16em] text-(--accent-deep)">
          {letter}
        </span>
        <span className="font-semibold uppercase tracking-[0.14em] text-(--muted)">
          {STREAM_STATUS_LABEL[status]}
        </span>
      </div>
      <p className="text-sm font-semibold text-(--ink)">{title}</p>
      <p className="text-[11px] leading-relaxed text-(--muted)">{measures}</p>
      <p className="mt-auto text-xs font-medium text-(--accent-deep)">{detail} →</p>
    </Link>
  );
}

function FourStreams({
  base,
  experiment,
  stats,
}: {
  base: string;
  experiment: ExperimentDetail;
  stats: ExperimentStatistics | undefined;
}) {
  const h1Missing = unmetPreconditions(experiment.readiness, "h1");
  const h2Missing = unmetPreconditions(experiment.readiness, "h2");
  const c3Available =
    experiment.h1_summary.execution_count > 0 &&
    experiment.h1_summary.latest_execution_status === "succeeded";
  const teacher = teacherStreamStatus(
    c3Available,
    Boolean(experiment.readiness.base_pack_approved),
  );
  const audit = auditStreamStatus(
    stats?.source_audit,
    experiment.h1_summary.latest_execution_status === "succeeded",
  );
  return (
    <div className="grid gap-2 sm:grid-cols-2 xl:grid-cols-4">
      <StreamCard
        letter="H1"
        title="Curriculum alignment"
        measures="C0–C3 packs on the same lesson, rated for lesson-plan alignment."
        href={`${base}/h1`}
        status={experiment.h1_summary.ready ? "ready" : "blocked"}
        detail={
          experiment.h1_summary.ready
            ? "Open H1 setup"
            : h1Missing.length > 0
              ? `Missing: ${h1Missing.join(", ")}`
              : "Not ready"
        }
      />
      <StreamCard
        letter="H2"
        title="Personalisation"
        measures="P0 base pack vs P1 personalised pack, per focal learner."
        href={`${base}/h2`}
        status={experiment.h2_summary.ready ? "ready" : "blocked"}
        detail={
          experiment.h2_summary.ready
            ? "Open H2 setup"
            : h2Missing.length > 0
              ? `Missing: ${h2Missing.join(", ")}`
              : "Not ready"
        }
      />
      <StreamCard
        letter="C4"
        title="Teacher governance"
        measures="Teacher approves / regenerates / rejects each generated pack. Process evidence."
        href={`${base}/results`}
        status={teacher.status}
        detail={teacher.detail}
      />
      <StreamCard
        letter="Audit"
        title="Source grounding"
        measures="Excerpts from C2/C3 packs scored against their cited textbook source."
        href={`${base}/results`}
        status={audit.status}
        detail={audit.detail}
      />
    </div>
  );
}

/**
 * Top banner — the single suggested next action plus an "N items need
 * attention" pill when the backend flagged any failures. Both fields come
 * straight from the `/workflow` snapshot — no client-side derivation.
 */
function NextActionBanner({
  base,
  snapshot,
}: {
  base: string;
  snapshot: WorkflowSnapshot | undefined;
}) {
  if (!snapshot) return null;
  const next = snapshot.next_action ?? null;
  const attention = snapshot.attention ?? [];
  if (!next && attention.length === 0) {
    return (
      <Card padding="md" className="flex flex-wrap items-baseline gap-2">
        <p className="text-sm font-semibold text-emerald-700">
          ✓ Every workflow step is in progress or complete.
        </p>
      </Card>
    );
  }
  return (
    <Card padding="md" className="flex flex-wrap items-baseline justify-between gap-3">
      {next ? (
        <p className="text-sm text-(--ink)">
          <span className="font-semibold text-(--accent-deep)">Next:</span> {next.label}
          {next.href ? (
            <Link
              className="ml-2 font-semibold text-(--accent-deep) hover:underline"
              href={base + next.href}
            >
              open →
            </Link>
          ) : null}
        </p>
      ) : (
        <p className="text-sm text-(--muted)">No clear next action.</p>
      )}
      {attention.length > 0 ? (
        <p className="text-sm font-semibold text-rose-700">
          ⚠ {attention.length} item{attention.length === 1 ? "" : "s"} need attention
        </p>
      ) : null}
    </Card>
  );
}

/** Researcher toggle: mark the experiment as a throwaway sandbox. */
function SandboxToggle({ experimentId, isSandbox }: { experimentId: string; isSandbox: boolean }) {
  const mutation = useSetExperimentSandbox(experimentId);
  return (
    <label className="flex cursor-pointer items-start gap-2 text-sm">
      <input
        type="checkbox"
        className="mt-0.5"
        checked={isSandbox}
        disabled={mutation.isPending}
        onChange={(event) => mutation.mutate(event.target.checked)}
      />
      <span>
        <span className="font-semibold text-(--ink)">Sandbox (test) experiment</span>
        <span className="block text-xs text-(--muted)">
          A throwaway run — excluded from the investigation tally and real reporting, and badged
          “Sandbox”. Use for dev/demo experiments that must never count.
        </span>
      </span>
    </label>
  );
}

function SkeletonShell() {
  return (
    <main className="flex w-full flex-col gap-3 py-2">
      {[0, 1].map((index) => (
        <Card key={index} padding="md">
          <div className="h-4 w-2/3 animate-pulse bg-(--sunken)" />
        </Card>
      ))}
      <Card padding="lg" className="space-y-3">
        <div className="h-3 w-32 animate-pulse bg-(--sunken)" />
        {[0, 1, 2, 3].map((index) => (
          <div key={index} className="h-4 w-full animate-pulse bg-(--sunken)/60" />
        ))}
      </Card>
    </main>
  );
}

/** Renders the experiment Overview as a workflow + next-action command center. */
export function ExperimentOverviewPage({ experimentId }: ExperimentOverviewPageProps) {
  const experimentQuery = useExperiment(experimentId);
  const experiment = experimentQuery.data ?? null;
  const statsQuery = useExperimentStatistics(experiment?.experiment_id ?? null);
  const stats: ExperimentStatistics | undefined = statsQuery.data ?? undefined;
  // Backend-derived workflow snapshot — the four-streams cards stay client-side
  // (small enough, conceptual framing only), but the 18-row checklist + next
  // action + attention list all come from the `/workflow` endpoint now.
  const workflowQuery = useExperimentWorkflow(experiment?.experiment_id ?? null);
  const snapshot = workflowQuery.data;

  if (experimentQuery.isLoading) {
    return <SkeletonShell />;
  }

  if (experimentQuery.isError || !experiment) {
    return (
      <main className="w-full py-8">
        <Card padding="lg">
          <h1 className="text-2xl font-semibold text-[color:var(--ink)]">Experiment not found</h1>
          <p className="mt-2 text-sm text-[color:var(--muted)]">
            We could not load the requested experiment baseline.
          </p>
          <Link
            className="mt-4 inline-flex text-sm font-semibold text-[color:var(--accent-deep)] hover:underline"
            href="/research"
          >
            Back to studies
          </Link>
        </Card>
      </main>
    );
  }

  const base = `/research/experiments/${experiment.experiment_id}`;
  const lastActivity = formatRelativeTime(lastActivityIso(experiment));
  const kpis = compactKpis(experiment);

  return (
    <main className="flex w-full min-w-0 flex-col gap-3 py-4">
      {/* Setup signals — who, which baseline, when approved — for an experiment still running. */}
      {experiment.lifecycle_status === "ended" ? null : (
        <div className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1 border-b border-(--line) pb-2 text-xs text-(--muted)">
          <div className="flex min-w-0 flex-wrap items-baseline gap-x-4 gap-y-1">
            {kpis.map((kpi, index) => (
              <span key={kpi.key} title={kpi.title} className="text-(--ink)">
                {kpi.value}
                {index < kpis.length - 1 ? <span className="ml-4 text-(--muted)">·</span> : null}
              </span>
            ))}
          </div>
          {lastActivity ? (
            <span>Last activity {lastActivity}</span>
          ) : (
            <span>No activity yet</span>
          )}
        </div>
      )}

      {experiment.lifecycle_status === "ended" ? (
        <ConcludedRecordCard experiment={experiment} base={base} />
      ) : (
        <>
          <NextActionBanner base={base} snapshot={snapshot} />

          {/* Conceptual framing — the four evaluation streams the protocol defines.
              Sits above the workflow so the researcher learns the framework once
              per session; the workflow accordion below carries the operational
              per-step state. */}
          <FourStreams base={base} experiment={experiment} stats={stats} />

          <WorkflowChecklist
            phases={snapshot?.phases ?? []}
            summary={snapshot?.summary}
            base={base}
          />
        </>
      )}

      <div className="mt-6 space-y-8">
        <ProvenanceSection experimentId={experiment.experiment_id} />
        {experiment.lifecycle_status === "ended" ? null : (
          <Section title="Settings">
            <SandboxToggle
              experimentId={experiment.experiment_id}
              isSandbox={Boolean(experiment.is_sandbox)}
            />
          </Section>
        )}
      </div>
    </main>
  );
}
