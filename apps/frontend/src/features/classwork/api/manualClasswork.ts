import { apiFetch } from "@/shared/api/client";

export type ManualClassworkObjective = {
  lesson_objective_id: string;
  objective_text?: string | null;
  curriculum_objective_id?: string | null;
};

export type KnowledgeComponentOption = {
  id: string;
  kc_code: string;
  description: string;
};

export type ExistingClassworkItem = {
  item_id: string;
  lesson_objective_id?: string | null;
  stem: string;
  options: Record<string, string>;
  correct_option: string;
  knowledge_component_id?: string | null;
  difficulty?: string | null;
  option_misconceptions?: Record<string, string> | null;
};

/** Form prerequisites for entering classwork: the frozen plan's objectives, the
 *  subtopic's knowledge components, any items already entered, and the frozen flag. */
export type ManualClassworkContext = {
  plan_version_id: string;
  subject?: string | null;
  topic?: string | null;
  subtopic?: string | null;
  objectives: ManualClassworkObjective[];
  knowledge_components: KnowledgeComponentOption[];
  items: ExistingClassworkItem[];
  released: boolean;
};

export type ClassworkObjectiveCoverage = {
  lesson_objective_id: string;
  objective_text?: string | null;
  item_count: number;
  has_items: boolean;
};

export type ClassworkCoverage = {
  plan_version_id: string;
  total_items: number;
  objectives: ClassworkObjectiveCoverage[];
  objectives_without_items: string[];
};

export type ClassworkItemPayload = {
  lesson_objective_id: string;
  stem: string;
  options: Record<string, string>;
  correct_option: string;
  knowledge_component_id: string | null;
  difficulty: string | null;
  option_misconceptions: Record<string, string>;
};

/** One item to derive distractor misconceptions for (FD-03). */
export type DeriveMisconceptionsItem = {
  stem: string;
  options: Record<string, string>;
  correct_option: string;
  lesson_objective_id: string | null;
};

export type DeriveMisconceptionsResponse = {
  items: { option_misconceptions: Record<string, string> }[];
};

export const fetchClassworkContext = (planVersionId: string): Promise<ManualClassworkContext> =>
  apiFetch<ManualClassworkContext>(
    `/assessments/exit-assessment/${encodeURIComponent(planVersionId)}/classwork/context`
  );

export const fetchClassworkCoverage = (planVersionId: string): Promise<ClassworkCoverage> =>
  apiFetch<ClassworkCoverage>(
    `/assessments/exit-assessment/${encodeURIComponent(planVersionId)}/classwork/coverage`
  );

/** Persist the experiment lesson's hand-entered classwork (replaces the set).
 *  Returns the items-per-objective coverage report. */
export const createExperimentManualClasswork = (
  experimentId: string,
  items: ClassworkItemPayload[]
): Promise<ClassworkCoverage> =>
  apiFetch<ClassworkCoverage>(
    `/experiments/${encodeURIComponent(experimentId)}/classwork/manual`,
    { method: "POST", body: JSON.stringify({ items }) }
  );

/** Suggest a misconception code per wrong option for the entered items (FD-03). */
export const deriveMisconceptions = (
  planVersionId: string,
  items: DeriveMisconceptionsItem[]
): Promise<DeriveMisconceptionsResponse> =>
  apiFetch<DeriveMisconceptionsResponse>(
    `/assessments/exit-assessment/${encodeURIComponent(planVersionId)}/classwork/derive-misconceptions`,
    { method: "POST", body: JSON.stringify({ items }) }
  );
