import { ReactNode, useEffect } from "react";
import { createPortal } from "react-dom";

type DrawerProps = {
  open: boolean;
  onClose: () => void;
  title?: string;
  side?: "left" | "right";
  /** The panel's width as Tailwind classes. */
  width?: string;
  children: ReactNode;
};

/**
 * A slide-over panel: a dimmed backdrop plus a flat, squared panel that slides in from
 * the edge. Used for on-demand surfaces (e.g. the syllabus map) that should open on
 * click rather than occupy a permanent sidebar. Closes on Escape or backdrop click.
 *
 * It is drawn into the page body: a card that animates carries a transform, and a fixed panel
 * inside one is placed against the card, not the window.
 */
export function Drawer({
  open,
  onClose,
  title,
  side = "left",
  width = "w-[360px] max-w-[88vw]",
  children,
}: DrawerProps) {
  useEffect(() => {
    const onEsc = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    if (open) window.addEventListener("keydown", onEsc);
    return () => window.removeEventListener("keydown", onEsc);
  }, [open, onClose]);

  return createPortal(
    <div
      className={`fixed inset-0 z-50 ${open ? "" : "pointer-events-none"}`}
      aria-hidden={!open}
    >
      <div
        className={`absolute inset-0 bg-(--ink)/30 transition-opacity duration-200 ${
          open ? "opacity-100" : "opacity-0"
        }`}
        onClick={onClose}
      />
      <div
        className={`absolute inset-y-0 flex ${width} flex-col bg-(--surface) transition-transform duration-200 ${
          side === "left" ? "left-0 border-r" : "right-0 border-l"
        } border-(--line) ${
          open ? "translate-x-0" : side === "left" ? "-translate-x-full" : "translate-x-full"
        }`}
      >
        <div className="flex items-center justify-between border-b border-(--line) px-5 py-4">
          <h2 className="text-xs font-semibold uppercase tracking-[0.16em] text-(--faint)">
            {title}
          </h2>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close"
            className="text-(--ink-2) transition-colors hover:text-(--ink)"
          >
            ✕
          </button>
        </div>
        <div className="flex-1 overflow-y-auto px-5 py-4">{children}</div>
      </div>
    </div>,
    document.body,
  );
}
