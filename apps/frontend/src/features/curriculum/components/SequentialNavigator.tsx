import { useState, useMemo } from "react";
import { useSchemeOfWork } from "../hooks/useSchemeOfWork";
import { Card } from "@/shared/components/ui/Card";
import { Select } from "@/shared/components/ui/Form";

interface SequentialNavigatorProps {
  tcsId?: string;
  onSessionSelect: (session: {
    term: string;
    week: number;
    session_id: string; // lesson_period_id
    topic: string;
    subtopic_title: string;
  }) => void;
}

export const SequentialNavigator = ({
  tcsId,
  onSessionSelect,
}: SequentialNavigatorProps) => {
  const [week, setWeek] = useState<number>(1);

  // Data Fetching
  const { data: scheme, isLoading } = useSchemeOfWork(tcsId);
  const term = scheme?.term ?? "";

  // Derived State
  const currentWeek = useMemo(() => {
    if (!scheme) return null;
    return scheme.weeks.find((w) => w.week_number === week);
  }, [scheme, week]);

  const objectives = useMemo(() => {
    if (!currentWeek?.objectives) return [];
    // Handle dict or list - seed data was dict {"goals": []}
    const goals = currentWeek.objectives["goals"];
    if (Array.isArray(goals)) return goals as string[];
    return [];
  }, [currentWeek]);

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Navigation Controls */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Select
          label="Week"
          value={week.toString()}
          onChange={(e) => setWeek(parseInt(e.target.value))}
        >
          {Array.from({ length: 12 }, (_, i) => (
            <option key={i + 1} value={i + 1}>
              Week {i + 1}
            </option>
          ))}
        </Select>
      </div>

      {/* Topic Display */}
      <Card className="p-6 bg-(--surface) backdrop-blur-sm border-(--line)">
        {isLoading ? (
          <div className="h-16 flex items-center justify-center text-(--muted)">
            Loading scheme...
          </div>
        ) : currentWeek ? (
          <div>
            <h3 className="text-lg font-semibold text-(--ink) mb-2">
              {currentWeek.title}
            </h3>
            <div className="flex flex-wrap gap-2 mb-4">
              {objectives.slice(0, 3).map((obj, i) => (
                <span
                  key={i}
                  className="px-2 py-1 bg-(--accent-soft) text-(--accent-deep) text-xs rounded-none"
                >
                  {obj.length > 60 ? obj.slice(0, 60) + "..." : obj}
                </span>
              ))}
            </div>
          </div>
        ) : (
          <div className="text-(--muted) italic">
            No topic found for this week in {term}.
          </div>
        )}
      </Card>

      {/* Session Selection */}
      <div className="space-y-3">
        <h4 className="font-medium text-(--muted) uppercase text-xs tracking-wider">
          Available Sessions
        </h4>
        {isLoading ? (
          <div className="space-y-2">
            {[1, 2].map((i) => (
              <div
                key={i}
                className="h-16 bg-(--surface) rounded-xl animate-pulse"
              />
            ))}
          </div>
        ) : currentWeek && currentWeek.lesson_periods.length > 0 ? (
          <div className="grid gap-3">
            {currentWeek.lesson_periods.map((day) => (
              <button
                key={day.id}
                type="button"
                onClick={() =>
                  onSessionSelect({
                    term: term,
                    week: week,
                    session_id: day.id,
                    topic: currentWeek.title || "",
                    subtopic_title: day.subtopic_title || "",
                  })
                }
                className="group relative flex items-start p-4 text-left bg-white border border-transparent rounded-xl hover:border-(--accent) transition-all duration-200"
              >
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-(--sunken) text-(--ink-2) uppercase">
                      Period {day.period_number}
                    </span>
                    <span className="text-xs font-medium text-(--accent)">
                      {day.title || day.subtopic_title || "Unassigned"}
                    </span>
                  </div>
                </div>
                <div className="ml-4 opacity-0 group-hover:opacity-100 transition-opacity self-center text-(--accent)">
                  <svg
                    className="w-5 h-5"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 5l7 7-7 7"
                    />
                  </svg>
                </div>
              </button>
            ))}
          </div>
        ) : (
          <div className="text-sm text-(--muted) text-center py-8">
            No sessions available for this selection.
          </div>
        )}
      </div>
    </div>
  );
};
