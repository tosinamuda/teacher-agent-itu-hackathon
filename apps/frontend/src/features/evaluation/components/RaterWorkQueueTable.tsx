import { Link } from "@/shared/router";

/**
 * One row of the rater's unified work queue. `type` is a plain-language task
 * label ("Revision note review", "Learner comparison", "Source check") — never a
 * hypothesis id or condition code, which would unblind the study design.
 */
export type RaterWorkItem = {
  id: string;
  /** Primary label shown to the rater (packet code or item description). */
  code: string;
  type: string;
  done: boolean;
  href: string;
};

const StatusChip = ({ done }: { done: boolean }) => (
  <span
    className={`rounded-none px-2.5 py-1 text-xs font-semibold ${
      done
        ? "bg-[color:var(--accent-soft)] text-[color:var(--accent-deep)]"
        : "bg-white text-[color:var(--muted)]"
    }`}
  >
    {done ? "Completed" : "To rate"}
  </span>
);

/**
 * Renders the rater's full queue as ONE flat table across every task type, items
 * still to rate first. Each row opens its item directly.
 */
export function RaterWorkQueueTable({ items }: { items: RaterWorkItem[] }) {
  if (items.length === 0) {
    return (
      <p className="text-sm text-[color:var(--muted)]">
        Nothing is ready for review yet. Items appear here once a researcher assigns
        work to you.
      </p>
    );
  }

  const ordered = [...items.filter((item) => !item.done), ...items.filter((item) => item.done)];

  return (
    <div className="overflow-x-auto">
      <table className="w-full border-separate border-spacing-y-2 text-left text-sm">
        <thead>
          <tr className="text-xs font-semibold uppercase tracking-[0.14em] text-[color:var(--muted)]">
            <th className="px-3 py-1">Item</th>
            <th className="px-3 py-1">Type</th>
            <th className="px-3 py-1">Status</th>
            <th className="px-3 py-1 text-right">Action</th>
          </tr>
        </thead>
        <tbody>
          {ordered.map((item) => (
            <tr key={`${item.type}-${item.id}`} className="rounded-2xl bg-(--surface)">
              <td className="max-w-[22rem] truncate px-3 py-3 font-semibold text-[color:var(--ink)]">
                {item.code}
              </td>
              <td className="px-3 py-3 text-[color:var(--muted)]">{item.type}</td>
              <td className="px-3 py-3">
                <StatusChip done={item.done} />
              </td>
              <td className="px-3 py-3 text-right">
                <Link
                  className="text-sm font-semibold text-[color:var(--accent-deep)] hover:underline"
                  href={item.href}
                >
                  {item.done ? "Review" : "Open"}
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
