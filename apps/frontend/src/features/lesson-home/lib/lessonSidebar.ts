import type {
  SidebarGroup,
  SidebarItem,
} from "@/shared/components/workspace/SidebarNav";

import type { HomeRow } from "./lessonHome";

const pathOf = (href: string): string => href.split("?")[0];

/**
 * A lesson's sidebar: the same list in every state. A locked line is shown dimmed and cannot be
 * opened; a material not made yet leads to the lesson, where it is made, and is never the selected line.
 */
export function lessonSidebarGroups(
  lessonHome: string,
  rows: { plan: HomeRow; materials: HomeRow[]; learners: HomeRow[] },
  pathname: string,
  working: ReadonlySet<string> = new Set(),
): SidebarGroup[] {
  const item = (row: HomeRow, opensPlan = false): SidebarItem => {
    if (row.status === "locked") return { label: row.title, disabled: true };
    const href = row.href ?? row.action?.href ?? lessonHome;
    const here =
      pathOf(href) === pathname ||
      (opensPlan && pathname.startsWith("/research/teacher/lesson-plan/"));
    return {
      label: row.title,
      href,
      active: pathOf(href) !== lessonHome && here,
      working: working.has(row.key),
    };
  };
  return [
    {
      items: [
        {
          label: "Overview",
          href: lessonHome,
          active: pathname === lessonHome,
        },
        item(rows.plan, true),
      ],
    },
    { heading: "Materials", items: rows.materials.map((row) => item(row)) },
    { items: rows.learners.map((row) => item(row)) },
  ];
}
