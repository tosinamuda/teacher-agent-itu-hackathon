import { Link } from "@/shared/router";
import { useMemo } from "react";

import type { ResearchSchool } from "../types";

type SchoolDirectoryTableProps = {
  schools: ResearchSchool[];
  /** Id of a just-created school (from `?created=`) to highlight + float to the top. */
  highlightId?: string | null;
};

/** Sort newest-first when `created_at` is present, otherwise keep API order. A just-
 *  created school is forced to the top so the highlight is always visible. */
function sortSchools(schools: ResearchSchool[], highlightId?: string | null): ResearchSchool[] {
  return [...schools].sort((a, b) => {
    if (highlightId) {
      if (a.id === highlightId) return -1;
      if (b.id === highlightId) return 1;
    }
    if (a.created_at && b.created_at) return b.created_at.localeCompare(a.created_at);
    return 0;
  });
}

/** The research school directory as a table — name + code, term/year, counts, and a
 *  link into each school's setup. */
export function SchoolDirectoryTable({ schools, highlightId }: SchoolDirectoryTableProps) {
  const rows = useMemo(() => sortSchools(schools, highlightId), [schools, highlightId]);

  return (
    <div className="overflow-x-auto rounded-2xl border border-(--line) bg-(--surface)">
      <table className="w-full text-left text-sm">
        <thead className="border-b border-(--line) text-xs uppercase tracking-[0.12em] text-(--muted)">
          <tr>
            <th className="px-4 py-3 font-semibold">School</th>
            <th className="px-4 py-3 font-semibold">Term · Year</th>
            <th className="px-4 py-3 font-semibold">Classes</th>
            <th className="px-4 py-3 font-semibold">Workspaces</th>
            <th className="px-4 py-3" />
          </tr>
        </thead>
        <tbody>
          {rows.map((school) => (
            <tr
              key={school.id}
              className={`border-b border-(--line) last:border-0 transition hover:bg-[color:var(--accent-soft)] ${
                school.id === highlightId ? "animate-highlight" : ""
              }`}
            >
              <td className="px-4 py-3">
                <Link href={`/research/setup/${school.id}/details`} className="block">
                  <span className="font-semibold text-(--ink)">{school.name}</span>{" "}
                  <span className="text-(--muted)">({school.school_code})</span>
                </Link>
              </td>
              <td className="px-4 py-3 text-(--muted)">
                {school.current_term ?? "—"} · {school.default_academic_year ?? "—"}
              </td>
              <td className="px-4 py-3 text-(--muted)">{school.class_count}</td>
              <td className="px-4 py-3 text-(--muted)">{school.workspace_count}</td>
              <td className="px-4 py-3 text-right">
                <Link
                  href={`/research/setup/${school.id}/details`}
                  className="text-sm font-semibold text-(--accent-deep) hover:underline"
                >
                  Open →
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
