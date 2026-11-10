import { ContentBlockRenderer } from "@/shared/components/renderer/ContentBlockRenderer";
import { ExplanationBlock } from "@/shared/components/renderer/ExplanationBlock";
import { RichText } from "@/shared/components/renderer/RichText";
import type {
  ContentBlock,
  LessonStepStructured,
} from "@/shared/types/lesson-schema";

const OVERLINE =
  "text-[11px] font-semibold uppercase tracking-[0.12em] text-(--faint)";

function Activities({ label, items }: { label: string; items: string[] }) {
  return (
    <div className="flex flex-col gap-2">
      <h4 className={OVERLINE}>{label}</h4>
      <ul className="flex flex-col gap-1.5">
        {items.map((item, at) => (
          <li key={at} className="flex gap-2 text-sm text-(--ink)">
            <span aria-hidden="true" className="text-(--ink-2)">
              ▪
            </span>
            <span className="prose max-w-none">
              <RichText text={item} />
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}

/** One step as a row that opens: its length and share of the lesson show closed; its activities and content show open. */
export function PlanStepRow({
  step,
  number,
  share,
  open,
  onToggle,
  mark,
}: {
  step: LessonStepStructured;
  number: number;
  /** The step's share of the lesson, in percent. */
  share: number;
  open: boolean;
  onToggle: (open: boolean) => void;
  /** The agent changed this step, or is changing it now. */
  mark?: "changed" | "revising";
}) {
  const minutes = step.duration_minutes ?? step.estimated_minutes;
  const teacher =
    step.activities?.filter((a) => a.who === "teacher").map((a) => a.what) ??
    [];
  const students =
    step.activities?.filter((a) => a.who === "student").map((a) => a.what) ??
    [];
  const narrative = step.content?.trim();
  const blocks = step.blocks ?? [];

  return (
    <details
      id={`step-${step.step_id}`}
      data-step-id={step.step_id}
      open={open}
      onToggle={(event) => onToggle(event.currentTarget.open)}
      className={`group border-t border-(--line) first:border-t-0 ${
        mark === "revising"
          ? "outline outline-2 -outline-offset-2 outline-(--accent)"
          : ""
      }`}
    >
      <summary className="flex cursor-pointer list-none items-center gap-3 px-4 py-3 hover:bg-(--sunken) [&::-webkit-details-marker]:hidden">
        <span className="w-5 shrink-0 text-xs text-(--ink-2)">{number}</span>
        <span className="flex min-w-0 flex-1 flex-col gap-1.5">
          <span className="flex items-center gap-2 text-sm font-semibold text-(--ink)">
            {step.title}
            {mark === "changed" ? (
              <span className="bg-(--info-tint) px-1.5 py-0.5 text-[11px] font-medium text-(--info-ink)">
                Changed
              </span>
            ) : null}
            {mark === "revising" ? (
              <span className="text-[11px] font-medium text-(--accent-deep)">
                The agent is changing this
              </span>
            ) : null}
          </span>
          <span aria-hidden="true" className="h-0.5 bg-(--line)">
            <span
              className="block h-full bg-(--ink-2)"
              style={{ width: `${Math.max(share, 4)}%` }}
            />
          </span>
        </span>
        {minutes != null ? (
          <span className="shrink-0 text-xs text-(--faint)">{minutes} min</span>
        ) : null}
        <svg
          viewBox="0 0 16 16"
          width="14"
          height="14"
          aria-hidden="true"
          className="shrink-0 text-(--ink-2) transition-transform group-open:rotate-90"
        >
          <path
            d="M6 3.5L10.5 8 6 12.5"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.5"
          />
        </svg>
      </summary>
      <div className="flex flex-col gap-4 px-4 pb-5 pl-12">
        <div className="grid gap-6 sm:grid-cols-2">
          <Activities label="Teacher" items={teacher} />
          <Activities label="Students" items={students} />
        </div>
        {narrative || blocks.length > 0 ? (
          <details>
            <summary className="cursor-pointer text-xs font-semibold text-(--ink-2) hover:text-(--ink)">
              Lesson content for this step
            </summary>
            <div className="mt-3 flex flex-col gap-3 border-l-2 border-(--line) pl-4">
              {narrative ? (
                <ExplanationBlock
                  block={{
                    id: `${step.step_id}-content`,
                    type: "explanation",
                    content: narrative,
                  }}
                />
              ) : null}
              {blocks.map((block: ContentBlock, at: number) => (
                <div key={block.id || `block-${at}`} data-block-id={block.id}>
                  <ContentBlockRenderer block={block} />
                </div>
              ))}
            </div>
          </details>
        ) : null}
      </div>
    </details>
  );
}
