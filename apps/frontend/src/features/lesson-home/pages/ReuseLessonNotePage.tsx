import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";

import { reuseLessonNote } from "@/features/content/api/reuseNote";
import { useLessonContent } from "@/features/content/hooks/useContent";
import type { ContentSummary } from "@/features/content/types";
import { useStudySources } from "@/features/class-evidence/hooks/useStudyResults";
import { PlanSourcePicker } from "@/features/lesson-plan/components/PlanSourcePicker";
import { ThisLesson } from "@/features/lesson-plan/components/ThisLesson";
import type { PlanSource } from "@/features/lesson-plan/api/reusePlan";
import { Button } from "@/shared/components/ui/Button";
import { Link, useRouter } from "@/shared/router";

import { useLessonHome } from "../hooks/useLessonHome";

const errorMessage = (error: unknown): string =>
  error instanceof Error ? error.message : "Something went wrong.";

const day = (iso: string | null): string => (iso ? iso.slice(0, 10) : "");

function Notes({
  notes,
  chosen,
  onChoose,
}: {
  notes: ContentSummary[];
  chosen: string | null;
  onChoose: (id: string) => void;
}) {
  if (notes.length === 0)
    return (
      <p className="text-sm text-(--ink-2)">
        That lesson has no lesson note yet.
      </p>
    );
  return (
    <fieldset className="flex flex-col gap-2">
      <legend className="text-sm font-semibold text-(--ink)">
        Its lesson note
      </legend>
      {notes.map((note) => (
        <label
          key={note.id}
          className="flex items-center gap-3 border border-(--line) bg-(--surface) px-3 py-2 text-sm"
        >
          <input
            type="radio"
            name="note"
            checked={chosen === note.id}
            onChange={() => onChoose(note.id)}
          />
          <span className="flex-1 text-(--ink)">
            Lesson note · version {note.version} · {day(note.created_at)}
          </span>
          <span className="text-xs text-(--ink-2)">
            {note.review_status === "approved" ? "Approved" : "Not approved"}
          </span>
        </label>
      ))}
    </fieldset>
  );
}

/** The evaluation's lessons whose approved note has a section for every step of this plan. */
function EvaluationNotes({
  lessonPeriodId,
  chosen,
  onChoose,
}: {
  lessonPeriodId: string;
  chosen: string | null;
  onChoose: (id: string) => void;
}) {
  const sources = useStudySources(lessonPeriodId, true);
  const withNotes = (sources.data ?? []).filter(
    (source) => source.lesson_note_id && source.note_fits,
  );
  if (sources.isLoading) return null;
  if (withNotes.length === 0)
    return (
      <p className="text-sm text-(--ink-2)">
        None of the evaluation&apos;s lessons has a lesson note that fits this plan&apos;s steps.
      </p>
    );
  return (
    <fieldset className="flex flex-col gap-2">
      <legend className="text-sm font-semibold text-(--ink)">
        The evaluation&apos;s lesson
      </legend>
      {withNotes.map((source) => (
        <label
          key={source.plan_version_id}
          className="flex items-center gap-3 border border-(--line) bg-(--surface) px-3 py-2 text-sm"
        >
          <input
            type="radio"
            name="evaluation-note"
            checked={chosen === source.lesson_note_id}
            onChange={() => onChoose(source.lesson_note_id as string)}
          />
          <span className="flex-1 text-(--ink)">{source.lesson_title}</span>
          <span className="text-xs text-(--ink-2)">Its note has every step of this plan</span>
        </label>
      ))}
    </fieldset>
  );
}

type Where = "lesson" | "evaluation";

const WHERE: { where: Where; label: string; hint: string }[] = [
  { where: "lesson", label: "Another lesson's note", hint: "A note from a lesson of any class you teach" },
  { where: "evaluation", label: "The evaluation's lesson note", hint: "The lesson note the study used" },
];

/**
 * Use the lesson note of another lesson's plan as this plan's note. It can be copied where the
 * plans have the same steps, as when this plan was reused from that one.
 */
export function ReuseLessonNotePage({
  lessonPeriodId,
}: {
  lessonPeriodId: string;
}) {
  const router = useRouter();
  const queryClient = useQueryClient();
  const home = useLessonHome(lessonPeriodId);
  const [where, setWhere] = useState<Where>("lesson");
  const [source, setSource] = useState<PlanSource | null>(null);
  const [chosen, setChosen] = useState<string | null>(null);
  const sourceVersion =
    source?.kind === "version" ? source.planVersionId : null;
  const notes = (useLessonContent(sourceVersion).data ?? []).filter(
    (item) => item.type === "lesson-note" && item.level === "class",
  );

  const copy = useMutation({
    mutationFn: (sourceId: string) =>
      reuseLessonNote(sourceId, home.planVersionId as string),
    onSuccess: (result) => {
      void queryClient.invalidateQueries({ queryKey: ["content"] });
      router.push(`/research/teacher/content/${result.content_id}`);
    },
  });

  return (
    <main className="mx-auto flex w-full max-w-2xl flex-col gap-6 py-6">
      <Link
        href={`/research/teacher/lessons/${lessonPeriodId}`}
        className="text-sm text-(--ink-2) hover:text-(--ink)"
      >
        ‹ Back to the lesson
      </Link>
      <header className="flex flex-col gap-1">
        <h1 className="text-2xl font-semibold text-(--ink)">
          Use an existing lesson note
        </h1>
        <p className="text-sm text-(--ink-2)">
          Choose the lesson whose note you want. It is copied onto this
          lesson&apos;s plan, so the two plans need the same steps. You read it
          through and approve it as you would any note.
        </p>
      </header>
      {home.planVersionId === null && !home.isLoading ? (
        <p className="text-sm text-(--ink-2)">
          Approve this lesson&apos;s plan first. A note is made from an approved
          plan.
        </p>
      ) : (
        <>
          <ThisLesson lessonPeriodId={lessonPeriodId} />
          <div role="group" aria-label="Where the note comes from" className="grid gap-2 sm:grid-cols-2">
            {WHERE.map((option) => (
              <button
                key={option.where}
                type="button"
                aria-pressed={where === option.where}
                onClick={() => {
                  setWhere(option.where);
                  setSource(null);
                  setChosen(null);
                  copy.reset();
                }}
                className={`flex flex-col gap-0.5 border px-3 py-2 text-left ${
                  where === option.where
                    ? "border-(--ink) bg-(--surface)"
                    : "border-(--line-2) text-(--ink-2) hover:border-(--ink-2)"
                }`}
              >
                <span className="text-sm font-semibold text-(--ink)">{option.label}</span>
                <span className="text-xs text-(--ink-2)">{option.hint}</span>
              </button>
            ))}
          </div>
          {where === "lesson" ? (
            <>
              <PlanSourcePicker
                allowFile={false}
                exceptLessonId={lessonPeriodId}
                onChange={(next) => {
                  setSource(next);
                  setChosen(null);
                  copy.reset();
                }}
              />
              {sourceVersion ? (
                <Notes notes={notes} chosen={chosen} onChoose={setChosen} />
              ) : null}
            </>
          ) : (
            <EvaluationNotes
              lessonPeriodId={lessonPeriodId}
              chosen={chosen}
              onChoose={(id) => {
                setChosen(id);
                copy.reset();
              }}
            />
          )}
          {copy.isError ? (
            <p role="alert" className="text-sm text-(--danger-ink)">
              {errorMessage(copy.error)}
            </p>
          ) : null}
          <div>
            <Button
              isLoading={copy.isPending}
              disabled={chosen === null}
              onClick={() => chosen && copy.mutate(chosen)}
            >
              Use this note
            </Button>
          </div>
        </>
      )}
    </main>
  );
}
