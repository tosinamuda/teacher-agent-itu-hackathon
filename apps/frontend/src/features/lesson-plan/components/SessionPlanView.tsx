import { useRef } from "react";
import { LessonStepStructured } from "@/shared/types/lesson-schema";
import { SourceReferences } from "@/shared/components/references/SourceReferences";

import { useTypesetMath } from "../hooks/useTypesetMath";

import { PlanStepCard } from "./PlanStepCard";

/** Metadata fields displayed in the session plan header. */
interface SessionPlanMetadata {
  subject?: string;
  grade?: string;
  term?: string;
  week?: number;
  topic?: string;
  subtopic?: string;
  track?: string;
}

/** The structured session plan content from the API. */
export interface SessionPlanData {
  steps: LessonStepStructured[];
  curriculum_objectives?:
    | {
        curriculum_objective_id: string;
        objective_text: string;
        objective_order: number;
      }[]
    | null;
  lesson_plan_objectives?:
    | {
        lesson_objective_id: string;
        objective_text: string;
        objective_order: number;
        curriculum_objective_id: string;
        curriculum_objective_text: string;
        kc_type: "concept" | "procedure" | "representation";
        kc_focus: string;
        source_form?: string | null;
        target_form?: string | null;
      }[]
    | null;
  theme?: string | null;
  entry_behaviour?: string[] | null;
  instructional_materials?: string[] | null;
  references?: string[] | null;
}

/**
 * Renders a session plan as a document in NERDC format: its objectives, the rest of the plan's
 * context on one line that opens, then every step, open.
 */
export function SessionPlanView({
  sessionPlan,
  metadata,
}: {
  sessionPlan: SessionPlanData;
  metadata?: SessionPlanMetadata;
}) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const steps = sessionPlan.steps;

  useTypesetMath(containerRef, sessionPlan);

  return (
    <div
      ref={containerRef}
      id="lesson-plan-content"
      className="flex min-h-0 flex-1 flex-col gap-6 overflow-y-auto overscroll-contain"
    >
      {/* Header: Subject, Grade, Term, Week */}
      {metadata && (
        <div className="rounded-xl bg-(--sunken) border border-(--line) p-4">
          <div className="flex flex-wrap gap-3 text-sm">
            {metadata.subject && (
              <span className="rounded-none bg-white border border-(--line) px-3 py-1 font-medium">
                {metadata.subject}
              </span>
            )}
            {metadata.grade && (
              <span className="rounded-none bg-white border border-(--line) px-3 py-1">
                {metadata.grade}
              </span>
            )}
            {metadata.term && (
              <span className="rounded-none bg-white border border-(--line) px-3 py-1">
                {metadata.term}
              </span>
            )}
            {metadata.week != null && (
              <span className="rounded-none bg-white border border-(--line) px-3 py-1">
                Week {metadata.week}
              </span>
            )}
          </div>
          {(metadata.topic || metadata.subtopic) && (
            <div className="mt-3 space-y-0.5">
              {metadata.topic && (
                <p className="text-sm font-semibold text-(--ink)">
                  {metadata.topic}
                </p>
              )}
              {metadata.subtopic && (
                <p className="text-sm text-(--ink-2)">{metadata.subtopic}</p>
              )}
            </div>
          )}
        </div>
      )}

      <PlanObjectives sessionPlan={sessionPlan} />
      <PlanContext sessionPlan={sessionPlan} />

      <section aria-label="Steps" className="space-y-3">
        <h3 className="text-base font-semibold text-(--ink)">
          Steps{" "}
          <span className="font-normal text-(--faint)">· {steps.length}</span>
        </h3>
        {steps.map((step, index) => (
          <PlanStepCard key={step.step_id} step={step} index={index} />
        ))}
      </section>
    </div>
  );
}

function ListSection({
  label,
  items,
  ids,
}: {
  label: string;
  items: string[];
  ids?: (string | undefined)[];
}) {
  return (
    <div>
      <h3 className="text-xs font-semibold text-(--faint) uppercase tracking-wider mb-2">
        {label}
      </h3>
      <ul className="space-y-1">
        {items.map((item, i) => (
          <li
            key={i}
            data-objective-id={ids?.[i]}
            className="text-sm text-(--ink-2) flex gap-2"
          >
            <span className="text-(--faint) shrink-0">&#8226;</span>
            <span className="min-w-0 flex-1 [overflow-wrap:anywhere]">
              {item}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}

/** What the lesson sets out to do: the curriculum's objectives and the plan's own. */
function PlanObjectives({ sessionPlan }: { sessionPlan: SessionPlanData }) {
  const curriculum = sessionPlan.curriculum_objectives ?? [];
  const lesson = sessionPlan.lesson_plan_objectives ?? [];
  if (!curriculum.length && !lesson.length) return null;
  return (
    <div className="grid gap-x-6 gap-y-4 rounded-xl border border-(--line) bg-white p-4 sm:grid-cols-2">
      {curriculum.length ? (
        <ListSection
          label="Curriculum Objectives"
          items={curriculum.map((o) => o.objective_text)}
        />
      ) : null}
      {lesson.length ? (
        <ListSection
          label="Lesson Plan Objectives"
          items={lesson.map((o) => o.objective_text)}
          ids={lesson.map((o) => o.lesson_objective_id)}
        />
      ) : null}
    </div>
  );
}

/** What the lesson draws on: what students already know, the materials and the sources. */
function PlanContext({ sessionPlan }: { sessionPlan: SessionPlanData }) {
  const entry = sessionPlan.entry_behaviour ?? [];
  const materials = sessionPlan.instructional_materials ?? [];
  const references = sessionPlan.references ?? [];
  if (!entry.length && !materials.length && !references.length) return null;
  return (
    <section
      aria-label="Basis for the plan"
      className="rounded-xl border border-(--line) bg-white p-4"
    >
      <div className="space-y-4">
        <div className="grid gap-x-6 gap-y-4 sm:grid-cols-2">
          {entry.length ? (
            <ListSection label="Students already know" items={entry} />
          ) : null}
          {materials.length ? (
            <ListSection label="Materials" items={materials} />
          ) : null}
        </div>
        {references.length ? (
          <div>
            <h3 className="text-xs font-semibold text-(--faint) uppercase tracking-wider mb-2">
              Sources
            </h3>
            <SourceReferences references={references} />
          </div>
        ) : null}
      </div>
    </section>
  );
}
