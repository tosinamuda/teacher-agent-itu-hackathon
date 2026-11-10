import { useMemo, useState } from "react";

import { Button } from "@/shared/components/ui/Button";
import { AttachmentField } from "@/shared/components/ui/AttachmentField";

import type { OnBehalfItem, OnBehalfObjective, OnBehalfRequest } from "../api/onBehalf";
import { hasMarks, toMarkedWork, type WorkMark, type WorkedQuestion } from "../lib/markedWork";
import { ClassworkQuestions } from "./ClassworkQuestions";
import { MarkedWorkForm } from "./MarkedWorkForm";

type Mode = "chosen" | "score" | "work";
type ScoreDraft = Record<string, { score: string; max: string }>;

const inputClass =
  "w-20 border border-(--line-2) bg-(--surface) px-2 py-1 text-sm text-(--ink) outline-none focus:border-(--accent)";

/**
 * Record one student's responses: per-question chosen options (full signal) or, as
 * a fallback, per-objective scores (band only). The teacher reads the student's
 * marked sheet and can attach a photo of it.
 */
export function ResponseEntryForm({
  studentName,
  items,
  objectives,
  questions,
  onQuestionsChange,
  busy,
  onSubmit,
}: {
  studentName: string;
  items: OnBehalfItem[];
  objectives: OnBehalfObjective[];
  /** The classwork's worked questions, kept by the page so they last from one student to the next. */
  questions: WorkedQuestion[];
  onQuestionsChange: (questions: WorkedQuestion[]) => void;
  busy: boolean;
  onSubmit: (payload: Omit<OnBehalfRequest, "student_id">) => void;
}) {
  const hasItems = items.length > 0;
  const [mode, setMode] = useState<Mode>(hasItems ? "chosen" : "score");
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [scores, setScores] = useState<ScoreDraft>({});
  const [marks, setMarks] = useState<Record<string, WorkMark>>({});
  const [attachmentId, setAttachmentId] = useState<string | null>(null);

  const objectiveText = useMemo(
    () => new Map(objectives.map((o) => [o.lesson_objective_id, o.objective_text])),
    [objectives]
  );

  const chosenPayload = Object.entries(answers)
    .filter(([, option]) => option)
    .map(([item_id, selected_option]) => ({ item_id, selected_option }));

  const scorePayload = objectives
    .map((objective) => {
      const draft = scores[objective.lesson_objective_id];
      const score = Number(draft?.score);
      const max = Number(draft?.max);
      return { lesson_objective_id: objective.lesson_objective_id, score, max_score: max };
    })
    .filter((entry) => Number.isFinite(entry.score) && entry.max_score > 0 && entry.score <= entry.max_score);

  const workPayload = toMarkedWork(questions, marks);

  const canSave =
    mode === "chosen"
      ? chosenPayload.length > 0
      : mode === "score"
        ? scorePayload.length > 0
        : hasMarks(workPayload);

  const save = () =>
    onSubmit(
      mode === "chosen"
        ? { answers: chosenPayload, provenance_attachment_id: attachmentId }
        : mode === "score"
          ? { objective_scores: scorePayload, provenance_attachment_id: attachmentId }
          : { marked_work: workPayload, provenance_attachment_id: attachmentId }
    );

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <p className="text-sm font-semibold text-(--ink)">Recording for {studentName}</p>
        <div className="flex gap-0.5 border border-(--line-2) text-xs">
          {hasItems ? (
            <ModeTab active={mode === "chosen"} onClick={() => setMode("chosen")}>
              Per question
            </ModeTab>
          ) : null}
          <ModeTab active={mode === "work"} onClick={() => setMode("work")}>
            Marked work
          </ModeTab>
          <ModeTab active={mode === "score"} onClick={() => setMode("score")}>
            Score only
          </ModeTab>
        </div>
      </div>

      {mode === "work" ? (
        <div className="space-y-5">
          <ClassworkQuestions
            questions={questions}
            objectives={objectives}
            onChange={onQuestionsChange}
          />
          <MarkedWorkForm
            questions={questions}
            marks={marks}
            onMark={(id, mark) => setMarks((current) => ({ ...current, [id]: mark }))}
          />
        </div>
      ) : mode === "chosen" ? (
        <div className="space-y-4">
          {items.map((item, index) => (
            <fieldset key={item.item_id} className="space-y-2 border border-(--line-2) bg-(--surface) p-3">
              <legend className="text-sm text-(--ink-2)">
                {index + 1}. {item.stem}
              </legend>
              <div className="flex flex-wrap gap-3">
                {Object.entries(item.options).map(([key, label]) => (
                  <label key={key} className="flex items-center gap-1 text-sm text-(--ink-2)">
                    <input
                      type="radio"
                      name={`item-${item.item_id}`}
                      checked={answers[item.item_id] === key}
                      onChange={() =>
                        setAnswers((current) => ({ ...current, [item.item_id]: key }))
                      }
                    />
                    <span className="font-semibold">{key}.</span> {label}
                  </label>
                ))}
              </div>
            </fieldset>
          ))}
        </div>
      ) : (
        <div className="space-y-2">
          <p className="text-xs text-(--muted)">
            Enter how many each student got right per objective. This gives a band but no
            misconception (use Per question or Marked work to capture the mistake).
          </p>
          {objectives.map((objective) => {
            const draft = scores[objective.lesson_objective_id] ?? { score: "", max: "" };
            const setDraft = (next: Partial<{ score: string; max: string }>) =>
              setScores((current) => ({
                ...current,
                [objective.lesson_objective_id]: { ...draft, ...next },
              }));
            return (
              <div
                key={objective.lesson_objective_id}
                className="flex items-center justify-between gap-3 border border-(--line-2) bg-(--surface) px-3 py-2"
              >
                <span className="text-sm text-(--ink-2)">
                  {objectiveText.get(objective.lesson_objective_id) || objective.lesson_objective_id}
                </span>
                <span className="flex items-center gap-1 text-sm text-(--muted)">
                  <input
                    className={inputClass}
                    type="number"
                    min={0}
                    value={draft.score}
                    placeholder="got"
                    onChange={(event) => setDraft({ score: event.target.value })}
                  />
                  <span>/</span>
                  <input
                    className={inputClass}
                    type="number"
                    min={1}
                    value={draft.max}
                    placeholder="of"
                    onChange={(event) => setDraft({ max: event.target.value })}
                  />
                </span>
              </div>
            );
          })}
        </div>
      )}

      <AttachmentField
        value={attachmentId}
        kind="student_answer_sheet"
        label="Photo of the student's marked sheet (optional)"
        onChange={setAttachmentId}
      />

      <Button isLoading={busy} disabled={!canSave} onClick={save}>
        Save responses
      </Button>
    </div>
  );
}

function ModeTab({
  active,
  onClick,
  children,
}: {
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`px-3 py-1 font-semibold ${
        active ? "bg-(--accent-soft) text-(--accent-deep)" : "text-(--muted) hover:bg-(--surface-2)"
      }`}
    >
      {children}
    </button>
  );
}
