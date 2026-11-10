import { Link } from "@/shared/router";

import { InvestigationResultsRollup as Rollup } from "../lib/experiments";

const fmt = (value: number | null) => (value === null ? "—" : value.toFixed(2));

function Stat({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="rounded-2xl border border-(--line) bg-white p-4">
      <p className="text-xs font-semibold uppercase tracking-wide text-(--muted)">{label}</p>
      <p className="mt-1 text-2xl font-semibold text-(--ink)">{value}</p>
    </div>
  );
}

/** Rolled-up rater results across an investigation's experiments. */
export function InvestigationResultsRollup({
  rollup,
  isLoading,
}: {
  rollup: Rollup | undefined;
  isLoading: boolean;
}) {
  if (isLoading) {
    return <p className="text-sm text-(--muted)">Loading results…</p>;
  }
  if (!rollup || rollup.experiment_count === 0) {
    return (
      <p className="rounded-2xl border border-dashed border-(--line) bg-(--surface) p-6 text-center text-sm text-(--muted)">
        No experiments with results yet — create experiments for the scoped lessons.
      </p>
    );
  }

  return (
    <div className="space-y-4">
      <div className="grid gap-3 sm:grid-cols-4">
        <Stat label="Experiments" value={rollup.experiment_count} />
        <Stat label="Packets rated" value={`${rollup.rated_packet_count}/${rollup.packet_count}`} />
        <Stat label="Ratings" value={`${rollup.total_ratings} · ${rollup.distinct_raters}r`} />
        <Stat label="Mean overall" value={fmt(rollup.mean_overall)} />
      </div>

      <div className="overflow-x-auto">
        <table className="w-full border-separate border-spacing-y-2 text-left text-sm">
          <thead className="text-(--muted)">
            <tr>
              <th className="px-3">Experiment</th>
              <th className="px-3">Packets rated</th>
              <th className="px-3">Ratings</th>
              <th className="px-3">Mean</th>
            </tr>
          </thead>
          <tbody>
            {rollup.per_experiment.map((row) => (
              <tr key={row.experiment_id} className="rounded-2xl bg-(--surface)">
                <td className="px-3 py-2">
                  <Link
                    className="text-(--accent-deep) hover:underline"
                    href={`/research/experiments/${row.experiment_id}/results`}
                  >
                    {row.experiment_id.slice(0, 16)}…
                  </Link>
                </td>
                <td className="px-3 py-2 text-(--muted)">
                  {row.rated_packet_count}/{row.packet_count}
                </td>
                <td className="px-3 py-2 text-(--muted)">{row.total_ratings}</td>
                <td className="px-3 py-2 font-semibold text-(--ink)">{fmt(row.mean_overall)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
