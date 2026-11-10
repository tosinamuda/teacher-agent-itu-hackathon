import { Link } from "@/shared/router";

import { useLessonHome } from "../hooks/useLessonHome";
import type { HomeRow } from "../lib/lessonHome";

/** Where a made thing opens: its page, or the page its review button goes to. Nothing for one not made. */
const pageOf = (row: HomeRow): string | undefined =>
  row.status === "locked" || row.status === "notStarted" || row.create
    ? undefined
    : (row.href ?? row.action?.href);

/**
 * The conversations of a lesson: the plan's, then each material's. Each has its own chat on its
 * own page, so this lists them and goes to the one wanted.
 */
export function LessonConversations({
  lessonPeriodId,
}: {
  lessonPeriodId: string;
}) {
  const { rows } = useLessonHome(lessonPeriodId);
  const made = [rows.plan, ...rows.materials].filter((row) => pageOf(row));
  if (made.length === 0) return null;

  return (
    <section aria-label="Conversations" className="flex flex-col gap-2">
      <h3 className="text-[11px] font-semibold uppercase tracking-[0.12em] text-(--faint)">
        Conversations
      </h3>
      <ul className="flex flex-col border border-(--line)">
        {made.map((row) => (
          <li
            key={row.key}
            className="border-t border-(--line) first:border-t-0"
          >
            <Link
              href={pageOf(row) as string}
              className="flex items-center justify-between gap-3 px-3 py-2.5 text-sm hover:bg-(--sunken)"
            >
              <span className="font-semibold text-(--ink)">{row.title}</span>
              <span className="text-xs text-(--ink-2)">Open chat</span>
            </Link>
          </li>
        ))}
      </ul>
    </section>
  );
}
