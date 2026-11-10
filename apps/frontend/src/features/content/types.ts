/** A content type, as the API names it: a built-in type, or any type registered since. */
export type ContentTypeSlug = string;

/** How content of a type is built: its own generator, or the content engine over MCP. */
export type Engine = "builtin" | "mcp";

/** What one part of drafted content covers. */
export type Unit =
  "lesson" | "curriculum_objective" | "lesson_objective" | "plan_step";

/** One shape an item of a mixed list may take, named by the item's `kind`. */
export type PartKind = {
  name: string;
  description: string;
  fields: PartField[];
};

/**
 * One field of a part. A `group` holds one object with `fields`; an `items` field lists
 * objects with `fields`, or with the fields of one of its `kinds` each.
 */
export type PartField = {
  name: string;
  description: string;
  type:
    | "text"
    | "markdown"
    | "tikz"
    | "maths"
    | "whole_number"
    | "yes_no"
    | "list"
    | "group"
    | "items";
  required: boolean;
  fields?: PartField[];
  kinds?: PartKind[];
  options?: string[];
  min_items?: number;
};

export type Level = "class" | "learner";

/** One revision of a type's spec: what content of the type is and must do. */
export type Spec = {
  revision: number;
  material: string;
  audience: string;
  levels: Level[];
  structure: string[];
  requirements: string[];
  adaptable: string[];
  /** Set for a type drafted part by part: what one part covers, and the fields of a part. */
  unit: Unit | null;
  parts: PartField[] | null;
  /** The fields of the part written once for the whole lesson, when there is one. */
  lesson_parts: PartField[] | null;
  /** The skills its content is written with, each pinned at a revision. */
  skills: { skill: string; revision: number }[];
};

/** Teaching content is for the teacher; learning material is for learners. */
export type Audience = "teacher" | "learner";

/** One way of making a type's content; the default is what new content is made with. */
export type GeneratorInfo = {
  level: Level;
  /** What drives the model: a DSPy program (`dspy-pipeline`) or the content engine (`engine`). */
  harness: "dspy-pipeline" | "engine";
  /** Where the content's schema lives: written in the program, or read from a spec. */
  schema_source: "code" | "spec";
  /** A pipeline name such as `2026-09-02`, or the plugin that holds the spec. */
  ref: string;
  status: "default" | "available" | "retired";
  spec_revision: number | null;
};

export type ContentTypeInfo = {
  type: ContentTypeSlug;
  /** What a person calls it. */
  label: string;
  audience: Audience;
  engine: Engine;
  /** Whether a frozen plan version generates it; a lesson plan is made from its lesson. */
  made_from_a_plan_version: boolean;
  spec: Spec;
  /** Its plugin was removed: the content made stays readable, and nothing new is generated. */
  retired: boolean;
  generators: GeneratorInfo[];
};

export type ReviewStatus = "pending" | "approved" | "rejected";

export type ContentSummary = {
  id: string;
  type: ContentTypeSlug;
  level: Level;
  plan_version_id: string;
  student_id: string | null;
  /** Echoed back on approval; an approval of an older version is refused. */
  version: number;
  review_status: ReviewStatus;
  /** Why the teacher rejected it or withdrew it. */
  review_reason: string | null;
  created_at: string | null;
  /** Its lesson's study has concluded: it can be read, never changed. */
  read_only: boolean;
  /** Where it came from, and the spec revision, pipeline and sources it was generated with. */
  provenance: {
    origin?: Origin;
    specification?: { kind: string; revision: number };
    pipeline?: string;
    /** The generator that made it: its harness, schema source and ref. */
    generator?: {
      harness: string;
      schema: string;
      ref: string;
      spec_revision?: number;
    };
    expert_sources?: ExpertSources;
    lesson_note?: { id: string; version: number; origin: Origin | null } | null;
  };
};

export type ReviewedCheck = {
  check: string;
  passed: boolean;
  message: string | null;
};

export type CitedPassage = {
  source_ref: string;
  title: string | null;
  excerpt: string;
};

/** The checks a version passed and the passages it was given, as recorded when it was written. */
export type ReviewRecord = {
  version: number;
  checks: ReviewedCheck[];
  passages: CitedPassage[];
};

export type ContentItem = ContentSummary & {
  content: Record<string, unknown>;
  review: ReviewRecord | null;
  /** Its type's plugin makes it into a file, which can be downloaded. */
  has_file: boolean;
};

export type Revision = {
  turn_number: number;
  feedback: string;
  summary: string | null;
  created_at: string;
};

export type Approval = {
  id: string;
  approved_version: number;
  approved_by: string | null;
  approved_at: string;
};

/** One thing the chat showed while content was made: a message, the agent's text, or a tool call. */

/** Where a piece of content came from. */
export type Origin = "teacher" | "study_record" | "generated";

/** The expert content a revision note is grounded in. */
export type ExpertSources = "lesson-note" | "textbook" | "both";

/** The note for one plan step, as markdown. */
export type NoteSection = { step_id: string; body: string };

export type LessonNoteManifest = {
  artefact_type: "lesson_note";
  plan_version_id: string;
  sections: NoteSection[];
};

/** Engine-built content: one checked part per unit, in the lesson's order. */
export type EngineManifest = {
  content_type: ContentTypeSlug;
  plan_version_id: string;
  unit: Unit;
  sections: EngineSection[];
  /** A slide deck's cover, set by the app when it saved the deck; older decks have none. */
  cover?: { title: string; subtitle: string; objectives: string[] };
};

export type EngineSection = {
  unit_id: string;
  /** Which kind of unit the section is for; content stored before it was recorded has none. */
  unit?: Unit;
  label: string;
  part: Record<string, unknown>;
};
