import { ContentBlockRenderer } from "@/shared/components/renderer/ContentBlockRenderer";
import { SourceReferences } from "@/shared/components/references/SourceReferences";

import { ExperimentStoryLessonPlan } from "../lib/experiments";

/** A labelled list of plain-string plan fields (materials, references, …). */
function FieldList({ label, items }: { label: string; items?: string[] }) {
  if (!items || items.length === 0) return null;
  return (
    <div>
      <p className="text-sm text-(--muted)">{label}</p>
      <ul className="mt-1 list-disc space-y-0.5 pl-5 text-sm text-(--ink)">
        {items.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

/**
 * Renders the teacher's authored lesson plan as the origin of the Experiment Story:
 * the lesson objectives, entry behaviour, materials and references, then the teaching
 * steps (each step's blocks via the shared ContentBlockRenderer). This is what the
 * teacher wrote, before any student artefact exists.
 */
export function StoryLessonPlan({ plan }: { plan: ExperimentStoryLessonPlan | null | undefined }) {
  if (!plan) {
    return <p className="text-sm italic text-(--muted)">Lesson plan not available.</p>;
  }
  const objectives = plan.lesson_plan_objectives ?? [];
  const steps = plan.steps ?? [];

  return (
    <div className="space-y-5">
      {objectives.length > 0 ? (
        <div>
          <p className="text-sm text-(--muted)">Lesson objectives</p>
          <ol className="mt-1 list-decimal space-y-0.5 pl-5 text-sm text-(--ink)">
            {objectives.map((objective) => (
              <li key={objective.lesson_objective_id ?? objective.objective_text}>
                {objective.objective_text}
              </li>
            ))}
          </ol>
        </div>
      ) : null}

      <div className="grid gap-4 sm:grid-cols-2">
        <FieldList label="Entry behaviour" items={plan.entry_behaviour} />
        <FieldList label="Instructional materials" items={plan.instructional_materials} />
      </div>

      {plan.references?.length ? (
        <div>
          <p className="text-sm text-(--muted)">References</p>
          <div className="mt-1">
            <SourceReferences references={plan.references} />
          </div>
        </div>
      ) : null}

      {steps.length > 0 ? (
        <div className="space-y-4">
          <p className="text-sm text-(--muted)">Teaching steps</p>
          {steps.map((step) => (
            <div key={step.step_id} className="border-t border-(--line) pt-3">
              <p className="mb-2 font-medium text-(--ink)">
                {step.title}
                {step.step_kind ? (
                  <span className="ml-2 text-sm font-normal text-(--muted)">{step.step_kind}</span>
                ) : null}
              </p>
              {(step.blocks ?? []).length > 0 ? (
                <div className="space-y-2">
                  {(step.blocks ?? []).map((block, index) => (
                    <ContentBlockRenderer
                      key={block.id ?? `${step.step_id}-${index}`}
                      block={block}
                    />
                  ))}
                </div>
              ) : null}
            </div>
          ))}
        </div>
      ) : null}
    </div>
  );
}
