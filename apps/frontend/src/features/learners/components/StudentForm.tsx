import { UseFormReturn } from "react-hook-form";
import { LearnerFormState } from "../types";

type StudentFormProps = {
  form: UseFormReturn<LearnerFormState>;
  onSubmit: (e?: React.BaseSyntheticEvent) => Promise<void>;
  isBusy: boolean;
  selectedLearnerId: string | null;
  formError: string | null;
  classOptions: { value: string; label: string }[];
  fieldOptions: string[];
  tradeSubjects: string[];
  fieldsOfStudy: string[]; // keys
  toggleCoreSubject: (subject: string) => void;
  selectedCoreSubjects: string[];
  subjectSummary: string[];
  // Handlers for dynamic field updates
  onFieldOfStudyChange: (field: string) => void;
};

export function StudentForm({
  form,
  onSubmit,
  isBusy,
  selectedLearnerId,
  formError,
  classOptions,
  fieldOptions,
  tradeSubjects,
  fieldsOfStudy,
  toggleCoreSubject,
  selectedCoreSubjects,
  subjectSummary,
  onFieldOfStudyChange,
}: StudentFormProps) {
  "use no memo"; // react-hook-form 7 fills a registered input only when register() runs again on render.
  return (
    <div className="panel animate-fade-up delay-2 h-full flex flex-col">
      <div className="panel__title shrink-0">
        <h2>{selectedLearnerId ? "Edit Learner" : "Create Learner"}</h2>
        <span>Capture subject slots and learning preferences for Phase 3.</span>
      </div>

      <form onSubmit={onSubmit} className="flex-1 overflow-y-auto px-1">
        <div className="space-y-6">
          {/* Section: Basic Identity */}
          <div className="bg-(--sunken)/50 p-4 rounded-lg">
            <h3 className="text-sm font-semibold mb-3 text-(--ink-2)">
              Identity
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="field">
                <label>Learner ID (Code)</label>
                <div className="relative">
                  <input
                    {...form.register("code")}
                    readOnly
                    className="bg-(--sunken) cursor-not-allowed text-muted-foreground"
                  />
                  {!selectedLearnerId && (
                    <p className="text-[10px] text-muted-foreground mt-1 absolute right-2 top-2">
                      Auto-generated
                    </p>
                  )}
                </div>
              </div>
              <div className="field">
                <label>Full name</label>
                <input {...form.register("full_name")} />
              </div>
            </div>
          </div>

          {/* Section: Academic Classification */}
          <div className="bg-(--sunken)/50 p-4 rounded-lg">
            <h3 className="text-sm font-semibold mb-3 text-(--ink-2)">
              Academic Classification
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="field">
                <label>Grade</label>
                <input {...form.register("grade")} />
              </div>
              <div className="field">
                <label>Track</label>
                <input {...form.register("track")} />
              </div>
              <div className="field">
                <label>Class</label>
                <select {...form.register("class_id")}>
                  <option value="">Select class</option>
                  {classOptions.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Section: Subject Selection */}
          <div className="bg-(--sunken)/50 p-4 rounded-lg">
            <h3 className="text-sm font-semibold mb-3 text-(--ink-2)">
              Subject Selection
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div className="field">
                <label>Field of study</label>
                <select
                  {...form.register("field_of_study")}
                  onChange={(e) => onFieldOfStudyChange(e.target.value)}
                >
                  <option value="">Select field</option>
                  {fieldsOfStudy.map((field) => (
                    <option key={field} value={field}>
                      {field}
                    </option>
                  ))}
                </select>
              </div>
              <div className="field">
                <label>Trade subject</label>
                <select {...form.register("trade_subject")}>
                  <option value="">Select trade</option>
                  {tradeSubjects.map((subject) => (
                    <option key={subject} value={subject}>
                      {subject}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="field">
              <label>Field core subjects (pick 3)</label>
              <div className="chip-grid">
                {fieldOptions.length === 0 && (
                  <p className="hint">
                    Choose a field of study to see options.
                  </p>
                )}
                {fieldOptions.map((subject) => (
                  <button
                    key={subject}
                    type="button"
                    className={`chip ${
                      selectedCoreSubjects.includes(subject) ? "active" : ""
                    }`}
                    onClick={() => toggleCoreSubject(subject)}
                  >
                    {subject}
                  </button>
                ))}
              </div>
            </div>

            {/* Subject Mix Summary */}
            <div className="meta-card mt-4">
              <span>Subject mix</span>
              <strong>
                {subjectSummary.length
                  ? subjectSummary.join(" · ")
                  : "No subjects selected"}
              </strong>
            </div>
          </div>

          {/* Section: Personalization */}
          <div className="bg-(--sunken)/50 p-4 rounded-lg">
            <h3 className="text-sm font-semibold mb-3 text-(--ink-2)">
              Learning Personalization
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="field">
                <label>Language level</label>
                <select {...form.register("language_level")}>
                  <option value="">Default</option>
                  <option value="simple">Simple</option>
                  <option value="standard">Standard</option>
                  <option value="advanced">Advanced</option>
                </select>
              </div>
              <div className="field">
                <label>Pace</label>
                <select {...form.register("pace_preference")}>
                  <option value="">Default</option>
                  <option value="slow">Slow</option>
                  <option value="standard">Standard</option>
                  <option value="fast">Fast</option>
                </select>
              </div>
              <div className="field">
                <label>Time budget (mins)</label>
                <input
                  type="number"
                  {...form.register("time_budget_minutes")}
                />
              </div>
            </div>
          </div>

          {formError && <p className="hint error">{formError}</p>}
        </div>

        <div className="sticky bottom-0 bg-surface py-4 mt-6 border-t border-line">
          <div className="output__actions">
            <button
              className="btn btn--primary w-full md:w-auto"
              type="submit"
              disabled={isBusy}
            >
              {isBusy
                ? "Saving..."
                : selectedLearnerId
                  ? "Save Changes"
                  : "Create Learner"}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}
