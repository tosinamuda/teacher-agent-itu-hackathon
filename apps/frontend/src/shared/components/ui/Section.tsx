import type { ReactNode } from "react";

/**
 * A titled block of a page: a quiet heading, an optional muted aside on the right, and its
 * content. Sections are set apart by space, not boxes.
 */
export function Section({
  title,
  aside,
  children,
}: {
  title: ReactNode;
  aside?: ReactNode;
  children: ReactNode;
}) {
  return (
    <section className="space-y-3">
      <header className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1">
        <h2 className="text-base font-semibold text-(--ink)">{title}</h2>
        {aside ? <div className="text-sm text-(--muted)">{aside}</div> : null}
      </header>
      {children}
    </section>
  );
}
