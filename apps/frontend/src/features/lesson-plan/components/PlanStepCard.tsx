import { ContentBlockRenderer } from "@/shared/components/renderer/ContentBlockRenderer";
import { ExplanationBlock } from "@/shared/components/renderer/ExplanationBlock";
import { RichText } from "@/shared/components/renderer/RichText";
import {
  ContentBlock,
  LessonStepStructured,
} from "@/shared/types/lesson-schema";

/** Renders a single instructional step with its metadata and content blocks. */
export function PlanStepCard({
  step,
  index,
}: {
  step: LessonStepStructured;
  index: number;
}) {
  const blocks = step.blocks ?? [];
  const minutes = step.duration_minutes ?? step.estimated_minutes;
  const badgeLabel = step.instructional_type ?? step.step_kind ?? step.type;
  // Rendered as the NERDC form prints them — two columns — while the underlying
  // `activities` list keeps the order the step actually runs in.
  const teacherActivities =
    step.activities?.filter((a) => a.who === "teacher").map((a) => a.what) ??
    [];
  const studentActivities =
    step.activities?.filter((a) => a.who === "student").map((a) => a.what) ??
    [];
  const hasActivities =
    teacherActivities.length > 0 || studentActivities.length > 0;
  const hasBlocks = blocks.length > 0;
  const stepContent = step.content?.trim();

  return (
    <div
      data-step-id={step.step_id}
      className="rounded-xl border border-(--line) bg-white overflow-hidden"
    >
      {/* Step header */}
      <div className="flex items-center justify-between border-b border-(--line) px-4 py-3 bg-(--sunken)/50">
        <div className="flex items-center gap-2">
          <span className="text-xs font-bold text-(--faint)">
            Step {index + 1}
          </span>
          <span className="rounded-none bg-(--accent-soft) text-(--accent-deep) px-2.5 py-0.5 text-[10px] font-bold uppercase tracking-wider">
            {badgeLabel}
          </span>
          <h3 className="text-sm font-semibold text-(--ink)">{step.title}</h3>
        </div>
        <div className="flex items-center gap-3 text-xs text-(--faint)">
          {minutes != null && <span>{minutes} min</span>}
        </div>
      </div>

      {/* Teacher/Student activities */}
      {hasActivities ? (
        <div className="grid sm:grid-cols-2 gap-0 border-b border-(--line)">
          {teacherActivities.length ? (
            <div className="p-3 border-r border-(--line)">
              <ActivityList
                label="Teacher Activities"
                activities={teacherActivities}
              />
            </div>
          ) : null}
          {studentActivities.length ? (
            <div className="p-3">
              <ActivityList
                label="Student Activities"
                activities={studentActivities}
              />
            </div>
          ) : null}
        </div>
      ) : null}

      {/* Step narrative/summary (Markdown + LaTeX). Carries the material for steps
          that have no content blocks (e.g. intro/conclusion). */}
      {stepContent ? (
        <div className="p-4 border-b border-(--line)">
          <ExplanationBlock
            block={{
              id: `${step.step_id}-content`,
              type: "explanation",
              content: stepContent,
            }}
          />
        </div>
      ) : null}

      {/* Content blocks */}
      {hasBlocks ? (
        <div className="p-4 space-y-3">
          {blocks.map((block: ContentBlock, i: number) => (
            <div key={block.id || `block-${i}`} data-block-id={block.id}>
              <ContentBlockRenderer block={block} />
            </div>
          ))}
        </div>
      ) : null}
    </div>
  );
}

/** One column of a step's activities; each activity is markdown with maths. */
function ActivityList({
  label,
  activities,
}: {
  label: string;
  activities: string[];
}) {
  return (
    <>
      <p className="text-[10px] font-bold text-(--faint) uppercase tracking-wider mb-1">
        {label}
      </p>
      <ul className="space-y-0.5">
        {activities.map((a, i) => (
          <li key={i} className="prose max-w-none text-xs text-(--ink-2)">
            <RichText text={a} />
          </li>
        ))}
      </ul>
    </>
  );
}
