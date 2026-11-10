import type { AssignedRater } from "../types";

/** A quiet block of the live assignment page, set apart by space rather than a box. */
export const SECTION_CLASS = "space-y-3";
const PILL_CLASS =
  "inline-flex items-center gap-1 border border-(--line-2) bg-(--bg) px-2 py-0.5 text-xs text-(--ink-2)";

export function RaterChips({ raters }: { raters: AssignedRater[] }) {
  if (raters.length === 0) {
    return <p className="text-xs italic text-(--muted)">No raters yet.</p>;
  }
  return (
    <ul className="flex flex-wrap gap-1.5">
      {raters.map((rater) => (
        <li key={rater.assignment_id} className={PILL_CLASS}>
          <span className="font-medium text-(--ink)">{rater.display_name}</span>
          {rater.is_adjudicator ? (
            <span className="text-[10px] uppercase tracking-wide text-(--accent)">
              · adjudicator
            </span>
          ) : null}
        </li>
      ))}
    </ul>
  );
}
