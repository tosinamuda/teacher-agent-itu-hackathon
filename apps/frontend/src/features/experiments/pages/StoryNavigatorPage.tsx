import { useMemo } from "react";
import { Link } from "@/shared/router";

import { Badge } from "@/shared/components/ui/Badge";
import { Button } from "@/shared/components/ui/Button";
import { Card } from "@/shared/components/ui/Card";

import { useExperiments } from "../hooks/useExperiments";
import { ExperimentSummary } from "../lib/experiments";

/** Maps an experiment status string to a Badge variant. */
function statusVariant(status: string): "success" | "warning" | "error" | "default" {
  const value = status.toLowerCase();
  if (value.includes("fail")) return "error";
  if (value.includes("run") || value.includes("queue")) return "warning";
  if (value.includes("succeed") || value.includes("complete") || value.includes("ready")) {
    return "success";
  }
  return "default";
}

type SchemeGroup = {
  key: string;
  label: string;
  subtitle: string;
  experiments: ExperimentSummary[];
};

/** Groups experiments by their scheme-of-work context (subject · grade · class · term). */
function groupBySchemeOfWork(experiments: ExperimentSummary[]): SchemeGroup[] {
  const groups = new Map<string, SchemeGroup>();
  for (const experiment of experiments) {
    const key =
      [experiment.subject_name, experiment.grade_level, experiment.class_name, experiment.term]
        .filter(Boolean)
        .join(" · ") || "Other experiments";
    const label =
      [experiment.subject_name, experiment.grade_level].filter(Boolean).join(" · ") ||
      "Experiments";
    const subtitle = [experiment.term, experiment.school_name].filter(Boolean).join(" · ");
    const group = groups.get(key) ?? { key, label, subtitle, experiments: [] };
    group.experiments.push(experiment);
    groups.set(key, group);
  }
  return [...groups.values()];
}

/**
 * The scheme-of-work entry into Experiment Stories: browse experiments grouped by
 * their curriculum context (subject · grade · class · term), then open any lesson's
 * story to walk its pipeline — rendered artefacts with a per-step generation trace.
 */
export function StoryNavigatorPage() {
  const experimentsQuery = useExperiments({});
  const experiments = useMemo(() => experimentsQuery.data ?? [], [experimentsQuery.data]);
  const groups = useMemo(() => groupBySchemeOfWork(experiments), [experiments]);

  return (
    <div className="space-y-6">
      <header className="space-y-1">
        <p className="text-xs font-semibold uppercase tracking-[0.18em] text-(--muted)">
          Experiment stories
        </p>
        <h1 className="text-2xl font-semibold text-(--ink)">Browse by scheme of work</h1>
        <p className="text-sm text-(--muted)">
          Pick a subject and lesson to walk its experiment story end to end — rendered artefacts,
          with every generated step traceable to its raw LLM calls.
        </p>
      </header>

      {experimentsQuery.isLoading ? (
        <p className="text-sm text-(--muted)">Loading experiments…</p>
      ) : null}
      {experimentsQuery.isError ? (
        <p className="text-sm text-(--danger-ink)">Couldn&apos;t load experiments.</p>
      ) : null}

      {!experimentsQuery.isLoading && experiments.length === 0 ? (
        <div className="rounded-2xl border border-dashed border-(--line) bg-(--surface) p-8 text-center">
          <h2 className="text-lg font-semibold text-(--ink)">No experiments yet.</h2>
          <p className="mt-2 text-sm text-(--muted)">
            Create one from an approved baseline, then return to walk its story.
          </p>
          <Link
            className="mt-3 inline-block text-sm font-semibold text-(--accent-deep) hover:underline"
            href="/research/experiments/new"
          >
            New experiment →
          </Link>
        </div>
      ) : null}

      {groups.map((group) => (
        <Card key={group.key} padding="lg" className="space-y-3">
          <div>
            <h2 className="text-lg font-semibold text-(--ink)">{group.label}</h2>
            {group.subtitle ? (
              <p className="text-xs text-(--muted)">{group.subtitle}</p>
            ) : null}
          </div>
          <ul className="divide-y divide-(--line)">
            {group.experiments.map((experiment) => (
              <li
                key={experiment.experiment_id}
                className="flex flex-wrap items-center justify-between gap-3 py-3"
              >
                <div className="min-w-0">
                  <p className="truncate text-sm font-medium text-(--ink)">
                    {experiment.lesson_title ?? experiment.experiment_code}
                  </p>
                  <p className="text-xs text-(--muted)">{experiment.experiment_code}</p>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant={statusVariant(experiment.status)}>{experiment.status}</Badge>
                  <Link href={`/research/experiments/${experiment.experiment_id}/story`}>
                    <Button size="sm">Open story →</Button>
                  </Link>
                </div>
              </li>
            ))}
          </ul>
        </Card>
      ))}
    </div>
  );
}
