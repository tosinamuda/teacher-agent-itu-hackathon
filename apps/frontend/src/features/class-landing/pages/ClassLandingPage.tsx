import { useState } from "react";

import { useSchemeOfWork } from "@/features/curriculum/hooks/useSchemeOfWork";
import { usePendingPacks } from "@/features/pack-review/hooks/usePendingPacks";
import { useTeachingWorkspace } from "@/features/teaching-workspace/context/TeachingWorkspaceContext";
import { useLessonReviews } from "@/features/teaching-workspace/hooks/useLessonReviews";
import { useWorkspaceLessons } from "@/features/teaching-workspace/hooks/useWorkspaceLessons";
import { formatClassLabel } from "@/features/teaching-workspace/lib/labels";
import { buttonClass } from "@/shared/components/ui/Button";
import {
  RightPanel,
  type NeedsItem,
} from "@/shared/components/workspace/RightPanel";
import { WorkspacePage } from "@/shared/components/workspace/WorkspacePage";
import { Link } from "@/shared/router";

import {
  lessonCountText,
  lessonToStart,
  longestWaiting,
  termsOf,
  weekRows,
  type WeekRow,
} from "../lib/weeks";

function Chevron({ open }: { open: boolean }) {
  return (
    <svg
      viewBox="0 0 16 16"
      width="16"
      height="16"
      aria-hidden="true"
      className={`shrink-0 text-(--ink-2) transition-transform ${open ? "rotate-90" : ""}`}
    >
      <path
        d="M6 3.5L10.5 8 6 12.5"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.5"
      />
    </svg>
  );
}

/** One week: its number, topic and lesson count, opening to its lessons. */
function Week({
  week,
  open,
  onToggle,
}: {
  week: WeekRow;
  open: boolean;
  onToggle: () => void;
}) {
  return (
    <li
      id={`week-${week.id}`}
      className="border-t border-(--line) first:border-t-0"
    >
      <button
        type="button"
        aria-expanded={open}
        onClick={onToggle}
        className="flex w-full items-center gap-4 px-4 py-3 text-left hover:bg-(--sunken)"
      >
        <span className="w-12 text-sm text-(--ink-2)">Wk {week.number}</span>
        <span className="flex flex-1 flex-wrap items-baseline gap-x-3 text-sm font-semibold text-(--ink)">
          {week.title}
          {week.waiting > 0 ? (
            <span
              role="img"
              aria-label={`${week.waiting} waiting`}
              title={`${week.waiting} waiting`}
              className="size-2 self-center rounded-full bg-(--accent)"
            />
          ) : null}
          {week.current ? (
            <span className="text-xs font-normal text-(--accent)">
              This week
            </span>
          ) : null}
        </span>
        {week.startsOn ? (
          <span className="text-xs text-(--ink-2)">{week.startsOn}</span>
        ) : null}
        <span className="text-xs text-(--ink-2)">
          {lessonCountText(week.lessons.length)}
        </span>
        <Chevron open={open} />
      </button>
      {open ? (
        <ul className="bg-(--sunken)">
          {week.lessons.map((lesson) => (
            <li key={lesson.id} className="border-t border-(--line)">
              <Link
                href={`/research/teacher/lessons/${lesson.id}`}
                className="flex items-center gap-4 py-2.5 pl-20 pr-4 hover:bg-(--line)/40"
              >
                <span className="flex min-w-0 flex-1 flex-col gap-0.5">
                  <span className="text-sm text-(--ink)">{lesson.title}</span>
                  {lesson.waiting ? (
                    <span className="flex items-center gap-2 text-xs text-(--ink-2)">
                      <span
                        aria-hidden="true"
                        className="size-2 shrink-0 rounded-full bg-(--accent)"
                      />
                      {lesson.waiting}
                    </span>
                  ) : null}
                </span>
                <Chevron open={false} />
              </Link>
            </li>
          ))}
        </ul>
      ) : null}
    </li>
  );
}

/** The class the teacher last used: its weeks and lessons, and what waits for them. */
export function ClassLandingPage() {
  const { workspaces, currentWorkspace, setWorkspace, isLoading } =
    useTeachingWorkspace();
  const scheme = useSchemeOfWork(currentWorkspace?.term_class_subject_id);
  const lessons = useWorkspaceLessons(currentWorkspace?.id ?? null);
  const { reviews } = useLessonReviews(currentWorkspace?.id ?? null);
  const packs = usePendingPacks();
  const [chosenWeek, setChosenWeek] = useState<string | null | undefined>(
    undefined,
  );

  if (isLoading) return null;
  if (!currentWorkspace) {
    return (
      <p className="px-8 py-6 text-sm text-(--ink-2)">
        You are not assigned to a class yet.
      </p>
    );
  }
  const weeks = weekRows(scheme.data, reviews);
  const waitingMost = longestWaiting(weeks, reviews, new Date());
  const toStart = waitingMost
    ? null
    : lessonToStart(
        weeks,
        new Set(lessons.todo.map((lesson) => lesson.lesson_period_id)),
        reviews,
      );
  const thisWeek = weeks.find((week) => week.current);
  const openWeek =
    chosenWeek === undefined ? (thisWeek?.id ?? null) : chosenWeek;
  const goToThisWeek = () => {
    if (!thisWeek) return;
    setChosenWeek(thisWeek.id);
    document
      .getElementById(`week-${thisWeek.id}`)
      ?.scrollIntoView({ block: "center" });
  };
  const terms = termsOf(workspaces, currentWorkspace);
  const nothingPlanned =
    lessons.lessons.length > 0 &&
    lessons.todo.length === lessons.lessons.length;

  const needs: NeedsItem[] =
    packs.packs.length > 0
      ? [
          {
            id: "notes",
            title: "Personalised notes",
            detail: `${packs.packs.length} to review`,
            actions: (
              <Link
                href="/research/teacher/pack-reviews"
                className={buttonClass({ variant: "secondary", size: "sm" })}
              >
                Review
              </Link>
            ),
          },
        ]
      : [];
  const panel = (
    <RightPanel
      needs={needs}
      agent={
        <p className="text-xs text-(--faint)">
          Each material has its own chat with the agent. Open a lesson to find
          them.
        </p>
      }
    />
  );

  return (
    <WorkspacePage panel={panel}>
      <div className="flex flex-col gap-5">
        <header className="flex flex-col gap-1">
          <h1 className="text-2xl font-semibold text-(--ink)">
            {[currentWorkspace.class_name, currentWorkspace.subject_name]
              .filter(Boolean)
              .join(" · ") || formatClassLabel(currentWorkspace)}
          </h1>
          <p className="text-xs text-(--ink-2)">
            {scheme.data?.current_week_number
              ? `Week ${scheme.data.current_week_number} of ${weeks.length}`
              : [
                  currentWorkspace.term,
                  weeks.length > 0 ? `${weeks.length} weeks` : null,
                ]
                  .filter(Boolean)
                  .join(" · ")}
          </p>
        </header>

        <div className="flex flex-wrap items-center gap-3">
          {terms.length > 1 ? (
            <select
              aria-label="Term"
              value={currentWorkspace.id}
              onChange={(event) => {
                const next = terms.find(
                  (term) => term.id === event.target.value,
                );
                if (next) setWorkspace(next);
              }}
              className="border border-(--line-2) bg-(--sunken) px-3 py-1.5 text-xs font-semibold text-(--ink)"
            >
              {terms.map((term) => (
                <option key={term.id} value={term.id}>
                  {term.term}
                </option>
              ))}
            </select>
          ) : null}
          {thisWeek ? (
            <button
              type="button"
              onClick={goToThisWeek}
              className={buttonClass({ variant: "secondary", size: "sm" })}
            >
              Go to this week
            </button>
          ) : null}
          {nothingPlanned ? (
            <p className="text-sm text-(--ink-2)">
              Open a week, then open a lesson to start planning.
            </p>
          ) : null}
        </div>

        {waitingMost ? (
          <section className="flex items-center gap-4 border border-(--line) bg-(--surface) px-4 py-3">
            <div className="flex flex-1 flex-col gap-0.5">
              <span className="text-sm font-semibold text-(--ink)">
                {waitingMost.title}
              </span>
              <span className="text-xs text-(--ink-2)">
                Waiting since {waitingMost.since}
              </span>
            </div>
            <Link
              href={`/research/teacher/lessons/${waitingMost.id}`}
              className={buttonClass({ variant: "primary", size: "sm" })}
            >
              {waitingMost.action}
            </Link>
          </section>
        ) : null}
        {toStart ? (
          <section className="flex items-center gap-4 border border-(--line) bg-(--surface) px-4 py-3">
            <div className="flex flex-1 flex-col gap-0.5">
              <span className="text-xs text-(--ink-2)">
                Start with · Wk {toStart.weekNumber}
              </span>
              <span className="text-sm font-semibold text-(--ink)">
                {toStart.title}
              </span>
            </div>
            <Link
              href={`/research/teacher/lessons/${toStart.id}`}
              className={buttonClass({ variant: "primary", size: "sm" })}
            >
              Start planning
            </Link>
          </section>
        ) : null}

        {scheme.isError ? (
          <p className="text-sm text-(--danger)">
            Couldn&apos;t load the weeks.
          </p>
        ) : null}
        {scheme.isLoading ? (
          <p className="text-sm text-(--ink-2)">Loading the weeks…</p>
        ) : null}
        {weeks.length > 0 ? (
          <div className="border border-(--line) bg-(--surface)">
            <div className="flex gap-4 bg-(--sunken) px-4 py-2 text-[11px] uppercase tracking-[0.12em] text-(--faint)">
              <span className="w-12">Week</span>
              <span>Topic</span>
            </div>
            <ul>
              {weeks.map((week) => (
                <Week
                  key={week.id}
                  week={week}
                  open={openWeek === week.id}
                  onToggle={() =>
                    setChosenWeek(openWeek === week.id ? null : week.id)
                  }
                />
              ))}
            </ul>
          </div>
        ) : null}
      </div>
    </WorkspacePage>
  );
}
