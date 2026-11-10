import { useEffect, useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";

import {
  getResearchLearnerExperimentContext,
  listResearchLearnerClasses,
  listResearchLearnerSchools,
  listResearchLearners,
  listResearchLearnerWorkspaces,
} from "../api";

type UseResearchLearnerDirectoryOptions = {
  experimentId?: string | null;
  workspaceId?: string | null;
};

/** Coordinates filter state for the researcher-facing learner directory. */
export function useResearchLearnerDirectory({
  experimentId,
  workspaceId,
}: UseResearchLearnerDirectoryOptions) {
  const [schoolId, setSchoolId] = useState("");
  const [selectedWorkspaceId, setSelectedWorkspaceId] = useState("");
  const [classId, setClassId] = useState("");
  const [grade, setGrade] = useState("");
  const [track, setTrack] = useState("");

  const schoolsQuery = useQuery({
    queryKey: ["researchLearnerSchools"],
    queryFn: listResearchLearnerSchools,
  });
  const experimentContextQuery = useQuery({
    queryKey: ["researchLearnerExperimentContext", experimentId ?? "empty"],
    queryFn: () => getResearchLearnerExperimentContext(experimentId ?? ""),
    enabled: Boolean(experimentId),
  });
  const workspacesQuery = useQuery({
    queryKey: ["researchLearnerWorkspaces", schoolId || "all"],
    queryFn: () => listResearchLearnerWorkspaces(schoolId || undefined),
  });
  const classesQuery = useQuery({
    queryKey: ["researchLearnerClasses", schoolId || "all"],
    queryFn: () => listResearchLearnerClasses(schoolId || undefined),
  });
  const learnersQuery = useQuery({
    queryKey: ["researchLearnerList", grade, track, classId],
    queryFn: () => listResearchLearners({ grade, track, classId }),
  });

  const workspaces = useMemo(() => workspacesQuery.data ?? [], [workspacesQuery.data]);
  const classes = useMemo(() => classesQuery.data ?? [], [classesQuery.data]);
  const selectedWorkspace = workspaces.find(
    (workspace) => workspace.teacher_workspace_id === selectedWorkspaceId
  );

  useEffect(() => {
    if (experimentContextQuery.data?.school_id && !schoolId) {
      setSchoolId(experimentContextQuery.data.school_id);
    }
  }, [experimentContextQuery.data?.school_id, schoolId]);

  useEffect(() => {
    const preferredWorkspaceId =
      workspaceId || experimentContextQuery.data?.teacher_workspace_id;
    if (preferredWorkspaceId && !selectedWorkspaceId) {
      setSelectedWorkspaceId(preferredWorkspaceId);
    }
  }, [experimentContextQuery.data?.teacher_workspace_id, selectedWorkspaceId, workspaceId]);

  useEffect(() => {
    if (selectedWorkspace?.class_id && classId !== selectedWorkspace.class_id) {
      setClassId(selectedWorkspace.class_id);
      setGrade(selectedWorkspace.grade_level);
    }
  }, [classId, selectedWorkspace?.class_id, selectedWorkspace?.grade_level]);

  useEffect(() => {
    if (!selectedWorkspaceId && experimentContextQuery.data?.class_id && !classId) {
      setClassId(experimentContextQuery.data.class_id);
    }
  }, [classId, experimentContextQuery.data?.class_id, selectedWorkspaceId]);

  return {
    schoolId,
    setSchoolId,
    selectedWorkspaceId,
    setSelectedWorkspaceId,
    classId,
    setClassId,
    grade,
    setGrade,
    track,
    setTrack,
    schoolsQuery,
    workspacesQuery,
    classesQuery,
    learnersQuery,
    experimentContextQuery,
    workspaces,
    classes,
    selectedWorkspace,
  };
}
