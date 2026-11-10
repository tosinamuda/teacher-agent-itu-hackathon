import { useEffect, useRef, useState } from "react";

export type PlanMenuItem = { label: string; onSelect: () => void };

/** The "···" button beside a plan's title: the things that change the plan itself. */
export function PlanMenu({ items }: { items: PlanMenuItem[] }) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    const away = (event: MouseEvent) => {
      if (ref.current && !ref.current.contains(event.target as Node))
        setOpen(false);
    };
    const escape = (event: KeyboardEvent) => {
      if (event.key === "Escape") setOpen(false);
    };
    document.addEventListener("mousedown", away);
    document.addEventListener("keydown", escape);
    return () => {
      document.removeEventListener("mousedown", away);
      document.removeEventListener("keydown", escape);
    };
  }, [open]);

  if (items.length === 0) return null;
  return (
    <div ref={ref} className="relative">
      <button
        type="button"
        aria-label="More"
        aria-haspopup="menu"
        aria-expanded={open}
        onClick={() => setOpen((value) => !value)}
        className="flex size-8 items-center justify-center border border-(--line-2) bg-(--surface) text-(--ink-2) hover:text-(--ink)"
      >
        ···
      </button>
      {open ? (
        <div
          role="menu"
          className="absolute right-0 top-[calc(100%+4px)] z-20 w-56 border border-(--line) bg-(--surface)"
        >
          {items.map((item) => (
            <button
              key={item.label}
              type="button"
              role="menuitem"
              onClick={() => {
                setOpen(false);
                item.onSelect();
              }}
              className="block w-full px-4 py-2.5 text-left text-sm text-(--ink) hover:bg-(--sunken)"
            >
              {item.label}
            </button>
          ))}
        </div>
      ) : null}
    </div>
  );
}
