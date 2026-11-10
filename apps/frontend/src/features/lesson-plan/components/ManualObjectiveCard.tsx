import { RichContentEditor } from "@/shared/components/ui/RichContentEditor";

import type {
  CurriculumObjectiveOption,
  KcType,
  ObjectiveDraft,
} from "../manualDraft";

const fieldClass =
  "w-full border border-(--line-2) bg-(--surface) px-3 py-2 text-sm text-(--ink) outline-none focus:border-(--accent)";
const labelClass =
  "text-[11px] font-semibold uppercase tracking-[0.14em] text-(--muted)";

const KC_TYPES: { value: KcType; label: string }[] = [
  { value: "concept", label: "Concept (definition / idea)" },
  { value: "procedure", label: "Procedure (step-by-step method)" },
  {
    value: "representation",
    label: "Representation (diagram / number line / table)",
  },
];

/**
 * Edit one lesson objective and its instructional content. A concept objective
 * needs only an explanation; a procedure/representation objective also captures a
 * worked example. A practice item is always captured (it drives the evaluation
 * step). Content fields take Markdown + LaTeX via the MathLive-backed editor.
 */
export function ManualObjectiveCard({
  objective,
  index,
  curriculumOptions,
  onChange,
  onRemove,
}: {
  objective: ObjectiveDraft;
  index: number;
  curriculumOptions: CurriculumObjectiveOption[];
  onChange: (next: ObjectiveDraft) => void;
  onRemove: () => void;
}) {
  const patch = (next: Partial<ObjectiveDraft>) =>
    onChange({ ...objective, ...next });
  const needsWorkedExample = objective.kcType !== "concept";

  return (
    <div className="space-y-4 border border-(--line-2) bg-(--surface) p-4">
      <div className="flex items-center justify-between border-b border-(--line) pb-2">
        <p className="text-sm font-semibold text-(--ink)">
          Objective {index + 1}
        </p>
        <button
          type="button"
          onClick={onRemove}
          className="text-xs text-(--muted) hover:text-(--danger)"
        >
          Remove
        </button>
      </div>

      <label className="block space-y-1">
        <span className={labelClass}>Curriculum objective it serves</span>
        <select
          className={fieldClass}
          value={objective.curriculumObjectiveId}
          onChange={(event) =>
            patch({ curriculumObjectiveId: event.target.value })
          }
        >
          <option value="">— map to a curriculum objective —</option>
          {curriculumOptions.map((option) => (
            <option
              key={option.curriculum_objective_id}
              value={option.curriculum_objective_id}
            >
              {option.objective_order}. {option.objective_text}
            </option>
          ))}
        </select>
      </label>

      <label className="block space-y-1">
        <span className={labelClass}>
          Objective — what the learner will be able to do
        </span>
        <textarea
          rows={2}
          className={fieldClass}
          value={objective.objectiveText}
          onChange={(event) => patch({ objectiveText: event.target.value })}
        />
      </label>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <label className="block space-y-1">
          <span className={labelClass}>Type</span>
          <select
            className={fieldClass}
            value={objective.kcType}
            onChange={(event) =>
              patch({ kcType: event.target.value as KcType })
            }
          >
            {KC_TYPES.map((kc) => (
              <option key={kc.value} value={kc.value}>
                {kc.label}
              </option>
            ))}
          </select>
        </label>
        <label className="block space-y-1">
          <span className={labelClass}>Focus — the specific skill or idea</span>
          <input
            className={fieldClass}
            value={objective.kcFocus}
            onChange={(event) => patch({ kcFocus: event.target.value })}
          />
        </label>
      </div>

      <div className="space-y-1">
        <span className={labelClass}>Explanation</span>
        <RichContentEditor
          value={objective.explanation}
          onChange={(text) => patch({ explanation: text })}
          rows={3}
          placeholder="Explain the idea. Use $…$ for maths, e.g. $3 \times 10 = 30$."
        />
      </div>

      {needsWorkedExample ? (
        <WorkedExampleEditor objective={objective} onChange={onChange} />
      ) : null}

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div className="space-y-1">
          <span className={labelClass}>Practice question</span>
          <RichContentEditor
            value={objective.practice.question}
            onChange={(text) =>
              patch({ practice: { ...objective.practice, question: text } })
            }
            rows={2}
          />
        </div>
        <div className="space-y-1">
          <span className={labelClass}>Practice answer</span>
          <RichContentEditor
            value={objective.practice.answer}
            onChange={(text) =>
              patch({ practice: { ...objective.practice, answer: text } })
            }
            rows={2}
          />
        </div>
      </div>
    </div>
  );
}

function WorkedExampleEditor({
  objective,
  onChange,
}: {
  objective: ObjectiveDraft;
  onChange: (next: ObjectiveDraft) => void;
}) {
  const { workedExample } = objective;
  const labelClassLocal =
    "text-[11px] font-semibold uppercase tracking-[0.14em] text-(--muted)";
  const patchWorked = (next: Partial<ObjectiveDraft["workedExample"]>) =>
    onChange({ ...objective, workedExample: { ...workedExample, ...next } });
  const setStep = (
    stepIndex: number,
    key: "label" | "content",
    value: string,
  ) =>
    patchWorked({
      steps: workedExample.steps.map((step, i) =>
        i === stepIndex ? { ...step, [key]: value } : step,
      ),
    });

  return (
    <section className="space-y-3 border-t border-(--line) pt-3">
      <p className={labelClassLocal}>Worked example</p>
      <RichContentEditor
        value={workedExample.problem}
        onChange={(text) => patchWorked({ problem: text })}
        rows={2}
        placeholder="Problem statement"
      />
      {workedExample.steps.map((step, stepIndex) => (
        <div
          key={stepIndex}
          className="space-y-1 border-l-2 border-(--line) pl-3"
        >
          <div className="flex items-center justify-between">
            <input
              className="max-w-[140px] border border-(--line-2) bg-(--surface) px-2 py-1 text-xs text-(--ink)"
              value={step.label}
              onChange={(event) =>
                setStep(stepIndex, "label", event.target.value)
              }
              placeholder="Step 1"
            />
            <button
              type="button"
              onClick={() =>
                patchWorked({
                  steps: workedExample.steps.filter((_, i) => i !== stepIndex),
                })
              }
              className="text-xs text-(--muted) hover:text-(--danger)"
            >
              remove step
            </button>
          </div>
          <RichContentEditor
            value={step.content}
            onChange={(text) => setStep(stepIndex, "content", text)}
            rows={2}
            placeholder="What happens in this step"
          />
        </div>
      ))}
      <button
        type="button"
        onClick={() =>
          patchWorked({
            steps: [
              ...workedExample.steps,
              { label: `Step ${workedExample.steps.length + 1}`, content: "" },
            ],
          })
        }
        className="text-xs font-semibold text-(--accent-deep) hover:underline"
      >
        + add step
      </button>
      <div className="space-y-1">
        <span className={labelClassLocal}>Final answer</span>
        <RichContentEditor
          value={workedExample.finalAnswer}
          onChange={(text) => patchWorked({ finalAnswer: text })}
          rows={1}
          placeholder="Final answer"
        />
      </div>
    </section>
  );
}
