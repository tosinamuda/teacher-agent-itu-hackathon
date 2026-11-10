import { Link } from "@/shared/router";

import { LINK, ROW_HEAD, TABLE, TD, TH } from "@/shared/components/ui/table";

import { ExperimentSummary, experimentTitle } from "../lib/experiments";

type ExperimentTableProps = {
  experiments: ExperimentSummary[];
  openHref?: (experiment: ExperimentSummary) => string;
};

// Provenance of an experiment's ratings: synthetic = dry-run proxy only (not really
// evaluated); live = scored by expert raters; mixed = both (expert numbers reported).
const MODE_LABEL: Record<string, string> = {
  synthetic: "Rehearsed",
  live: "Evaluated",
  mixed: "Evaluated, with proxy",
};

const join = (parts: (string | null | undefined)[]) =>
  parts.map((p) => p?.trim()).filter(Boolean).join(" · ") || "—";

/** Where an experiment stands: ended, or its run status and which hypotheses can run. */
function stateOf(experiment: ExperimentSummary): string {
  if (experiment.lifecycle_status === "ended") return "Ended";
  const ready = [
    experiment.readiness.h1_ready ? "H1 ready" : null,
    experiment.readiness.h2_ready ? "H2 ready" : null,
  ];
  return join([experiment.status ?? "created", ...ready]);
}

/** Every experiment, one row each, its lesson linking to it. */
export function ExperimentTable({ experiments, openHref }: ExperimentTableProps) {
  return (
    <div className="overflow-x-auto">
      <table className={TABLE}>
        <thead>
          <tr>
            <th className={TH}>Topic</th>
            <th className={TH}>Where</th>
            <th className={TH}>State</th>
          </tr>
        </thead>
        <tbody>
          {experiments.map((experiment) => (
            <tr key={experiment.experiment_id}>
              <td className={`${ROW_HEAD} max-w-md`}>
                <Link
                  className={LINK}
                  href={
                    openHref
                      ? openHref(experiment)
                      : `/research/experiments/${experiment.experiment_id}`
                  }
                >
                  {experimentTitle(experiment)}
                </Link>
                <p className="font-mono text-xs font-normal text-(--muted)">
                  {experiment.experiment_code}
                  {experiment.evaluation_mode && MODE_LABEL[experiment.evaluation_mode]
                    ? ` · ${MODE_LABEL[experiment.evaluation_mode]}`
                    : ""}
                </p>
              </td>
              <td className={`${TD} text-(--ink-2)`}>
                {experiment.school_name ?? "—"}
                <p className="text-xs text-(--muted)">
                  {join([experiment.grade_level, experiment.subject_name, experiment.term])}
                </p>
              </td>
              <td className={`${TD} text-(--ink-2)`}>{stateOf(experiment)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
