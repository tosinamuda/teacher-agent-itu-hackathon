import { Button } from "@/shared/components/ui/Button";

import {
  EXPERIMENT_HYPOTHESES,
  ExperimentFilters,
  ExperimentWorkspaceOption,
  Hypothesis,
} from "../lib/experiments";

type ExperimentFilterBarProps = {
  filters: ExperimentFilters;
  onChange: (next: ExperimentFilters) => void;
  onReset: () => void;
  workspaces: ExperimentWorkspaceOption[];
  lockedHypothesis?: Hypothesis;
};

const fieldClass =
  "rounded-none border border-[color:var(--line)] bg-(--surface) px-4 py-2 text-sm text-[color:var(--ink)] outline-none transition focus:border-[color:var(--accent)]";

/** Renders the researcher-facing experiment filters with label-driven fields. */
export function ExperimentFilterBar({
  filters,
  onChange,
  onReset,
  workspaces,
  lockedHypothesis,
}: ExperimentFilterBarProps) {
  const schools = Array.from(
    new Map(
      workspaces.map((workspace) => [
        workspace.school_id,
        {
          id: workspace.school_id,
          label: `${workspace.school_name} (${workspace.school_code})`,
        },
      ])
    ).values()
  );
  const filteredWorkspaces = filters.schoolId
    ? workspaces.filter((workspace) => workspace.school_id === filters.schoolId)
    : workspaces;

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-end">
        <Button variant="ghost" size="sm" onClick={onReset}>
          Reset
        </Button>
      </div>
      <div className="grid gap-3 sm:grid-cols-2">
        <input
          className={fieldClass}
          placeholder="Experiment code"
          value={filters.experimentCode ?? ""}
          onChange={(event) =>
            onChange({ ...filters, experimentCode: event.target.value })
          }
        />
        <input
          className={fieldClass}
          placeholder="Search lesson, school, teacher"
          value={filters.query ?? ""}
          onChange={(event) => onChange({ ...filters, query: event.target.value })}
        />
        <select
          className={fieldClass}
          value={filters.schoolId ?? ""}
          onChange={(event) =>
            onChange({
              ...filters,
              schoolId: event.target.value,
              teacherWorkspaceId: "",
            })
          }
        >
          <option value="">All schools</option>
          {schools.map((school) => (
            <option key={school.id} value={school.id}>
              {school.label}
            </option>
          ))}
        </select>
        <select
          className={fieldClass}
          value={filters.teacherWorkspaceId ?? ""}
          onChange={(event) =>
            onChange({ ...filters, teacherWorkspaceId: event.target.value })
          }
        >
          <option value="">All workspaces</option>
          {filteredWorkspaces.map((workspace) => (
            <option
              key={workspace.teacher_workspace_id}
              value={workspace.teacher_workspace_id}
            >
              {workspace.workspace_name}
            </option>
          ))}
        </select>
        {!lockedHypothesis && (
          <select
            className={fieldClass}
            value={filters.hypothesis ?? ""}
            onChange={(event) =>
              onChange({
                ...filters,
                hypothesis: event.target.value as ExperimentFilters["hypothesis"],
              })
            }
          >
            <option value="">All hypotheses</option>
            {EXPERIMENT_HYPOTHESES.map((value) => (
              <option key={value} value={value}>
                {value}
              </option>
            ))}
          </select>
        )}
        <input
          className={fieldClass}
          placeholder="Status"
          value={filters.status ?? ""}
          onChange={(event) => onChange({ ...filters, status: event.target.value })}
        />
      </div>
    </div>
  );
}
