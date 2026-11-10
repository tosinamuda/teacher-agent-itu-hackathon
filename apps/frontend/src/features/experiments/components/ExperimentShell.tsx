import type { ReactNode } from "react";
import { Link } from "@/shared/router";
import { usePathname } from "@/shared/router";

import { Button } from "@/shared/components/ui/Button";
import { TabBar } from "@/shared/components/ui/TabBar";

import { EndStudyControl } from "./EndStudyControl";
import { useExperiment } from "../hooks/useExperiments";
import { useEndExperiment } from "../hooks/useExperimentResults";
import { ExperimentDetail } from "../lib/experiments";

type LifecycleStage = "setup" | "execute" | "evaluate" | "report";

type Tab = {
  slug: string;
  label: string;
  /** Long-form rater-/teacher-friendly hint shown in the tab's hover tooltip. */
  hint: string;
  /** Which lifecycle stage the tab belongs to — small tag rendered under the label. */
  stage: LifecycleStage;
};

/**
 * Tabs are ordered to mirror the experiment lifecycle (setup → execute →
 * evaluate → report). Each tab carries an explicit lifecycle stage so the user
 * can see where the tab fits in the workflow, not just what it does.
 */
const TABS: readonly Tab[] = [
  { slug: "", label: "Overview", hint: "Study context and readiness", stage: "setup" },
  {
    slug: "/h1",
    label: "H1 setup",
    hint: "Hypothesis 1 — curriculum alignment (conditions C0–C4)",
    stage: "setup",
  },
  {
    slug: "/h2",
    label: "H2 setup",
    hint: "Hypothesis 2 — personalisation (P0 base vs P1 personalised)",
    stage: "setup",
  },
  {
    slug: "/run",
    label: "Test",
    hint: "Run a test (an end-to-end execution of the experiment pipeline)",
    stage: "execute",
  },
  { slug: "/live", label: "Live", hint: "Watch a running execution", stage: "execute" },
  {
    slug: "/raters",
    label: "Raters",
    hint: "Assign expert raters to H1 lesson, H2 focal cases, and audit items",
    stage: "evaluate",
  },
  {
    slug: "/results",
    label: "Results",
    hint: "Expert-rater statistics and progress",
    stage: "evaluate",
  },
  {
    slug: "/story",
    label: "Story",
    hint: "Per-learner journey narrative",
    stage: "report",
  },
  {
    slug: "/compare",
    label: "Compare",
    hint: "Side-by-side C0–C3 / base-vs-P1 view",
    stage: "report",
  },
];

/** End Study is destructive — only surfaced on safe surfaces (away from Live monitor). */
const END_STUDY_ALLOWED_SLUGS: ReadonlySet<string> = new Set(["", "/results"]);

/** What an ended experiment can still be opened for: nothing runs, so no Test or Live. */
const ENDED_TAB_LABEL: Record<string, string | null> = {
  "/h1": "H1",
  "/h2": "H2",
  "/run": null,
  "/live": null,
};

function tabsFor(isEnded: boolean): Tab[] {
  if (!isEnded) return [...TABS];
  return TABS.flatMap((tab) => {
    if (!(tab.slug in ENDED_TAB_LABEL)) return [tab];
    const label = ENDED_TAB_LABEL[tab.slug];
    return label ? [{ ...tab, label }] : [];
  });
}

/**
 * Friendly breadcrumb labels for the read-only preview sub-routes that aren't
 * in the tab bar (e.g. `/lesson-plan`, `/assessment`, `/c0`–`/c3`). When the
 * current path matches one of these, the breadcrumb's trailing crumb shows the
 * label and the tab bar shows no active tab.
 */
const PREVIEW_ROUTE_LABEL: Record<string, string> = {
  "/lesson-plan": "Lesson plan",
  "/assessment": "Exit assessment",
  "/c0": "C0 pack",
  "/c1": "C1 pack",
  "/c2": "C2 pack",
  "/c3": "C3 pack",
};

/**
 * Coarse lifecycle state of the *real* study. Crucially, "Evaluated" advances only
 * on expert ratings (evaluation_mode live/mixed) — a synthetic-only dry run does NOT
 * advance it; that shows as the orthogonal "Rehearsed" chip instead.
 */
function lifecycleIndex(experiment: ExperimentDetail | undefined): number {
  if (experiment?.lifecycle_status === "ended") return 4;
  const mode = experiment?.evaluation_mode;
  if (mode === "live" || mode === "mixed") return 3;
  const executions = experiment?.executions ?? [];
  if (executions.some((e) => /run|queue|pending|progress/i.test(e.status ?? ""))) return 1;
  if (executions.some((e) => /succeed|complete|done/i.test(e.status ?? ""))) return 2;
  return 0;
}

/**
 * Persistent shell for one experiment: a header (breadcrumb + lesson title +
 * Rehearsed chip + lifecycle-aware primary action + guarded End-Study), and a
 * tab bar ordered by lifecycle (setup, execute, evaluate, report), with a gap
 * where the stage changes. An ended experiment has no Test or Live tab.
 */
export function ExperimentShell({
  experimentId,
  children,
}: {
  experimentId: string;
  children: ReactNode;
}) {
  const pathname = usePathname();
  const experimentQuery = useExperiment(experimentId);
  const endStudy = useEndExperiment(experimentId);

  const experiment = experimentQuery.data;
  const base = `/research/experiments/${experimentId}`;
  const stage = lifecycleIndex(experiment);
  const isEnded = stage === 4;
  const running = stage === 1;
  // Orthogonal to the lifecycle: a synthetic dry run has produced proxy ratings.
  const rehearsed =
    experiment?.evaluation_mode === "synthetic" || experiment?.evaluation_mode === "mixed";
  // The classroom context (grade · subject) — the study's scope, links up to the parent.
  const workspaceLabel = [
    experiment?.grade_level ?? experiment?.class_name,
    experiment?.subject_name,
  ]
    .filter(Boolean)
    .join(" · ");
  const experimentCode = experiment?.experiment_code ?? experimentId;
  // Show the lesson title; only fall back to a friendly placeholder, never the
  // raw plan_version_id (which is a UUID and reads as a leaked internal id).
  const lessonSubtitle = experiment?.lesson_title ?? "Lesson plan unset";

  // Most-specific tab wins (so Overview doesn't light up on every sub-route).
  // For the preview sub-routes (e.g. `/lesson-plan`, `/c0`) we want no tab
  // active and the breadcrumb to show the preview label, so we start the
  // reducer with `null` instead of `""` (Overview) and only promote a slug
  // when the path actually matches it.
  const tabs = tabsFor(isEnded);
  const activeSlug = tabs.reduce<string | null>((best, tab) => {
    const href = base + tab.slug;
    const match = tab.slug === "" ? pathname === base : pathname.startsWith(href);
    if (!match) return best;
    if (best === null) return tab.slug;
    return tab.slug.length >= best.length ? tab.slug : best;
  }, null);
  const activeTab = activeSlug !== null ? tabs.find((tab) => tab.slug === activeSlug) : undefined;
  const showEndStudyControl =
    activeSlug !== null && END_STUDY_ALLOWED_SLUGS.has(activeSlug);
  // Preview sub-route (lesson plan, assessment, c0–c3) — no tab matches,
  // so use the friendly label table for the breadcrumb trailing crumb.
  // pathname slice gives `"/lesson-plan"` etc., so the first segment is at
  // index [1] after the empty leading-slash split entry.
  const previewSegment =
    activeSlug === null ? pathname.slice(base.length).split("/")[1] : null;
  const previewLabel = previewSegment ? PREVIEW_ROUTE_LABEL[`/${previewSegment}`] : undefined;

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div className="min-w-0 flex-1 space-y-1">
          <nav className="flex min-w-0 flex-wrap items-center gap-1.5 text-xs text-(--muted)">
            <Link href="/research" className="hover:text-(--accent-deep)">
              Studies
            </Link>
            {workspaceLabel ? (
              <>
                <span aria-hidden>›</span>
                {experiment?.investigation_id ? (
                  <Link
                    href={`/research/investigations/${experiment.investigation_id}`}
                    className="max-w-[28ch] truncate hover:text-(--accent-deep)"
                    title={experiment.investigation_code ?? workspaceLabel}
                  >
                    {workspaceLabel}
                  </Link>
                ) : (
                  <span className="max-w-[28ch] truncate" title={workspaceLabel}>
                    {workspaceLabel}
                  </span>
                )}
              </>
            ) : null}
            <span aria-hidden>›</span>
            <span
              className="max-w-[24ch] truncate font-mono text-[11px] font-semibold tracking-tight text-(--accent-deep)"
              title={experimentCode}
            >
              {experimentCode}
            </span>
            {activeTab && activeTab.slug !== "" ? (
              <>
                <span aria-hidden>›</span>
                <span className="font-medium text-(--ink-2)">{activeTab.label}</span>
              </>
            ) : previewLabel ? (
              <>
                <span aria-hidden>›</span>
                <span className="font-medium text-(--ink-2)">{previewLabel}</span>
              </>
            ) : null}
          </nav>
          {/* Page title is the lesson — the experiment code is the breadcrumb's
              last crumb, so repeating it as an <h1> here would just stack the
              same string twice. The lesson tells the rater "what is this study
              about" in plain English. */}
          <h1
            className="truncate text-2xl font-semibold tracking-tight text-(--ink)"
            title={lessonSubtitle}
          >
            {lessonSubtitle}
          </h1>
        </div>
        <div className="flex shrink-0 items-center gap-2">
          {experiment?.is_sandbox ? (
            <span
              className="inline-flex items-center whitespace-nowrap rounded-none border border-(--warning-ink) bg-(--warning-tint) px-2.5 py-1 text-[11px] font-semibold uppercase tracking-[0.1em] text-(--warning-ink)"
              title="Sandbox experiment — throwaway/test. Excluded from the investigation rollup and real reporting."
            >
              Sandbox
            </span>
          ) : null}
          {rehearsed ? (
            <span
              className="inline-flex items-center whitespace-nowrap rounded-none border border-dashed border-(--accent) px-2.5 py-1 text-[11px] font-semibold text-(--accent-deep)"
              title="A synthetic dry run produced proxy ratings. These are excluded from reported expert results."
            >
              ⟳ Rehearsed
            </span>
          ) : null}
          {!isEnded ? (
            <Link href={running ? `${base}/live` : `${base}/run`}>
              <Button size="sm" variant="primary">
                {running ? "Watch live →" : "Run test →"}
              </Button>
            </Link>
          ) : null}
          {showEndStudyControl ? (
            <EndStudyControl
              isEnded={isEnded}
              endedBy={experiment?.ended_by}
              onEnd={() => endStudy.mutate()}
              isEnding={endStudy.isPending}
            />
          ) : null}
        </div>
      </div>

      <TabBar
        label="Experiment workspace"
        tabs={tabs.map((tab, index) => ({
          href: base + tab.slug,
          label: tab.label,
          hint: tab.hint,
          active: tab.slug === activeSlug,
          gapBefore: index > 0 && tabs[index - 1].stage !== tab.stage,
        }))}
      />

      <div className="min-w-0">{children}</div>
    </div>
  );
}
