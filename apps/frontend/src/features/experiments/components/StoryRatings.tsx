import { ExperimentRatingsSummary } from "../lib/experiments";

/**
 * The Story's ratings step: the *expert* (reported) mean and per-hypothesis breakdown,
 * with synthetic dry-run scores shown only as a small labelled proxy footnote — never
 * folded into the headline number.
 */
export function StoryRatings({ ratings }: { ratings: ExperimentRatingsSummary | undefined }) {
  if (!ratings) {
    return <p className="text-sm italic text-(--muted)">No ratings yet.</p>;
  }
  const hasExpert = ratings.total_ratings > 0;
  return (
    <div className="space-y-2">
      {hasExpert ? (
        <div className="flex flex-wrap gap-4 text-sm">
          <span>
            Expert mean:{" "}
            <span className="font-semibold text-(--ink)">{ratings.mean_overall ?? "—"}</span>
          </span>
          {Object.entries(ratings.by_hypothesis).map(([hyp, summary]) => (
            <span key={hyp} className="text-(--muted)">
              {hyp}: {summary.mean_overall ?? "—"} ({summary.rating_count})
            </span>
          ))}
        </div>
      ) : (
        <p className="text-sm text-(--muted)">Not yet evaluated by expert raters.</p>
      )}
      {ratings.synthetic ? (
        <p className="text-xs italic text-(--muted)">
          ⟳ synthetic proxy: {ratings.synthetic.mean_overall ?? "—"} (N=
          {ratings.synthetic.rating_count}) — a dry run, excluded from reported results.
        </p>
      ) : null}
    </div>
  );
}
