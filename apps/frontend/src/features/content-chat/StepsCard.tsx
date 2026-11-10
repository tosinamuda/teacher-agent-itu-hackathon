import { useState } from "react";

import { runningLine, toolLine } from "./toolLine";
import type { Step } from "./steps";
import { toolCount } from "./steps";

type State = "done" | "failed" | "running";

const MARK: Record<State, string> = {
  done: "bg-(--success-tint) text-(--success-ink)",
  failed: "bg-(--danger-tint) text-(--danger-ink)",
  running: "bg-(--surface) text-(--accent)",
};

/** A step's state as a small round mark: ticked, failed, or turning while it runs. */
function Mark({ state }: { state: State }) {
  return (
    <span
      aria-hidden
      className={`flex h-4 w-4 shrink-0 items-center justify-center rounded-full text-[9px] font-bold ${MARK[state]}`}
    >
      {state === "running" ? (
        <span className="h-3 w-3 animate-spin rounded-full border-2 border-(--line-2) border-t-(--accent)" />
      ) : state === "failed" ? (
        "!"
      ) : (
        "✓"
      )}
    </span>
  );
}

function Chevron({ open }: { open: boolean }) {
  return (
    <span aria-hidden className="ml-auto pl-2 text-[10px] text-(--faint)">
      {open ? "▾" : "▸"}
    </span>
  );
}

/** One step on the timeline: its mark sits on the line that joins the steps. */
function Row({ state, children }: { state: State; children: React.ReactNode }) {
  return (
    <li className="relative pl-7 before:absolute before:left-[7px] before:top-0 before:bottom-0 before:w-px before:bg-(--line-2)">
      <span className="absolute left-0 top-[7px]">
        <Mark state={state} />
      </span>
      {children}
    </li>
  );
}

function Part({
  label,
  children,
}: {
  label: string;
  children: React.ReactNode;
}) {
  return (
    <div>
      <p className="mb-0.5 text-[10px] font-semibold uppercase tracking-[0.12em] text-(--faint)">
        {label}
      </p>
      <p className="whitespace-pre-wrap [overflow-wrap:anywhere]">{children}</p>
    </div>
  );
}

/** A step with something to open: the title, and in a click what came before it and what it found. */
function Detailed({
  title,
  said,
  found,
  failed,
}: {
  title: string;
  said?: string;
  found?: string;
  failed: boolean;
}) {
  const [open, setOpen] = useState(false);
  const tone = failed ? "text-(--danger-ink)" : "text-(--ink)";
  if (!said && !found)
    return <div className={`px-2 py-1.5 ${tone}`}>{title}</div>;
  return (
    <>
      <button
        type="button"
        aria-expanded={open}
        onClick={() => setOpen(!open)}
        className={`flex w-full items-center px-2 py-1.5 text-left hover:bg-(--sunken) ${tone}`}
      >
        <span>{title}</span>
        <Chevron open={open} />
      </button>
      {open ? (
        <div className="mx-2 mb-2 space-y-3 border-l-2 border-(--line-2) bg-(--sunken) px-3 py-2 text-[13px] leading-relaxed">
          {said ? (
            <div className="text-(--ink-2)">
              <Part label="Before this step">{said}</Part>
            </div>
          ) : null}
          {found ? (
            <div className={failed ? "text-(--danger-ink)" : "text-(--ink)"}>
              <Part label={failed ? "Why it failed" : "Found"}>{found}</Part>
            </div>
          ) : null}
        </div>
      ) : null}
    </>
  );
}

/**
 * The agent's tool calls in one turn, as steps on a timeline that grows as it works. A step is
 * one row, ticked when it is done, and a click on it opens what came before it and what it
 * found. The card is open while the agent is at work and closes to a count once it has
 * finished, so the reply that follows is what the teacher reads.
 */
export function StepsCard({
  steps,
  active,
  workingOn,
}: {
  steps: readonly Step[];
  active: boolean;
  workingOn: string | null;
}) {
  const [chosen, setChosen] = useState<boolean | null>(null);
  const open = chosen ?? active;
  const count = toolCount(steps);
  return (
    <li className="overflow-hidden border border-(--line) bg-(--surface) text-xs">
      <button
        type="button"
        aria-expanded={open}
        onClick={() => setChosen(!open)}
        className="flex w-full items-center gap-2 bg-(--sunken) px-3 py-2 text-left"
      >
        <Mark state={active ? "running" : "done"} />
        <span className="text-[13px] font-semibold text-(--ink)">
          {active ? "Working on it" : "Worked on it"}
        </span>
        <span className="text-(--muted)">
          {count} {count === 1 ? "step" : "steps"}
        </span>
        <Chevron open={open} />
      </button>
      {open ? (
        <ol className="px-2 py-2">
          {steps.map((step) =>
            step.from === "thinking" ? (
              <Row key={step.id} state="done">
                <Detailed title="Thought" said={step.text} failed={false} />
              </Row>
            ) : (
              <Row key={step.id} state={step.failed ? "failed" : "done"}>
                <Detailed
                  title={`${step.failed ? "Could not: " : ""}${toolLine(step)}`}
                  said={step.said}
                  found={step.observed}
                  failed={step.failed}
                />
              </Row>
            ),
          )}
          {active && workingOn ? (
            <Row state="running">
              <div className="px-2 py-1.5 text-(--ink)">
                {runningLine(workingOn)}…
              </div>
            </Row>
          ) : null}
        </ol>
      ) : null}
    </li>
  );
}
