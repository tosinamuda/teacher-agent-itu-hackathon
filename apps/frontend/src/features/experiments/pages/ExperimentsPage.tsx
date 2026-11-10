import { Link } from "@/shared/router";
import { useMemo, useState } from "react";

import { Modal } from "@/shared/components/ui/Modal";

import { ExperimentFilterBar } from "../components/ExperimentFilterBar";
import { ExperimentTable } from "../components/ExperimentTable";
import { useExperiments, useExperimentWorkspaces } from "../hooks/useExperiments";
import { ExperimentFilters, Hypothesis } from "../lib/experiments";

type ExperimentsPageProps = {
  title?: string;
  hypothesis?: Hypothesis;
  actionPathPrefix?: string;
};

/** Renders the researcher experiment list with label-driven filters. */
export function ExperimentsPage({
  title = "Experiments",
  hypothesis,
  actionPathPrefix,
}: ExperimentsPageProps) {
  const initialFilters = useMemo<ExperimentFilters>(
    () => ({
      schoolId: "",
      teacherWorkspaceId: "",
      experimentCode: "",
      query: "",
      hypothesis: hypothesis ?? "",
      status: "",
    }),
    [hypothesis],
  );
  const [filters, setFilters] = useState<ExperimentFilters>(initialFilters);
  const [filtersOpen, setFiltersOpen] = useState(false);
  const experimentsQuery = useExperiments(filters);
  const workspacesQuery = useExperimentWorkspaces();

  const experiments = useMemo(() => experimentsQuery.data ?? [], [experimentsQuery.data]);
  const workspaces = useMemo(() => workspacesQuery.data ?? [], [workspacesQuery.data]);
  // Count active filters (other than the quick search + the lane's locked hypothesis).
  const activeFilterCount = [
    filters.schoolId,
    filters.teacherWorkspaceId,
    filters.experimentCode,
    filters.status,
    hypothesis ? "" : filters.hypothesis,
  ].filter(Boolean).length;

  return (
    <main className="flex w-full flex-col gap-6 py-8">
      <h1 className="text-2xl font-semibold text-(--ink)">
        {hypothesis ? `${title} · ${hypothesis}` : title}
      </h1>

      <div className="space-y-4">
        <div className="flex flex-wrap items-center gap-2">
          <input
            value={filters.query ?? ""}
            onChange={(event) => setFilters({ ...filters, query: event.target.value })}
            placeholder="Search lesson, school, teacher…"
            className="h-9 min-w-[12rem] flex-1 border border-(--line-2) bg-(--surface) px-3 text-sm text-(--ink) outline-none focus:border-(--ink)"
          />
          <button
            type="button"
            onClick={() => setFiltersOpen(true)}
            className="text-sm text-(--muted) hover:text-(--ink)"
          >
            Filters{activeFilterCount ? ` (${activeFilterCount})` : ""}
          </button>
          <span className="ml-auto text-sm text-[color:var(--muted)]">
            {experiments.length} {experiments.length === 1 ? "result" : "results"}
          </span>
        </div>

        {experimentsQuery.isLoading && (
          <p className="text-sm text-[color:var(--muted)]">Loading experiments…</p>
        )}
        {experimentsQuery.isError && (
          <p className="text-sm text-(--danger-ink)">Failed to load experiments.</p>
        )}
        {!experimentsQuery.isLoading && experiments.length === 0 && (
          <p className="text-sm text-(--muted)">
            No experiments.{" "}
            <Link className="text-(--accent-deep) hover:underline" href="/research/experiments/new">
              New experiment
            </Link>
          </p>
        )}

        {experiments.length > 0 && (
          <ExperimentTable
            experiments={experiments}
            openHref={
              actionPathPrefix
                ? (experiment) => `${actionPathPrefix}/${experiment.experiment_id}`
                : undefined
            }
          />
        )}
      </div>

      <Modal
        isOpen={filtersOpen}
        onClose={() => setFiltersOpen(false)}
        title="Filter experiments"
        maxWidthClassName="max-w-2xl"
      >
        <div className="p-4">
          <ExperimentFilterBar
            filters={filters}
            onChange={setFilters}
            lockedHypothesis={hypothesis}
            onReset={() => setFilters(initialFilters)}
            workspaces={workspaces}
          />
        </div>
      </Modal>
    </main>
  );
}
