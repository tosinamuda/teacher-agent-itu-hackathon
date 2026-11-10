import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";

import { apiFetch } from "@/shared/api/client";
import {
  StudentPackResponse,
  SubjectFilterOption,
  artefactResponseToSummary,
  filterArtefactsBySubject,
  getSubjectOptions,
  sortArtefactsByCreatedAt,
} from "@/features/student/lib/studentLessons";

// Optional: accept a forced student ID (e.g. from context)
export const useStudentWorkspace = (forcedStudentId?: string | null) => {
  // If we have a forced ID (auth mode), we don't need to fetch the list.
  // We assume the context/page handles the student fetching/verification.
  const resolvedStudentId = forcedStudentId ?? null;

  // Only fetch packs if we have an ID. The learner endpoint returns approved-only
  // packs, so students never see one that's still awaiting teacher review.
  const packsQuery = useQuery({
    queryKey: ["studentWorkspaceArtefacts", resolvedStudentId],
    queryFn: async () => {
      const packs = await apiFetch<StudentPackResponse[]>(
        `/artefacts/post-class-review-packs?learner_id=${resolvedStudentId}`
      );
      return packs.map(artefactResponseToSummary);
    },
    enabled: Boolean(resolvedStudentId),
  });

  const [subjectFilter, setSubjectFilter] = useState("all");
  const subjectOptions = useMemo<SubjectFilterOption[]>(
    () => getSubjectOptions(packsQuery.data ?? []),
    [packsQuery.data]
  );
  const activeSubject = useMemo(() => {
    if (subjectOptions.find((option) => option.value === subjectFilter)) {
      return subjectFilter;
    }
    return "all";
  }, [subjectFilter, subjectOptions]);

  const packs = useMemo(
    () => sortArtefactsByCreatedAt(packsQuery.data ?? []),
    [packsQuery.data]
  );
  const filteredPacks = useMemo(
    () => filterArtefactsBySubject(packs, activeSubject),
    [packs, activeSubject]
  );

  return {
    selectedLearnerId: resolvedStudentId ?? "",
    packsQuery,
    packs: filteredPacks,
    subjectOptions,
    subjectFilter: activeSubject,
    setSubjectFilter,
  };
};
