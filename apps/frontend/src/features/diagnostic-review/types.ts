/** One teacher-facing MCQ diagnostic item (with the answer key + tagged distractors). */
export type DiagnosticItem = {
  item_id: string;
  lesson_objective_id: string;
  stem: string;
  options: Record<string, string>;
  correct_option: string;
  distractor_misconceptions: Record<string, string>;
  difficulty: string;
};

/** One of the lesson plan's objectives, as a question names it. */
export type PlanObjective = {
  lesson_objective_id: string;
  objective_text: string;
  objective_order?: number | null;
};

/** The diagnostic seed/result payload carried by the revision thread. */
export type DiagnosticPayload = {
  plan_version_id: string;
  items: DiagnosticItem[];
};

/** One persisted revision turn on a diagnostic (instruction + what changed). */
export type DiagnosticRevisionTurn = {
  revision_turn_id: string;
  turn_number: number;
  instruction: string;
  summary?: string | null;
  validation_passed: boolean;
  created_at: string;
};

/** A diagnostic revision thread: turns + the current items (the chat seed). */
export type DiagnosticRevisionThread = {
  revision_thread_id: string;
  artefact_type: string;
  subject_id: string;
  current_session_plan?: DiagnosticPayload | null;
  turns: DiagnosticRevisionTurn[];
};

/** The result of submitting one turn: the new turn + the revised items. */
export type SubmitDiagnosticTurnResult = {
  turn: DiagnosticRevisionTurn;
  result_version_id: string;
  session_plan: DiagnosticPayload;
  validation_passed: boolean;
};
