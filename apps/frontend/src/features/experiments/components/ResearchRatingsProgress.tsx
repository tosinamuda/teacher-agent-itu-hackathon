import { ExperimentRatingsSummary } from "../lib/experiments";

const fmt = (value: number | null) => (value === null ? "—" : value.toFixed(2));

/**
 * Rater-rating progress for a study: how many packets have been rated, by how many
 * raters, and the mean overall scores (overall + per hypothesis) — the results that
 * trickle in as raters work through the blinded queue.
 */
export function ResearchRatingsProgress({
  ratings,
  isLoading,
}: {
  ratings: ExperimentRatingsSummary | undefined;
  isLoading: boolean;
}) {
  if (isLoading) {
    return <p className="text-sm text-(--muted)">Loading ratings…</p>;
  }
  if (!ratings) {
    return <p className="text-sm text-(--muted)">No ratings available.</p>;
  }

  const pct =
    ratings.packet_count > 0
      ? Math.round((ratings.rated_packet_count / ratings.packet_count) * 100)
      : 0;

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        <div className="h-2 flex-1 overflow-hidden rounded-none bg-(--line)/40">
          <div className="h-full rounded-none bg-(--accent)" style={{ width: `${pct}%` }} />
        </div>
        <span className="text-xs font-medium text-(--muted)">
          {ratings.rated_packet_count}/{ratings.packet_count} packets rated
        </span>
      </div>

      <div className="grid gap-3 sm:grid-cols-3">
        <div className="rounded-2xl border border-(--line) bg-white p-4">
          <p className="text-xs font-semibold uppercase tracking-wide text-(--muted)">Ratings</p>
          <p className="mt-1 text-2xl font-semibold text-(--ink)">{ratings.total_ratings}</p>
          <p className="text-xs text-(--muted)">{ratings.distinct_raters} rater(s)</p>
        </div>
        <div className="rounded-2xl border border-(--line) bg-white p-4">
          <p className="text-xs font-semibold uppercase tracking-wide text-(--muted)">Mean overall</p>
          <p className="mt-1 text-2xl font-semibold text-(--ink)">{fmt(ratings.mean_overall)}</p>
        </div>
        <div className="rounded-2xl border border-(--line) bg-white p-4">
          <p className="text-xs font-semibold uppercase tracking-wide text-(--muted)">By hypothesis</p>
          <ul className="mt-1 space-y-0.5 text-sm text-(--ink)">
            {Object.entries(ratings.by_hypothesis).map(([hyp, summary]) => (
              <li key={hyp}>
                {hyp}: {fmt(summary.mean_overall)}{" "}
                <span className="text-xs text-(--muted)">({summary.rating_count} ratings)</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
