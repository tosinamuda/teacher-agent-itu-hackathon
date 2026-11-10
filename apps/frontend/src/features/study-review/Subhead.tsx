import type { ReactNode } from "react";

/** A quiet label over one part of an objective: what was taught, the note, the scores. */
export function Subhead({ children }: { children: ReactNode }) {
  return <h3 className="text-sm font-medium text-(--muted)">{children}</h3>;
}
