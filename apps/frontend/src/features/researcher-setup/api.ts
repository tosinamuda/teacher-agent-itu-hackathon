import { apiFetch } from "@/shared/api/client";

import {
  CreateResearchLearnerRequest,
  CreateSchoolRequest,
  CreateSchoolWorkspaceRequest,
  ResearchLearnerList,
  ResearchSchool,
  SchoolClass,
  SchoolSetupCatalog,
  SchoolSetupWorkspace,
  TeacherOption,
  UpdateSchoolRequest,
} from "./types";

/** Lists schools available to the researcher workspace. */
export const listResearchSchools = async () =>
  apiFetch<ResearchSchool[]>("/school/schools");

/** Creates a new school. */
export const createResearchSchool = async (payload: CreateSchoolRequest) =>
  apiFetch<ResearchSchool>("/school/schools", {
    method: "POST",
    body: JSON.stringify(payload),
  });

/** Loads a single school for the selected-school setup page. */
export const getResearchSchool = async (schoolId: string) =>
  apiFetch<ResearchSchool>(`/school/schools/${schoolId}`);

/** Updates a single school from the selected-school setup page. */
export const updateResearchSchool = async (
  schoolId: string,
  payload: UpdateSchoolRequest
) =>
  apiFetch<ResearchSchool>(`/school/schools/${schoolId}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });

/** Loads the researcher setup catalog. */
export const getSchoolSetupCatalog = async () =>
  apiFetch<SchoolSetupCatalog>("/school/setup/catalog");

/** Lists setup workspaces for the selected school. */
export const listSchoolSetupWorkspaces = async (schoolId?: string) =>
  apiFetch<SchoolSetupWorkspace[]>(
    `/school/setup/workspaces${schoolId ? `?school_id=${schoolId}` : ""}`
  );

/** Creates a school workspace assignment. */
export const createSchoolSetupWorkspace = async (
  payload: CreateSchoolWorkspaceRequest
) =>
  apiFetch<SchoolSetupWorkspace>("/school/setup/workspaces", {
    method: "POST",
    body: JSON.stringify(payload),
  });

/** Onboards a teacher so they can be assigned a workspace. */
export const createTeacher = async (payload: {
  full_name: string;
  email: string;
  code: string;
}) =>
  apiFetch<TeacherOption>("/school/teachers", {
    method: "POST",
    body: JSON.stringify(payload),
  });

/** Lists classes scoped to the selected school. */
export const listSchoolClasses = async (schoolId?: string) =>
  apiFetch<SchoolClass[]>(`/school/classes${schoolId ? `?school_id=${schoolId}` : ""}`);

/** Creates a basic learner record and assigns it to a class. */
export const createResearchLearner = async (
  payload: CreateResearchLearnerRequest
) =>
  apiFetch("/learners", {
    method: "POST",
    body: JSON.stringify(payload),
  });

/** Lists learners scoped to a single class for the selected-school page. */
export const listResearchLearners = async (classId?: string) =>
  apiFetch<ResearchLearnerList>(
    `/learners${classId ? `?class_id=${classId}&page=1&page_size=100` : "?page=1&page_size=100"}`
  );
