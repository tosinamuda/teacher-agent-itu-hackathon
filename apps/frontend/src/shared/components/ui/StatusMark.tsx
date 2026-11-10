import type { ReactNode } from "react";

/** The one status vocabulary. Colour carries meaning only for the two dots. */
export type StatusKind =
  | "needsYou"
  | "complete"
  | "inProgress"
  | "waiting"
  | "notStarted"
  | "locked"
  | "rejected"
  | "withdrawn";

const NAMES: Record<StatusKind, string> = {
  needsYou: "Needs you",
  complete: "Complete",
  inProgress: "In progress",
  waiting: "Waiting on students",
  notStarted: "Not started",
  locked: "Locked",
  rejected: "Rejected or failed",
  withdrawn: "Withdrawn",
};

const MARK_COLOUR: Record<StatusKind, string> = {
  needsYou: "text-(--warning)",
  complete: "text-(--ink)",
  inProgress: "text-(--ink-2)",
  waiting: "text-(--ink-2)",
  notStarted: "text-(--ink-2)",
  locked: "text-(--faint)",
  rejected: "text-(--danger)",
  withdrawn: "text-(--faint)",
};

function Glyph({ kind }: { kind: StatusKind }) {
  switch (kind) {
    case "needsYou":
    case "rejected":
    case "withdrawn":
      return <circle cx="8" cy="8" r="4" fill="currentColor" />;
    case "complete":
      return <path d="M3.5 8.5l3 3 6-7" fill="none" stroke="currentColor" strokeWidth="1.5" />;
    case "inProgress":
      return (
        <>
          <circle cx="8" cy="8" r="5" fill="none" stroke="currentColor" strokeWidth="1.5" />
          <path d="M8 3a5 5 0 0 1 0 10z" fill="currentColor" />
        </>
      );
    case "waiting":
      return (
        <>
          <circle cx="8" cy="8" r="5" fill="none" stroke="currentColor" strokeWidth="1.5" />
          <path d="M8 5v3l2 1.5" fill="none" stroke="currentColor" strokeWidth="1.5" />
        </>
      );
    case "notStarted":
      return <circle cx="8" cy="8" r="4.5" fill="none" stroke="currentColor" strokeWidth="1.5" />;
    case "locked":
      return (
        <>
          <rect x="3.5" y="7" width="9" height="6" fill="none" stroke="currentColor" strokeWidth="1.5" />
          <path d="M5.5 7V5.5a2.5 2.5 0 0 1 5 0V7" fill="none" stroke="currentColor" strokeWidth="1.5" />
        </>
      );
  }
}

function Mark({ kind, label }: { kind: StatusKind; label?: string }) {
  return (
    <svg
      viewBox="0 0 16 16"
      width="16"
      height="16"
      className={`shrink-0 ${MARK_COLOUR[kind]}`}
      {...(label === undefined ? { "aria-hidden": true } : { role: "img", "aria-label": label })}
    >
      <Glyph kind={kind} />
    </svg>
  );
}

/** A status mark on its own, where the column or heading already names the state. */
export function StatusMark({ kind, label }: { kind: StatusKind; label?: string }) {
  return <Mark kind={kind} label={label ?? NAMES[kind]} />;
}

/** Mark and word together, for list rows. The word names the state, so the mark is decorative. */
export function Status({ kind, children }: { kind: StatusKind; children: ReactNode }) {
  return (
    <span className="inline-flex items-center gap-2 text-sm text-(--ink-2)">
      <Mark kind={kind} />
      {children}
    </span>
  );
}
