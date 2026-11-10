import { Link } from "@/shared/router";

import { LINK, ROW_HEAD, TABLE, TD, TH } from "@/shared/components/ui/table";
import type { StudyRatingsTally } from "@/features/study-ratings/types";

import { InvestigationExperimentRow } from "../lib/experiments";

const placeOf = (experiment: InvestigationExperimentRow) =>
  [experiment.school_name, experiment.subject_name].filter(Boolean).join(" · ") || "—";

/**
 * A study's topics, one row per lesson, linked to the lesson's experiment. A column every row
 * shares says nothing and is left out: the school and subject when there is one, the status
 * when every run succeeded. With the study's tallies, each row counts its ratings too.
 */
export function InvestigationExperimentsTable({
  experiments,
  tallies = [],
}: {
  experiments: InvestigationExperimentRow[];
  tallies?: StudyRatingsTally[];
}) {
  if (experiments.length === 0) {
    return <p className="text-sm text-(--muted)">No experiments yet.</p>;
  }
  const rows = [...experiments].sort((a, b) => a.experiment_code.localeCompare(b.experiment_code));
  const showPlace = new Set(rows.map(placeOf)).size > 1;
  const showStatus = rows.some((row) => row.status !== "succeeded");
  const tally = new Map(tallies.map((each) => [each.plan_version_id, each]));
  const showRatings = tallies.length > 0;

  return (
    <div className="overflow-x-auto">
      <table className={TABLE}>
        <thead>
          <tr>
            <th className={TH}>Topic</th>
            {showPlace ? <th className={TH}>School · subject</th> : null}
            {showStatus ? <th className={TH}>Status</th> : null}
            {showRatings ? (
              <>
                <th className={TH}>Scores</th>
                <th className={TH}>Comparisons</th>
                <th className={TH}>Raters</th>
              </>
            ) : null}
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => {
            const counts = row.plan_version_id ? tally.get(row.plan_version_id) : undefined;
            return (
              <tr key={row.experiment_id}>
                <td className={ROW_HEAD}>
                  <Link href={`/research/experiments/${row.experiment_id}`} className={LINK}>
                    {row.lesson_title ?? row.experiment_code}
                  </Link>
                  {row.is_sandbox ? (
                    <span className="ml-2 text-xs font-normal text-(--muted)">sandbox</span>
                  ) : null}
                </td>
                {showPlace ? <td className={`${TD} text-(--ink-2)`}>{placeOf(row)}</td> : null}
                {showStatus ? <td className={`${TD} text-(--ink-2)`}>{row.status}</td> : null}
                {showRatings ? (
                  <>
                    <td className={TD}>{counts?.scores ?? 0}</td>
                    <td className={TD}>{counts?.judgements ?? 0}</td>
                    <td className={TD}>{counts?.raters ?? 0}</td>
                  </>
                ) : null}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
