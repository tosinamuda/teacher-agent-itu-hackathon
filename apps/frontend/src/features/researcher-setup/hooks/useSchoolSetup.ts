import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  createResearchLearner,
  createResearchSchool,
  createSchoolSetupWorkspace,
  createTeacher,
  getResearchSchool,
  getSchoolSetupCatalog,
  listResearchLearners,
  listResearchSchools,
  listSchoolClasses,
  listSchoolSetupWorkspaces,
  updateResearchSchool,
} from "../api";
import {
  CreateResearchLearnerRequest,
  CreateSchoolRequest,
  CreateSchoolWorkspaceRequest,
  UpdateSchoolRequest,
} from "../types";

/** Lists schools for the setup workspace. */
export const useResearchSchools = () =>
  useQuery({
    queryKey: ["researchSchools"],
    queryFn: listResearchSchools,
  });

/** Loads a single school for the selected-school page. */
export const useResearchSchool = (schoolId?: string) =>
  useQuery({
    queryKey: ["researchSchool", schoolId ?? "empty"],
    queryFn: () => getResearchSchool(schoolId ?? ""),
    enabled: Boolean(schoolId),
  });

/** Loads grade, subject, teacher, year, and term options. */
export const useSchoolSetupCatalog = () =>
  useQuery({
    queryKey: ["schoolSetupCatalog"],
    queryFn: getSchoolSetupCatalog,
  });

/** Lists setup workspaces scoped to a school. */
export const useSchoolSetupWorkspaces = (schoolId?: string) =>
  useQuery({
    queryKey: ["schoolSetupWorkspaces", schoolId ?? "all"],
    queryFn: () => listSchoolSetupWorkspaces(schoolId),
  });

/** Lists classes scoped to a school. */
export const useSchoolClasses = (schoolId?: string) =>
  useQuery({
    queryKey: ["schoolClasses", schoolId ?? "all"],
    queryFn: () => listSchoolClasses(schoolId),
    enabled: Boolean(schoolId),
  });

/** Creates a school and refreshes the setup overview. */
export const useCreateResearchSchool = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: CreateSchoolRequest) => createResearchSchool(payload),
    onSuccess: (school) => {
      void queryClient.invalidateQueries({ queryKey: ["researchSchools"] });
      void queryClient.setQueryData(["researchSchool", school.id], school);
    },
  });
};

/** Onboards a teacher and refreshes the setup catalog (the assign-teacher list). */
export const useCreateTeacher = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: { full_name: string; email: string; code: string }) =>
      createTeacher(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["schoolSetupCatalog"] });
    },
  });
};

/** Updates a school and refreshes directory and detail caches. */
export const useUpdateResearchSchool = (schoolId?: string) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: UpdateSchoolRequest) =>
      updateResearchSchool(schoolId ?? "", payload),
    onSuccess: (school) => {
      void queryClient.invalidateQueries({ queryKey: ["researchSchools"] });
      void queryClient.setQueryData(["researchSchool", school.id], school);
    },
  });
};

/** Creates a workspace and refreshes the school-specific lists. */
export const useCreateSchoolSetupWorkspace = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: CreateSchoolWorkspaceRequest) =>
      createSchoolSetupWorkspace(payload),
    onSuccess: (_data, variables) => {
      void queryClient.invalidateQueries({ queryKey: ["researchSchools"] });
      void queryClient.invalidateQueries({
        queryKey: ["schoolSetupWorkspaces", variables.school_id],
      });
      void queryClient.invalidateQueries({
        queryKey: ["schoolClasses", variables.school_id],
      });
    },
  });
};

/** Creates a learner and refreshes class-scoped caches. */
export const useCreateResearchLearner = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: CreateResearchLearnerRequest) => createResearchLearner(payload),
    onSuccess: (_data, variables) => {
      void queryClient.invalidateQueries({ queryKey: ["schoolClasses"] });
      void queryClient.invalidateQueries({
        queryKey: ["researchLearners", variables.class_id],
      });
    },
  });
};

/** Lists learners scoped to a selected class for the researcher setup page. */
export const useResearchLearners = (classId?: string) =>
  useQuery({
    queryKey: ["researchLearners", classId ?? "all"],
    queryFn: () => listResearchLearners(classId),
    enabled: Boolean(classId),
  });
