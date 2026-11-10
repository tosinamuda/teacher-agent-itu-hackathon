export interface TeachingWorkspace {
  id: string;
  course_id: string;
  term_class_subject_id: string;
  class_id?: string | null;
  class_name?: string | null;
  school_id?: string | null;
  school_name?: string | null;
  name: string;
  subject_name: string;
  subject_code?: string;
  grade_level: string;
  term?: string;
  is_primary: boolean;
  teacher_id: string;
  settings?: Record<string, unknown>;
  created_at?: string;
}
