import type {
  KnowledgeComponentOption,
  ManualClassworkObjective,
} from "../api/manualClasswork";
import {
  nextOptionKey,
  type ClassworkItemDraft,
  type OptionDraft,
} from "../manualClassworkDraft";

const fieldClass =
  "w-full border border-(--line-2) bg-(--surface) px-3 py-2 text-sm text-(--ink) outline-none focus:border-(--accent)";
const labelClass = "text-[11px] font-semibold uppercase tracking-[0.14em] text-(--muted)";

const DIFFICULTIES = [
  { value: "", label: "—" },
  { value: "easy", label: "Easy" },
  { value: "medium", label: "Medium" },
  { value: "hard", label: "Hard" },
];

/**
 * Enter one MCQ classwork item: tag it to a lesson objective, write the stem and
 * options, and mark the correct one. The optional knowledge component and difficulty
 * mirror what the generated diagnostic stores. (Per-distractor misconceptions are
 * derived later, in FD-03 — not entered here.)
 */
export function ManualClassworkItemCard({
  item,
  index,
  objectives,
  knowledgeComponents,
  onChange,
  onRemove,
}: {
  item: ClassworkItemDraft;
  index: number;
  objectives: ManualClassworkObjective[];
  knowledgeComponents: KnowledgeComponentOption[];
  onChange: (next: ClassworkItemDraft) => void;
  onRemove: () => void;
}) {
  const patch = (next: Partial<ClassworkItemDraft>) => onChange({ ...item, ...next });

  const setOption = (key: string, text: string) =>
    patch({
      options: item.options.map((option) => (option.key === key ? { ...option, text } : option)),
    });

  const setMisconception = (key: string, value: string) =>
    patch({
      distractorMisconceptions: { ...item.distractorMisconceptions, [key]: value },
    });

  const addOption = () => {
    const key = nextOptionKey(item.options);
    if (!key) return;
    patch({ options: [...item.options, { key, text: "" }] });
  };

  const removeOption = (key: string) =>
    patch({
      options: item.options.filter((option) => option.key !== key),
      correctOption: item.correctOption === key ? "" : item.correctOption,
    });

  return (
    <div className="space-y-4 border border-(--line-2) bg-(--surface) p-4">
      <div className="flex items-center justify-between border-b border-(--line) pb-2">
        <p className="text-sm font-semibold text-(--ink)">Item {index + 1}</p>
        <button
          type="button"
          onClick={onRemove}
          className="text-xs text-(--muted) hover:text-(--danger)"
        >
          Remove
        </button>
      </div>

      <label className="block space-y-1">
        <span className={labelClass}>Objective this item assesses</span>
        <select
          className={fieldClass}
          value={item.lessonObjectiveId}
          onChange={(event) => patch({ lessonObjectiveId: event.target.value })}
        >
          <option value="">— tag to a lesson objective —</option>
          {objectives.map((objective) => (
            <option key={objective.lesson_objective_id} value={objective.lesson_objective_id}>
              {objective.objective_text || objective.lesson_objective_id}
            </option>
          ))}
        </select>
      </label>

      <label className="block space-y-1">
        <span className={labelClass}>Question</span>
        <textarea
          rows={2}
          className={fieldClass}
          value={item.stem}
          placeholder="The classwork question as written"
          onChange={(event) => patch({ stem: event.target.value })}
        />
      </label>

      <fieldset className="space-y-2">
        <legend className={labelClass}>Options — select the correct one</legend>
        {item.options.map((option: OptionDraft) => (
          <div key={option.key} className="space-y-1">
            <div className="flex items-center gap-2">
              <label className="flex items-center gap-1 text-sm text-(--ink-2)">
                <input
                  type="radio"
                  name={`correct-${index}`}
                  checked={item.correctOption === option.key}
                  onChange={() => patch({ correctOption: option.key })}
                  aria-label={`Mark option ${option.key} correct`}
                />
                <span className="w-4 font-semibold">{option.key}</span>
              </label>
              <input
                className={fieldClass}
                value={option.text}
                placeholder={`Option ${option.key}`}
                onChange={(event) => setOption(option.key, event.target.value)}
              />
              {item.options.length > 2 ? (
                <button
                  type="button"
                  onClick={() => removeOption(option.key)}
                  className="text-xs text-(--muted) hover:text-(--danger)"
                  aria-label={`Remove option ${option.key}`}
                >
                  ✕
                </button>
              ) : null}
            </div>
            {option.key !== item.correctOption && option.text.trim() ? (
              <input
                className="ml-7 w-[calc(100%-1.75rem)] border border-(--line) bg-(--surface-2) px-2 py-1 text-xs text-(--ink-2) outline-none focus:border-(--accent)"
                value={item.distractorMisconceptions[option.key] ?? ""}
                placeholder="misconception if chosen (e.g. divides_instead_of_multiplies)"
                onChange={(event) => setMisconception(option.key, event.target.value)}
                aria-label={`Misconception for option ${option.key}`}
              />
            ) : null}
          </div>
        ))}
        {item.options.length < 8 ? (
          <button
            type="button"
            onClick={addOption}
            className="text-xs font-semibold text-(--accent-deep) hover:underline"
          >
            + add option
          </button>
        ) : null}
      </fieldset>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <label className="block space-y-1">
          <span className={labelClass}>Knowledge component (optional)</span>
          <select
            className={fieldClass}
            value={item.knowledgeComponentId}
            onChange={(event) => patch({ knowledgeComponentId: event.target.value })}
          >
            <option value="">— none —</option>
            {knowledgeComponents.map((kc) => (
              <option key={kc.id} value={kc.id}>
                {kc.kc_code} — {kc.description}
              </option>
            ))}
          </select>
        </label>
        <label className="block space-y-1">
          <span className={labelClass}>Difficulty (optional)</span>
          <select
            className={fieldClass}
            value={item.difficulty}
            onChange={(event) => patch({ difficulty: event.target.value })}
          >
            {DIFFICULTIES.map((difficulty) => (
              <option key={difficulty.value} value={difficulty.value}>
                {difficulty.label}
              </option>
            ))}
          </select>
        </label>
      </div>
    </div>
  );
}
