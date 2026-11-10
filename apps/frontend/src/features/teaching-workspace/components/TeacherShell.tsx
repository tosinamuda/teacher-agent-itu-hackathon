import { useState, type ReactNode } from "react";

import {
  PANEL_COLUMN_CLASS,
  PanelSlotContext,
} from "@/shared/components/workspace/WorkspacePage";
import { PanelResizer } from "@/shared/components/workspace/PanelResizer";
import { usePanelWidth } from "@/shared/components/workspace/panelWidth";
import { WorkspaceShell } from "@/shared/components/workspace/WorkspaceShell";
import { Link } from "@/shared/router";

import { TeacherCrumbs } from "./TeacherCrumbs";
import { TeacherSidebar } from "./TeacherSidebar";

/** The teacher's frame. The sidebar appears once someone is signed in. */
export function TeacherShell({
  signedIn,
  userMenu,
  fillsFrame,
  children,
}: {
  signedIn: boolean;
  /** The page carries its own padding and panel, so the frame adds none. */
  fillsFrame: boolean;
  userMenu: ReactNode;
  children: ReactNode;
}) {
  const [panelColumn, setPanelColumn] = useState<HTMLElement | null>(null);
  const [panelWidth, setPanelWidth] = usePanelWidth();
  return (
    <WorkspaceShell
      top={
        <>
          <Link
            href="/research"
            className="font-(family-name:--font-display) text-base font-semibold tracking-[-0.01em] text-(--ink) no-underline hover:opacity-80"
          >
            Plan-to-Tutor
          </Link>
          {signedIn ? <TeacherCrumbs /> : null}
        </>
      }
      sidebar={signedIn ? <TeacherSidebar /> : null}
      sidebarFooter={userMenu}
    >
      {fillsFrame ? (
        <PanelSlotContext.Provider value={panelColumn}>
          <div className="flex min-h-0 flex-1 flex-col lg:flex-row">
            <div className="flex min-h-0 min-w-0 flex-1 flex-col">
              {children}
            </div>
            <aside
              ref={setPanelColumn}
              aria-label="Needs you and agent"
              className={PANEL_COLUMN_CLASS}
              style={
                { "--panel-width": `${panelWidth}px` } as React.CSSProperties
              }
            >
              <PanelResizer width={panelWidth} onChange={setPanelWidth} />
            </aside>
          </div>
        </PanelSlotContext.Provider>
      ) : (
        <div className="mx-auto w-full max-w-[1200px] px-6 py-5">
          {children}
        </div>
      )}
    </WorkspaceShell>
  );
}
