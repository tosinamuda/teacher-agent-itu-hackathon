import type { ReactNode } from "react";

/**
 * The app frame for a workspace: a slim top bar, a sidebar of navigation, and the
 * page. The page scrolls on its own so the bar and sidebar stay where they are.
 */
export function WorkspaceShell({
  top,
  sidebar,
  sidebarFooter,
  children,
}: {
  top: ReactNode;
  sidebar?: ReactNode;
  /** Stays at the foot of the sidebar however long the navigation is. */
  sidebarFooter?: ReactNode;
  children: ReactNode;
}) {
  return (
    <div className="relative flex h-screen flex-col overflow-hidden bg-(--bg)">
      <header className="flex h-12 shrink-0 items-center gap-4 border-b border-(--line) bg-(--surface) px-4">
        {top}
      </header>
      <div className="flex min-h-0 flex-1 flex-col md:flex-row">
        {sidebar ? (
          <aside className="flex w-full shrink-0 flex-col border-b border-(--line) bg-(--sunken) md:w-[220px] md:border-b-0 md:border-r">
            <div className="relative min-h-0 flex-1 overflow-y-auto py-3">
              {sidebar}
            </div>
            {sidebarFooter ? (
              <div className="shrink-0 border-t border-(--line)">
                {sidebarFooter}
              </div>
            ) : null}
          </aside>
        ) : null}
        <div className="relative flex min-h-0 min-w-0 flex-1 flex-col overflow-y-auto">
          {children}
        </div>
      </div>
    </div>
  );
}
