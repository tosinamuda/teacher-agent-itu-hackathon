import { StudentForm } from "../components/StudentForm";
import { useLearnerDetail } from "../hooks/useStudentDetail";

export function NewLearnerPage() {
  const {
    form,
    submitHandler,
    isBusy,
    formError,
    classOptions,
    fieldOptions,
    catalogQuery,
    toggleCoreSubject,
    selectedCoreSubjects,
    subjectSummary,
    handleFieldOfStudyChange,
  } = useLearnerDetail(); // No ID

  return (
    <div className="page student-new p-6 max-w-4xl mx-auto w-full h-full">
      <StudentForm
        form={form}
        onSubmit={submitHandler}
        isBusy={isBusy}
        selectedLearnerId={null}
        formError={formError}
        classOptions={classOptions}
        fieldOptions={fieldOptions}
        tradeSubjects={catalogQuery.data?.trade_subjects ?? []}
        fieldsOfStudy={Object.keys(catalogQuery.data?.fields_of_study ?? {})}
        toggleCoreSubject={toggleCoreSubject}
        selectedCoreSubjects={selectedCoreSubjects}
        subjectSummary={subjectSummary}
        onFieldOfStudyChange={handleFieldOfStudyChange}
      />
    </div>
  );
}
