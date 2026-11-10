import { Link } from "@/shared/router";

export type TabItem = {
  href: string;
  label: string;
  active: boolean;
  /** Shown on hover. */
  hint?: string;
  /** A little more space before this tab, where one group of tabs gives way to the next. */
  gapBefore?: boolean;
};

/** A page's tabs: one line, the current tab underlined, scrolling sideways when narrow. */
export function TabBar({ tabs, label }: { tabs: TabItem[]; label: string }) {
  return (
    <nav className="-mx-1 overflow-x-auto border-b border-(--line)" aria-label={label}>
      <div className="flex min-w-max px-1">
        {tabs.map((tab) => (
          <Link
            key={tab.href}
            href={tab.href}
            title={tab.hint}
            aria-current={tab.active ? "page" : undefined}
            className={`-mb-px whitespace-nowrap border-b-2 px-3 py-2.5 text-sm font-medium transition ${
              tab.gapBefore ? "ml-4" : ""
            } ${
              tab.active
                ? "border-(--accent) text-(--ink)"
                : "border-transparent text-(--muted) hover:text-(--ink)"
            }`}
          >
            {tab.label}
          </Link>
        ))}
      </div>
    </nav>
  );
}
