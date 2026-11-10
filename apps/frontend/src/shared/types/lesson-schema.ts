export type ContentBlockType =
  | "explanation"
  | "visual"
  | "worked_example"
  | "practice";

/** One action in a lesson-plan sequence, mirroring the backend `StepActivity`. */
export interface StepActivity {
  who: "teacher" | "student";
  what: string;
  /** A student activity only: whether it gives the students work of their own to do. */
  sets_work?: boolean;
}

export interface BaseContentBlock {
  type: ContentBlockType;
  id: string; // generated UUID for keying
}

export interface ExplanationBlock extends BaseContentBlock {
  type: "explanation";
  content: string; // Markdown supported
}

export interface VisualBlock extends BaseContentBlock {
  type: "visual";
  variant: "image" | "diagram_clock" | "diagram_number_line" | "diagram_tikz";
  caption?: string;
  /** A drawing the teacher made herself, as its TikZ source. */
  source_tikz?: string;
  data?: Record<string, unknown>; // For dynamic diagrams (e.g., { hour: 13, divisor: 12 })
  url?: string; // For static images
  source_record_id?: string;
  source_html_path?: string;
  source_anchor_id?: string;
}

export interface WorkedExampleBlock extends BaseContentBlock {
  type: "worked_example";
  problem: string;
  steps: {
    label: string;
    content: string; // Markdown
  }[];
  final_answer: string;
}

export interface PracticeBlock extends BaseContentBlock {
  type: "practice";
  question: string;
  answer: string;
  hints?: string[];
  lesson_objective_id?: string | null;
}

export type ContentBlock =
  | ExplanationBlock
  | VisualBlock
  | WorkedExampleBlock
  | PracticeBlock;

export interface LessonStepStructured {
  step_id: string;
  type: string;
  step_kind?: "intro" | "core" | "evaluation";
  /** The step's kind as the lesson-plan endpoint sends it. */
  step_role?: "intro" | "core" | "evaluation";
  instructional_type?:
    | "explain"
    | "example"
    | "practice"
    | "check"
    | "explain_only"
    | "explain_practice"
    | "explain_example_practice"
    | null;
  kc_type?: "concept" | "procedure" | "representation" | null;
  lesson_objective_id?: string | null;
  title: string;
  duration_minutes?: number;
  estimated_minutes?: number;
  /** Teacher-facing narrative/summary for the step (Markdown + LaTeX). Steps without
   * content blocks (e.g. intro/conclusion) carry their material here. */
  content?: string;
  blocks?: ContentBlock[];
  /** What happens in this step, in the order it runs. */
  activities?: StepActivity[];
}
