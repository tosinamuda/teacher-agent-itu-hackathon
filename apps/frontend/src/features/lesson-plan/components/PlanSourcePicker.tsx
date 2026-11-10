import { useRef, useState } from "react";

import {
  useExperimentWorkspaceLessons,
  useExperimentWorkspaces,
} from "@/features/experiments/hooks/useExperiments";

import { buttonClass } from "@/shared/components/ui/Button";

import type { PlanSource } from "../api/reusePlan";

const FIELD =
  "rounded-md border border-(--line) bg-(--surface) px-2 py-1.5 text-sm text-(--ink)";

/** Read a plan file as a plan's content; anything that is not a JSON object is refused. */
async function readPlanFile(file: File): Promise<Record<string, unknown>> {
  const parsed: unknown = JSON.parse(await file.text());
  if (typeof parsed !== "object" || parsed === null || Array.isArray(parsed)) {
    throw new Error("The file does not hold a lesson plan.");
  }
  return parsed as Record<string, unknown>;
}

/** A lesson id as a page's address spells it, without hyphens, so the two spellings compare equal. */
const bare = (id: string | undefined): string => (id ?? "").replaceAll("-", "");

type Mode = "lesson" | "file";

const MODES: { mode: Mode; label: string; hint: string }[] = [
  {
    mode: "lesson",
    label: "Another lesson's plan",
    hint: "An approved plan from a lesson of any class",
  },
  {
    mode: "file",
    label: "A plan file",
    hint: "A lesson plan saved as a JSON file",
  },
];

/** Choose the plan to reuse: the approved plan of another lesson, or a plan file. One at a time. */
export function PlanSourcePicker({
  onChange,
  allowFile = true,
  exceptLessonId,
}: {
  onChange: (source: PlanSource | null) => void;
  /** The lesson the plan is for, which is not offered as its own source. */
  exceptLessonId?: string;
  /** Whether a plan file can be chosen too; a lesson note is copied from a saved plan only. */
  allowFile?: boolean;
}) {
  const workspaces = useExperimentWorkspaces();
  const [mode, setMode] = useState<Mode>("lesson");
  const [workspaceId, setWorkspaceId] = useState<string | null>(null);
  const [lessonId, setLessonId] = useState("");
  const lessons = useExperimentWorkspaceLessons(workspaceId);
  const [fileName, setFileName] = useState<string | null>(null);
  const [fileError, setFileError] = useState<string | null>(null);
  const fileInput = useRef<HTMLInputElement | null>(null);

  const withPlans = (lessons.data ?? []).filter(
    (lesson) =>
      lesson.latest_approved_version_id &&
      bare(lesson.lesson_period_id) !== bare(exceptLessonId),
  );

  const choose = (next: Mode) => {
    if (next === mode) return;
    setMode(next);
    setLessonId("");
    setFileName(null);
    setFileError(null);
    if (fileInput.current) fileInput.current.value = "";
    onChange(null);
  };

  const pickFile = (file: File | undefined) => {
    setFileError(null);
    setFileName(file?.name ?? null);
    if (!file) return onChange(null);
    readPlanFile(file)
      .then((sessionPlan) =>
        onChange({ kind: "file", sessionPlan, fileName: file.name }),
      )
      .catch(() => {
        setFileError("The file is not a lesson plan in JSON.");
        setFileName(null);
        onChange(null);
      });
  };

  return (
    <div className="space-y-4">
      {allowFile ? (
        <div
          role="group"
          aria-label="Where the plan comes from"
          className="grid gap-2 sm:grid-cols-2"
        >
          {MODES.map(({ mode: option, label, hint }) => (
            <button
              key={option}
              type="button"
              aria-pressed={mode === option}
              onClick={() => choose(option)}
              className={`flex flex-col gap-0.5 border px-3 py-2 text-left ${
                mode === option
                  ? "border-(--ink) bg-(--surface)"
                  : "border-(--line-2) text-(--ink-2) hover:border-(--ink-2)"
              }`}
            >
              <span className="text-sm font-semibold text-(--ink)">
                {label}
              </span>
              <span className="text-xs text-(--ink-2)">{hint}</span>
            </button>
          ))}
        </div>
      ) : null}

      {mode === "lesson" ? (
        <fieldset className="space-y-2">
          <legend className="sr-only">Another lesson&apos;s plan</legend>
          {workspaces.isError ? (
            <p className="text-sm text-(--danger-ink)">
              Couldn&apos;t load the lessons that have plans.
              {allowFile ? " Use a plan file instead." : ""}
            </p>
          ) : (
            <div className="flex flex-wrap gap-3">
              <select
                aria-label="Class"
                className={FIELD}
                value={workspaceId ?? ""}
                onChange={(event) => {
                  setWorkspaceId(event.target.value || null);
                  setLessonId("");
                  onChange(null);
                }}
              >
                <option value="">Choose a class</option>
                {(workspaces.data ?? []).map((workspace) => (
                  <option
                    key={workspace.teacher_workspace_id}
                    value={workspace.teacher_workspace_id}
                  >
                    {`${workspace.class_name} · ${workspace.subject_name} · ${workspace.term} ${workspace.academic_year}`}
                  </option>
                ))}
              </select>
              <select
                aria-label="Lesson"
                className={FIELD}
                disabled={workspaceId === null}
                value={lessonId}
                onChange={(event) => {
                  setLessonId(event.target.value);
                  const version = withPlans.find(
                    (lesson) => lesson.lesson_period_id === event.target.value,
                  )?.latest_approved_version_id;
                  onChange(
                    version
                      ? { kind: "version", planVersionId: version }
                      : null,
                  );
                }}
              >
                <option value="">
                  {workspaceId && !lessons.isLoading && withPlans.length === 0
                    ? "No lesson here has an approved plan"
                    : "Choose a lesson"}
                </option>
                {withPlans.map((lesson) => (
                  <option
                    key={lesson.lesson_period_id}
                    value={lesson.lesson_period_id}
                  >
                    {`Week ${lesson.week_number}, period ${lesson.period_number}: ${lesson.lesson_title}`}
                  </option>
                ))}
              </select>
            </div>
          )}
        </fieldset>
      ) : (
        <fieldset className="space-y-2">
          <legend className="sr-only">A plan file</legend>
          <input
            ref={fileInput}
            type="file"
            accept=".json,application/json"
            aria-label="Plan file"
            className="sr-only"
            onChange={(event) => pickFile(event.target.files?.[0])}
          />
          <div className="flex flex-wrap items-center gap-3">
            <button
              type="button"
              onClick={() => fileInput.current?.click()}
              className={buttonClass({ variant: "secondary", size: "sm" })}
            >
              {fileName ? "Choose another file" : "Choose a file"}
            </button>
            <span className="text-sm text-(--ink-2)">
              {fileName ?? "No file chosen"}
            </span>
          </div>
          {fileError ? (
            <p className="text-sm text-(--danger-ink)">{fileError}</p>
          ) : null}
        </fieldset>
      )}
    </div>
  );
}
