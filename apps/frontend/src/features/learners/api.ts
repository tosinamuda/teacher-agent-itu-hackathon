import { apiFetch } from "@/shared/api/client";

import {
  ClassResponse,
  PaginatedLearnerResponse,
  ResearchSchoolOption,
  ResearchWorkspaceOption,
} from "./types";

type ExperimentContextEnvelope = {
  experiment: {
    experiment_id: string;
    experiment_code: string;
    lesson_title?: string | null;
    school_id?: string | null;
    class_id?: string | null;
    teacher_workspace_id: string;
  };
};

/** Lists schools that can be used to scope the research learner directory. */
export const listResearchLearnerSchools = async () =>
  apiFetch<ResearchSchoolOption[]>("/school/schools");

/** Lists classes for a selected school. */
export const listResearchLearnerClasses = async (schoolId?: string) =>
  apiFetch<ClassResponse[]>(`/school/classes${schoolId ? `?school_id=${schoolId}` : ""}`);

/** Lists researcher-visible workspaces for context filtering. */
export const listResearchLearnerWorkspaces = async (schoolId?: string) =>
  apiFetch<ResearchWorkspaceOption[]>(
    `/experiments/workspaces${schoolId ? `?school_id=${schoolId}` : ""}`
  );

/** Loads experiment context so the learner directory can be opened from a study lane. */
export const getResearchLearnerExperimentContext = async (experimentId: string) =>
  apiFetch<ExperimentContextEnvelope>(`/experiments/${experimentId}`).then(
    (response) => ({
      experiment_id: response.experiment.experiment_id,
      experiment_code: response.experiment.experiment_code,
      lesson_title: response.experiment.lesson_title ?? null,
      school_id: response.experiment.school_id ?? null,
      class_id: response.experiment.class_id ?? null,
      teacher_workspace_id: response.experiment.teacher_workspace_id,
    })
  );

/** Lists learners for the research directory. */
export const listResearchLearners = async (filters: {
  grade?: string;
  track?: string;
  classId?: string;
}) => {
  const params = new URLSearchParams();
  if (filters.grade) params.set("grade", filters.grade);
  if (filters.track) params.set("track", filters.track);
  if (filters.classId) params.set("class_id", filters.classId);
  params.set("page", "1");
  params.set("page_size", "100");
  return apiFetch<PaginatedLearnerResponse>(`/learners?${params.toString()}`);
};
