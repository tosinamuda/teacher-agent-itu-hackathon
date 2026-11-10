import { ReactNode, useState } from "react";

import { Button } from "@/shared/components/ui/Button";

/**
 * One part at a time: a "Section X of Y" line with Previous and Next above the part, so the
 * controls stay in reach however long the part is. With one part there are no controls. The page
 * can keep the index (`index`, `onIndexChange`); otherwise the pager keeps its own.
 *
 * In a column that has a fixed height the part fills what is left, so it can scroll in its card.
 */
export function Pager({
  count,
  label = "Section",
  heading,
  index: controlled,
  onIndexChange,
  children,
}: {
  count: number;
  label?: string;
  /** Replaces "Section X of Y" for the part shown. */
  heading?: (index: number) => string;
  index?: number;
  onIndexChange?: (index: number) => void;
  children: (index: number) => ReactNode;
}) {
  const [kept, setKept] = useState(0);
  if (count === 0) return null;
  const index = Math.max(0, Math.min(controlled ?? kept, count - 1));
  const go = (next: number) => {
    setKept(next);
    onIndexChange?.(next);
  };
  return (
    <div className="flex min-h-0 flex-1 flex-col gap-3">
      {count > 1 ? (
        <div className="flex shrink-0 items-center justify-between gap-3">
          <p className="text-xs font-semibold text-(--muted)">
            {heading ? heading(index) : `${label} ${index + 1} of ${count}`}
          </p>
          <div className="flex gap-2">
            <Button
              size="sm"
              variant="outline"
              onClick={() => go(Math.max(index - 1, 0))}
              disabled={index === 0}
            >
              Previous
            </Button>
            <Button
              size="sm"
              variant="primary"
              onClick={() => go(Math.min(index + 1, count - 1))}
              disabled={index === count - 1}
            >
              Next
            </Button>
          </div>
        </div>
      ) : null}
      <div className="flex min-h-0 flex-1 flex-col">{children(index)}</div>
    </div>
  );
}
