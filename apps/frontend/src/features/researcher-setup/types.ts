/** Researcher-facing school record. */
export type ResearchSchool = {
  id: string;
  name: string;
  school_code: string;
  default_academic_year?: string | null;
  current_term?: string | null;
  class_count: number;
  workspace_count: number;
  created_at?: string | null;
};

/** URL-backed tabs for selected-school setup. */
export type SchoolSetupTab = "details" | "classes" | "learners";

/** Grade option for setup forms. */
export type GradeLevelOption = {
  id: string;
  name: string;
};

/** Subject option for setup forms. */
export type SubjectOption = {
  id: string;
  name: string;
  code: string;
};

/** Teacher option for setup forms. */
export type TeacherOption = {
  id: string;
  full_name?: string | null;
  auth_id: string;
  email: string;
};

/** Shared setup catalog payload. */
export type SchoolSetupCatalog = {
  grade_levels: GradeLevelOption[];
  subjects: SubjectOption[];
  teachers: TeacherOption[];
  academic_years: string[];
  suggested_terms: string[];
};

/** Researcher-facing workspace setup record. */
export type SchoolSetupWorkspace = {
  workspace_id: string;
  term_class_subject_id: string;
  school_id: string;
  school_name: string;
  school_code: string;
  class_id: string;
  class_name: string;
  grade_level: string;
  subject_name: string;
  subject_code: string;
  term: string;
  academic_year: string;
  teacher_id: string;
  teacher_name?: string | null;
  workspace_name: string;
  is_primary: boolean;
  created_at?: string | null;
};

/** Class record returned by the school API. */
export type SchoolClass = {
  id: string;
  name: string;
  grade?: string | null;
  school_id?: string | null;
  school_name?: string | null;
  school_code?: string | null;
};

/** School creation payload. */
export type CreateSchoolRequest = {
  name: string;
  school_code: string;
  default_academic_year?: string;
  current_term?: string;
};

/** School update payload for the selected-school details tab. */
export type UpdateSchoolRequest = CreateSchoolRequest;

/** Workspace creation payload. */
export type CreateSchoolWorkspaceRequest = {
  school_id: string;
  class_name: string;
  grade_level_name: string;
  subject_code: string;
  term: string;
  academic_year: string;
  teacher_id: string;
  is_primary?: boolean;
};

/** Basic learner creation payload used during onboarding. */
export type CreateResearchLearnerRequest = {
  code: string;
  full_name: string;
  class_id: string;
  grade: string;
  track: string;
};

/** Lightweight learner row used in the researcher setup learner tab. */
export type ResearchLearner = {
  student_id: string;
  code?: string | null;
  full_name: string;
  grade: string;
  track: string;
  class_id?: string | null;
  class_name?: string | null;
  created_at?: string | null;
};

/** Paginated learner response used by the researcher setup learner tab. */
export type ResearchLearnerList = {
  data: ResearchLearner[];
  total: number;
  page: number;
  page_size: number;
};

/** Suggests a school code from the current school name. */
export const suggestSchoolCode = (value: string) =>
  value
    .toUpperCase()
    .replace(/[^A-Z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 32);

/** Normalizes the active selected-school tab from the URL query string. */
export const resolveSchoolSetupTab = (value: string | null | undefined): SchoolSetupTab => {
  if (value === "classes" || value === "learners") {
    return value;
  }
  return "details";
};
