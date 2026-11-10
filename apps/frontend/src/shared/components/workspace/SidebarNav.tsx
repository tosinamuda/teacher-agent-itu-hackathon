import { Link } from "@/shared/router";

export type SidebarItem = {
  label: string;
  /** Present for a page link. Absent for an item that acts (switching class). */
  href?: string;
  onSelect?: () => void;
  active?: boolean;
  /** Shown but not openable yet. */
  disabled?: boolean;
  /** A small trailing count. */
  count?: number;
  /** Marks that something waits for the teacher behind this row. */
  waiting?: boolean;
  /** Marks that the agent is writing what this row opens. */
  working?: boolean;
};

export type SidebarGroup = { heading?: string; items: SidebarItem[] };

const ROW =
  "flex w-full items-center justify-between gap-3 border-l-2 px-4 py-2 text-left text-sm";

function Row({ item }: { item: SidebarItem }) {
  const tone = item.active
    ? "border-(--ink) font-semibold text-(--ink)"
    : item.disabled
      ? "border-transparent text-(--faint)"
      : "border-transparent text-(--ink-2) hover:text-(--ink)";
  const trailing =
    item.count || item.waiting || item.working ? (
      <span className="flex items-center gap-2 text-xs text-(--faint)">
        {item.waiting ? (
          <span
            aria-hidden="true"
            className="size-2 rounded-full bg-(--accent)"
          />
        ) : null}
        {item.count ? item.count : null}
      </span>
    ) : null;

  if (item.disabled) {
    return (
      <span aria-disabled="true" className={`${ROW} ${tone}`}>
        {item.label}
        {trailing}
      </span>
    );
  }
  if (item.href) {
    return (
      <Link
        href={item.href}
        aria-current={item.active ? "page" : undefined}
        className={`${ROW} ${tone}`}
      >
        {item.label}
        {trailing}
      </Link>
    );
  }
  return (
    <button type="button" onClick={item.onSelect} className={`${ROW} ${tone}`}>
      {item.label}
      {trailing}
    </button>
  );
}

/** The sidebar's navigation: groups of rows, no status marks, one selected row. */
export function SidebarNav({
  groups,
  label,
}: {
  groups: SidebarGroup[];
  label: string;
}) {
  return (
    <nav aria-label={label} className="flex flex-col gap-4">
      {groups.map((group, index) => (
        <div key={group.heading ?? index} className="flex flex-col">
          {group.heading ? (
            <p className="px-4 pb-1 pt-2 text-[11px] font-semibold uppercase tracking-[0.12em] text-(--faint)">
              {group.heading}
            </p>
          ) : null}
          {group.items.map((item) => (
            <Row key={item.label} item={item} />
          ))}
        </div>
      ))}
    </nav>
  );
}
