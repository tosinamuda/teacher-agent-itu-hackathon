/** Part 1: a rater's 1–5 on one criterion for one of the note's objectives. */
export type CriterionScore = {
  rater: string;
  packet: string;
  objective_index: number;
  lesson_objective_id: string;
  /** The objective as the lesson plan words it, which the scoring page named. */
  objective_text: string | null;
  criterion_id: string;
  score: number;
  comment: string | null;
};

/** Part 2: a rater's choice between this note and the learner's other one. */
export type ComparativeJudgement = {
  rater: string;
  packet: string;
  shown_as: "A" | "B";
  other_note_id: string;
  /** The objective's number among those the set compared, not in the lesson. */
  objective_index: number;
  lesson_objective_id: string | null;
  objective_text: string | null;
  criterion_id: string;
  choice: string;
  favoured_condition: string | null;
  comment: string | null;
};

/** A returned rating document that rated the note: when, and the rater's closing comment. */
export type RatingDocument = {
  rater: string;
  /** The rater's profile, e.g. "Study rater 2". */
  rater_name: string;
  packet: string;
  shown_as: "A" | "B" | null;
  /** How much of the set came back answered. */
  state: "complete" | "partial" | "untouched";
  marks: number;
  rows_unanswered: number;
  date_completed: string | null;
  closing_comment: string | null;
};

/** One rating document a study rater returned for a lesson, and the note or learner it rated. */
export type RatedSet = {
  /** 1 scored one class note; 2 compared one learner's two notes. */
  part: 1 | 2;
  rater: string;
  rater_name: string;
  packet: string;
  /** Where the set sat in the rater's pile, from 1. */
  delivery_order: number;
  /** The note the set rated, or in Part 2 the note shown as A. */
  note_id: string;
  condition: string | null;
  draw: number | null;
  /** The learner's other note, shown as B, for Part 2. */
  other_note_id: string | null;
  learner_id: string | null;
  state: "complete" | "partial" | "untouched";
  /** As the rater wrote it on the document. */
  date_completed: string | null;
};

/** Who rated a lesson in the study, and which lessons the study's Part 2 compared. */
export type RaterSchedule = {
  sets: RatedSet[];
  compared_lessons: { experiment_id: string; experiment_code: string }[];
};

export type StudyRatings = {
  scores: CriterionScore[];
  judgements: ComparativeJudgement[];
  documents: RatingDocument[];
};

/** How much the study's raters recorded about one lesson's revision notes. */
export type StudyRatingsTally = {
  plan_version_id: string;
  scores: number;
  judgements: number;
  raters: number;
};

/** One criterion as the raters read it. */
export type InstrumentCriterion = {
  id: string;
  name: string;
  question: string;
  /** What scores 1 to 5 mean. */
  descriptors: string[];
  notes: string[];
  better: string;
};

/** The study's rating instrument, worded as on the rating documents. */
export type StudyInstrument = {
  scale: [number, string][];
  comparison: string[];
  part_1: InstrumentCriterion[];
  part_2: InstrumentCriterion[];
};

/** Part 1: one criterion's scores for one condition's notes, described. */
export type ConditionMean = {
  condition: string;
  criterion_id: string;
  mean: number;
  n: number;
  /** How many scores were 1, 2, 3, 4 and 5. */
  score_counts: number[];
  /** Cells two raters scored, and those both scored 4 or 5. */
  double_rated: number;
  both_favourable: number;
};

/** Part 2: how often one criterion's comparison came out one way in a lesson. */
export type ChoiceCount = {
  criterion_id: string;
  favoured: "P1" | "P0" | "neither";
  strength: "clearly" | "slightly" | null;
  count: number;
};

/** A lesson's study ratings described: every rater, draw and objective pooled. */
export type LessonResults = { part_1: ConditionMean[]; part_2: ChoiceCount[] };

/** One lesson objective's mean score for one condition: a single data point of the study. */
export type ObjectiveMean = {
  lesson: string;
  objective_id: string;
  objective_text: string | null;
  condition: string;
  mean: number;
  n: number;
};

/** A study's ratings across its lessons, described, with each objective as a data point. */
export type StudyWideResults = LessonResults & { objectives: ObjectiveMean[] };
