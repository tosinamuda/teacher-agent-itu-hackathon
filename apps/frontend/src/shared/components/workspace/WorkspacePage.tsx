import { createContext, useContext, type ReactNode } from "react";
import { createPortal } from "react-dom";

/**
 * Where a page's right panel goes. A frame that keeps its own panel column provides it: `null`
 * until the column exists, then the column itself, so moving between pages swaps what is in the
 * column and leaves the column where it is. Outside such a frame it is `undefined`, and the page
 * carries its own column.
 */
export const PanelSlotContext = createContext<HTMLElement | null | undefined>(
  undefined,
);

export const PANEL_COLUMN_CLASS =
  "relative w-full shrink-0 border-t border-(--line) bg-(--surface) lg:w-(--panel-width,360px) lg:overflow-y-auto lg:border-l lg:border-t-0";

/** A page inside the teacher shell: the page on the left, the right panel beside it. */
export function WorkspacePage({
  children,
  panel,
}: {
  children: ReactNode;
  panel: ReactNode;
}) {
  const slot = useContext(PanelSlotContext);
  const page = (
    <main className="relative min-w-0 flex-1 overflow-y-auto px-8 py-6">
      {children}
    </main>
  );

  if (slot === undefined) {
    return (
      <div className="flex min-h-0 flex-1 flex-col lg:flex-row">
        {page}
        <aside aria-label="Needs you and agent" className={PANEL_COLUMN_CLASS}>
          {panel}
        </aside>
      </div>
    );
  }
  return (
    <>
      {page}
      {slot ? createPortal(panel, slot) : null}
    </>
  );
}
