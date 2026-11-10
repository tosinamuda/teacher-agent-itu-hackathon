import { useMemo, useState, useEffect } from "react";
import { useSchemeOfWork } from "../hooks/useSchemeOfWork";
import { useCoursePlanStatuses } from "../hooks/useCoursePlanStatuses";
import { useTeachingWorkspace } from "@/features/teaching-workspace/context/TeachingWorkspaceContext";

import { lessonPeriodSubtitle } from "../lib/lessonPeriodLabels";

interface SyllabusBrowserProps {
  tcsId?: string;
  onSessionSelect: (session: {
    term: string;
    week: number;
    session_id: string; // lesson_period_id
    topic: string;
    subtopic_title: string;
    existingPlanId?: string;
  }) => void;
  selectedSessionId?: string;
  isEditable?: boolean;
  onEditWeek?: (weekId: string, title: string) => void;
  onAddDay?: (weekId: string, weekNumber: number) => void;
  onEditDay?: (day: {
    id: string;
    subtopic_title: string | null;
    period_number: number;
  }) => void;
  onDeleteDay?: (dayId: string) => void;
}

export const SyllabusBrowser = ({
  tcsId,
  onSessionSelect,
  selectedSessionId,
  isEditable = false,
  onEditWeek,
  onAddDay,
  onEditDay,
  onDeleteDay,
}: SyllabusBrowserProps) => {
  const { currentWorkspace, teacherId } = useTeachingWorkspace();
  const effectiveTcsId = tcsId || currentWorkspace?.term_class_subject_id;
  const { data: scheme, isLoading } = useSchemeOfWork(effectiveTcsId);
  const [expandedWeek, setExpandedWeek] = useState<number | null>(1); // Default to week 1

  const weeks = scheme?.weeks ?? [];

  // Fetch plan presence for this course/term
  const { data: planStatuses } = useCoursePlanStatuses({
    term: scheme?.term,
    teacherId: teacherId || undefined,
  });

  // Map session_id -> plan_id (latest version)
  const existingPlansMap = useMemo(() => {
    if (!planStatuses) return new Map<string, string>();
    const map = new Map<string, string>();
    for (const p of planStatuses) {
      if (p.session_id && !map.has(p.session_id)) {
        map.set(p.session_id, p.plan_id);
      }
    }
    return map;
  }, [planStatuses]);

  // Auto-expand the week containing the selected session
  useEffect(() => {
    if (scheme && selectedSessionId) {
      const weekForSession = scheme.weeks.find((week) =>
        week.lesson_periods.some((day) => day.id === selectedSessionId)
      );
      if (weekForSession && expandedWeek !== weekForSession.week_number) {
        setExpandedWeek(weekForSession.week_number);
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [scheme, selectedSessionId]);

  if (isLoading) {
    return (
      <div className="space-y-4 animate-pulse">
        {[1, 2, 3].map((i) => (
          <div key={i} className="h-20 bg-muted/20 rounded-xl" />
        ))}
      </div>
    );
  }

  if (!scheme || weeks.length === 0) {
    return (
      <div className="p-8 text-center border-2 border-dashed border-muted rounded-xl text-muted-foreground">
        No curriculum found for this course/term.
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="space-y-3 p-1">
        {weeks.map((week) => {
          const isExpanded = expandedWeek === week.week_number;
          const hasSelectedSession = week.lesson_periods.some(
            (d) => d.id === selectedSessionId
          );

          return (
            <div
              key={week.id}
              className={`rounded-xl border transition-all duration-300 overflow-hidden ${
                isExpanded || hasSelectedSession
                  ? "bg-white border-accent/20 ring-1 ring-accent/5"
                  : "bg-(--surface) border-transparent hover:border-border hover:bg-(--surface)"
              }`}
            >
              {/* Accordion Header */}
              <div
                className="w-full flex items-center justify-between p-4 text-left group/header cursor-pointer"
                onClick={(e) => {
                  // Prevent collapse if clicking edit button
                  if ((e.target as HTMLElement).closest(".edit-btn")) return;
                  setExpandedWeek(isExpanded ? null : week.week_number);
                }}
              >
                <div className="flex items-center gap-4 flex-1">
                  <div
                    className={`h-10 w-10 rounded-lg flex items-center justify-center text-sm font-bold border transition-colors ${
                      isExpanded
                        ? "bg-accent text-white border-accent"
                        : "bg-white text-muted-foreground border-border group-hover/header:border-accent/50 group-hover/header:text-accent"
                    }`}
                  >
                    W{week.week_number}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <h4
                        className={`font-medium text-sm truncate ${
                          isExpanded
                            ? "text-foreground"
                            : "text-muted-foreground"
                        }`}
                      >
                        {week.title}
                      </h4>
                      {isEditable && onEditWeek && (
                        <button
                          data-testid="week-edit-btn"
                          className="edit-btn opacity-0 group-hover/header:opacity-100 p-1 hover:bg-muted/50 rounded transition-opacity"
                          onClick={(e) => {
                            e.stopPropagation();
                            onEditWeek(week.id, week.title || "");
                          }}
                        >
                          <PencilIcon className="w-3.5 h-3.5 text-muted-foreground" />
                        </button>
                      )}
                    </div>
                    {!isExpanded && (
                      <p className="text-[10px] text-muted-foreground/70 truncate max-w-[200px]">
                        {week.lesson_periods.length} units:{" "}
                        {week.lesson_periods.map((d) => d.title || d.subtopic_title || d.subtopic_id).join(", ")}
                      </p>
                    )}
                  </div>
                </div>
                <div
                  className={`text-muted-foreground transition-transform duration-300 ml-2 ${
                    isExpanded ? "rotate-180" : ""
                  }`}
                >
                  <ChevronDownIcon className="size-4" />
                </div>
              </div>

              {/* Accordion Content */}
              {(isExpanded || hasSelectedSession) && (
                <div className="px-4 pb-4 space-y-1 animate-in slide-in-from-top-1 duration-200">
                  <div className="h-px w-full bg-linear-to-r from-transparent via-border to-transparent mb-3 opacity-50" />
                  {week.lesson_periods.map((day) => {
                    const isSelected = day.id === selectedSessionId;
                    const existingPlanId = existingPlansMap.get(day.id);
                    const hasPlan = !!existingPlanId;
                    const subtitle = lessonPeriodSubtitle(day);

                    // Don't show selection style if editable mode, just list
                    // Or keep selection style if we are still selecting?
                    // User might want to select to "Test" it, but editing is primary action?
                    // Let's keep selection behavior but add Floating Actions

                    return (
                      <div
                        key={day.id}
                        data-testid="session-item"
                        onClick={(e) => {
                          // Prevent selection if clicking actions
                          if ((e.target as HTMLElement).closest(".action-btn"))
                            return;

                          // If editing mode, clicking the body opens edit dialog? Or stays as selection?
                          // User said "click on syllabus map... will be to edit"
                          if (isEditable && onEditDay) {
                            onEditDay({
                              id: day.id,
                              subtopic_title: day.subtopic_title || "",
                              period_number: day.period_number,
                            });
                            return;
                          }

                          if (hasPlan) {
                            onSessionSelect({
                              term: scheme.term,
                              week: week.week_number,
                              session_id: day.id,
                              topic: week.title || "",
                              subtopic_title: day.subtopic_title || "",
                              existingPlanId: existingPlanId,
                            });
                          } else {
                            onSessionSelect({
                              term: scheme.term,
                              week: week.week_number,
                              session_id: day.id,
                              topic: week.title || "",
                              subtopic_title: day.subtopic_title || "",
                            });
                          }
                        }}
                        className={`group/item relative flex items-start gap-3 p-3 rounded-lg border cursor-pointer transition-all duration-200 ${
                          isSelected && !isEditable
                            ? "bg-(--accent-soft)/80 border-(--accent-soft)"
                            : "bg-transparent border-transparent hover:bg-muted/20 hover:border-border/50"
                        }`}
                      >
                        <div className="mt-1">
                          <div
                            className={`flex items-center justify-center w-4 h-4 rounded-none transition-colors ${
                              hasPlan && !isEditable
                                ? "bg-green-100 text-green-600"
                                : isSelected && !isEditable
                                ? "bg-accent"
                                : "bg-muted-foreground/30"
                            }`}
                          >
                            {hasPlan && !isEditable && (
                              <CheckIcon className="w-2.5 h-2.5" />
                            )}
                          </div>
                        </div>
                        <div className="flex-1 min-w-0 group-hover/item:pr-14 transition-all">
                          <div className="flex items-center gap-2">
                            <p
                              className={`text-sm font-medium truncate ${
                                isSelected && !isEditable
                                  ? "text-accent-deep"
                                  : "text-foreground"
                              }`}
                            >
                              {day.title || day.subtopic_title}
                            </p>
                          </div>
                          {subtitle ? (
                            <p className="text-xs text-muted-foreground line-clamp-1 mt-0.5">
                              {subtitle}
                            </p>
                          ) : null}
                        </div>

                        {/* Edit Actions */}
                        {isEditable && (
                          <div className="absolute right-2 top-2 opacity-0 group-hover/item:opacity-100 flex items-center gap-1 bg-(--surface) backdrop-blur rounded-md border p-0.5 transition-opacity">
                            {onEditDay && (
                              <button
                                className="action-btn p-1.5 hover:bg-muted rounded text-muted-foreground hover:text-foreground"
                                onClick={(e) => {
                                  e.stopPropagation();
                                  onEditDay({
                                    id: day.id,
                                    subtopic_title: day.subtopic_title,
                                    period_number: day.period_number,
                                  });
                                }}
                              >
                                <PencilIcon className="size-3" />
                              </button>
                            )}
                            {onDeleteDay && (
                              <button
                                className="action-btn p-1.5 hover:bg-red-50 rounded text-muted-foreground hover:text-red-600"
                                onClick={(e) => {
                                  e.stopPropagation();
                                  if (
                                    confirm(
                                      "Are you sure you want to delete this session?"
                                    )
                                  ) {
                                    onDeleteDay(day.id);
                                  }
                                }}
                              >
                                <TrashIcon className="size-3" />
                              </button>
                            )}
                          </div>
                        )}
                      </div>
                    );
                  })}

                  {/* Add Day Button */}
                  {isEditable && onAddDay && (
                    <button
                      className="w-full flex items-center justify-center gap-2 p-2 mt-2 text-xs font-medium text-muted-foreground border border-dashed rounded-lg hover:bg-muted/30 hover:text-foreground hover:border-border transition-colors group/add"
                      onClick={() => onAddDay(week.id, week.week_number)}
                    >
                      <PlusIcon className="size-3 group-hover/add:text-accent" />
                      Add Session to Week {week.week_number}
                    </button>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

// Simple Icons
const PencilIcon = ({ className }: { className?: string }) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    className={className}
  >
    <path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z" />
    <path d="m15 5 4 4" />
  </svg>
);

const TrashIcon = ({ className }: { className?: string }) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    className={className}
  >
    <path d="M3 6h18" />
    <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" />
    <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />
  </svg>
);

const PlusIcon = ({ className }: { className?: string }) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    className={className}
  >
    <path d="M5 12h14" />
    <path d="M12 5v14" />
  </svg>
);

const ChevronDownIcon = ({ className }: { className?: string }) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    className={className}
  >
    <path d="m6 9 6 6 6-6" />
  </svg>
);

const CheckIcon = ({ className }: { className?: string }) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    className={className}
  >
    <polyline points="20 6 9 17 4 12" />
  </svg>
);
