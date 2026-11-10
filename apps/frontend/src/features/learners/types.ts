export type SubjectOfferingCatalog = {
  curriculum?: string | null;
  subject_slots: {
    total_subjects: number;
    compulsory_subjects: number;
    field_core_subjects: number;
    trade_subjects: number;
    notes?: string[];
  };
  core_compulsory_subjects: string[];
  fields_of_study: Record<string, string[]>;
  trade_subjects: string[];
};

export type LearnerProfile = {
  student_id: string;
  code?: string;
  full_name: string;
  grade: string;
  track: string;
  class_id?: string | null;
  class_name?: string | null;
  field_of_study?: string | null;
  trade_subject?: string | null;
  field_core_subjects?: string[] | null;
  language_level?: string | null;
  pace_preference?: string | null;
  time_budget_minutes?: number | null;
};

export type ClassResponse = {
  id: string;
  name: string;
  grade?: string;
};

export type ResearchSchoolOption = {
  id: string;
  name: string;
  school_code: string;
};

export type ResearchWorkspaceOption = {
  teacher_workspace_id: string;
  school_id: string;
  class_id: string;
  class_name: string;
  subject_name: string;
  grade_level: string;
  term: string;
  academic_year: string;
  workspace_name: string;
};

export type ResearchLearnerExperimentContext = {
  experiment_id: string;
  experiment_code: string;
  lesson_title?: string | null;
  school_id?: string | null;
  class_id?: string | null;
  teacher_workspace_id?: string | null;
};

export type PaginatedLearnerResponse = {
  data: LearnerProfile[];
  total: number;
  page: number;
  page_size: number;
};

export type LearnerFormState = {
  student_id: string;
  code: string;
  full_name: string;
  grade: string;
  track: string;
  class_id: string;
  field_of_study: string;
  trade_subject: string;
  field_core_subjects: string[];
  language_level: string;
  pace_preference: string;
  time_budget_minutes: string;
};

/** How a teacher's class test places a learner: by their weakest objective. */
export type ClassBand = "remediate" | "reinforce" | "extend";

export type ClassLearner = {
  student_id: string;
  full_name: string;
  last_test: {
    lesson_title: string;
    band: ClassBand;
    /** Null when the test was recorded without counts. */
    correct: number | null;
    out_of: number | null;
    taken_at: string;
  } | null;
  /** The learner's personalised notes waiting for the teacher, and those already approved. */
  notes_to_review: number;
  notes_approved: number;
};

export type ClassLearnersResponse = { learners: ClassLearner[] };

export type LearnerTest = {
  lesson_period_id: string;
  lesson_title: string;
  band: ClassBand;
  correct: number | null;
  out_of: number | null;
  taken_at: string;
  /** Who entered the results when the learner did not answer themselves. */
  entered_by?: string | null;
};

export type LearnerObjectiveResult = {
  objective_text: string;
  lesson_period_id: string;
  lesson_title: string;
  band: ClassBand;
  correct: number | null;
  out_of: number | null;
};

/** One learner's class tests for a class's subject, and how they did on each objective. */
export type LearnerResults = {
  student_id: string;
  full_name: string;
  /** Newest first. */
  tests: LearnerTest[];
  /** Weakest first. */
  objectives: LearnerObjectiveResult[];
  /** Every lesson with a plan: those with a test newest first, then the rest as taught. */
  lessons: LearnerLesson[];
};

export type RevisionNoteStatus = "to_review" | "approved" | "waiting_for_test" | "not_made";

export type LearnerLesson = {
  lesson_period_id: string;
  lesson_title: string;
  correct: number | null;
  out_of: number | null;
  band: ClassBand | null;
  revision_note: RevisionNoteStatus;
  revision_note_id: string | null;
};
