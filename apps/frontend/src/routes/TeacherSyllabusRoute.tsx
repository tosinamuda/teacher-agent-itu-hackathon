import { useState } from "react";

import { SyllabusBrowser } from "@/features/curriculum/components/SyllabusBrowser";
import {
  EditWeekModal,
  EditDayModal,
} from "@/features/curriculum/components/SyllabusEditDialogs";
import { useSyllabusMutations } from "@/features/curriculum/hooks/useSyllabusMutations";
import { useTeachingWorkspace } from "@/features/teaching-workspace/context/TeachingWorkspaceContext";
import { formatTeachingWorkspaceLabel } from "@/features/teaching-workspace/lib/labels";

/** `/research/teacher/syllabus` — moved verbatim from the Next page module
 *  (route-layer component: it composes across features, which feature modules
 *  themselves must not do). */
export function TeacherSyllabusRoute() {
  const { currentWorkspace } = useTeachingWorkspace();
  const { deleteDay } = useSyllabusMutations();

  // Edit State
  const [editState, setEditState] = useState<
    | { type: "IDLE" }
    | { type: "WEEK"; weekId: string; currentTopic: string }
    | { type: "ADD_DAY"; weekId: string }
    | {
        type: "EDIT_DAY";
        day: {
          id: string;
          subtopic_title: string | null;
          period_number: number;
        };
      }
  >({ type: "IDLE" });

  return (
    <div className="flex flex-col h-full bg-(--sunken)/50">
      {/* Header */}
      <header className="px-8 py-6 bg-white border-b border-border">
        <div className="max-w-5xl mx-auto">
          <h1 className="text-2xl font-display font-medium text-(--ink)">
            Syllabus Management
          </h1>
          <p className="text-muted-foreground mt-1">
            Manage your course curriculum, weeks, and lesson sessions.
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto p-8">
        <div className="max-w-5xl mx-auto">
          <div className="bg-white rounded-xl border border-border p-6">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-lg font-medium text-(--ink)">
                  {currentWorkspace
                    ? `Curriculum: ${formatTeachingWorkspaceLabel(currentWorkspace)}`
                    : "Course Curriculum"}
                </h2>
                {currentWorkspace?.term && (
                  <span className="text-sm text-muted-foreground">
                    {currentWorkspace.term}
                  </span>
                )}
              </div>
            </div>

            <SyllabusBrowser
              isEditable={true}
              onEditWeek={(weekId, topic) =>
                setEditState({ type: "WEEK", weekId, currentTopic: topic })
              }
              onAddDay={(weekId) => setEditState({ type: "ADD_DAY", weekId })}
              onEditDay={(day) => setEditState({ type: "EDIT_DAY", day })}
              onDeleteDay={(dayId) => deleteDay.mutate(dayId)}
              onSessionSelect={() => {}} // No-op for management page
            />
          </div>
        </div>
      </main>

      {/* Modals */}
      <EditWeekModal
        isOpen={editState.type === "WEEK"}
        onClose={() => setEditState({ type: "IDLE" })}
        weekId={editState.type === "WEEK" ? editState.weekId : ""}
        currentTopic={editState.type === "WEEK" ? editState.currentTopic : ""}
      />

      <EditDayModal
        isOpen={editState.type === "ADD_DAY" || editState.type === "EDIT_DAY"}
        onClose={() => setEditState({ type: "IDLE" })}
        mode={editState.type === "ADD_DAY" ? "ADD" : "EDIT"}
        weekId={editState.type === "ADD_DAY" ? editState.weekId : undefined}
        day={editState.type === "EDIT_DAY" ? editState.day : undefined}
      />
    </div>
  );
}
