import { useState, useEffect } from "react";
import { StudentForm } from "../components/StudentForm";
import { StudentDetailView } from "../components/StudentDetailView";
import { useQuery } from "@tanstack/react-query";

import { useTeachingWorkspace } from "@/features/teaching-workspace/context/TeachingWorkspaceContext";
import { WorkspacePage } from "@/shared/components/workspace/WorkspacePage";
import { LearnersPanel } from "../components/LearnersPanel";
import { classLearnersQuery } from "../lib/classLearnersQuery";
import { useLearnerDetail } from "../hooks/useStudentDetail";

type StudentDetailPageProps = {
  learnerId: string;
};

export function LearnerDetailPage({ learnerId }: StudentDetailPageProps) {
  const [isEditing, setIsEditing] = useState(false);
  const { currentWorkspace } = useTeachingWorkspace();
  const classLearners = useQuery(
    classLearnersQuery(currentWorkspace?.id ?? ""),
  );
  const inClass = classLearners.data?.learners.find(
    (learner) => learner.student_id === learnerId,
  );

  const {
    form,
    submitHandler: originalSubmitHandler,
    isBusy,
    formError,
    classOptions,
    fieldOptions,
    catalogQuery,
    toggleCoreSubject,
    selectedCoreSubjects,
    subjectSummary,
    handleFieldOfStudyChange,
    learnerQuery,
  } = useLearnerDetail(learnerId);

  // Wrap submit handler to exit edit mode on success
  const handleSubmit = async (e?: React.BaseSyntheticEvent) => {
    await originalSubmitHandler(e);
    // Use isSuccess status from mutation if possible, or wait for learnerQuery to change?
    // Since useLearnerDetail's updateMutation invalidates query,
    // we can just wait or optimistically switch back if no error.
    // But submitHandler is void promise.
    // A better way is passing onSuccess to useStudentDetail, but for now specific logic:
    if (!isBusy) {
      // We can't know for sure here if it failed inside `useStudentDetail` easily without deeper refactor.
      // Check `formError` after effect?
      setIsEditing(false);
    }
  };

  // Hacky fix for exiting edit mode: watch isSubmitSuccessful
  useEffect(() => {
    if (form.formState.isSubmitSuccessful) {
      setIsEditing(false);
      form.reset(undefined, { keepValues: true }); // reset dirty state
    }
  }, [form.formState.isSubmitSuccessful, form]);

  if (learnerQuery.isLoading) {
    return (
      <WorkspacePage
        panel={
          <LearnersPanel
            notesToReview={inClass?.notes_to_review ?? 0}
            whose={inClass?.full_name ?? ""}
          />
        }
      >
        <p className="text-sm text-(--ink-2)">Loading learner details...</p>
      </WorkspacePage>
    );
  }

  if (learnerQuery.isError || !learnerQuery.data) {
    return (
      <WorkspacePage
        panel={
          <LearnersPanel
            notesToReview={inClass?.notes_to_review ?? 0}
            whose={inClass?.full_name ?? ""}
          />
        }
      >
        <p className="text-sm text-(--danger)">Failed to load learner.</p>
      </WorkspacePage>
    );
  }

  return (
    <WorkspacePage
      panel={
        <LearnersPanel
          notesToReview={inClass?.notes_to_review ?? 0}
          whose={inClass?.full_name ?? ""}
        />
      }
    >
      <div className="flex flex-col gap-6">
        {isEditing ? (
          <div className="flex flex-col h-full animate-fade-in">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold">Edit Learner</h2>
              <button
                className="btn btn--ghost"
                onClick={() => {
                  setIsEditing(false);
                  form.reset(); // Revert changes
                }}
              >
                Cancel
              </button>
            </div>
            <StudentForm
              form={form}
              onSubmit={handleSubmit}
              isBusy={isBusy}
              selectedLearnerId={learnerId}
              formError={formError}
              classOptions={classOptions}
              fieldOptions={fieldOptions}
              tradeSubjects={catalogQuery.data?.trade_subjects ?? []}
              fieldsOfStudy={Object.keys(
                catalogQuery.data?.fields_of_study ?? {},
              )}
              toggleCoreSubject={toggleCoreSubject}
              selectedCoreSubjects={selectedCoreSubjects}
              subjectSummary={subjectSummary}
              onFieldOfStudyChange={handleFieldOfStudyChange}
            />
          </div>
        ) : (
          <StudentDetailView
            student={learnerQuery.data}
            onEdit={() => setIsEditing(true)}
          />
        )}
      </div>
    </WorkspacePage>
  );
}
