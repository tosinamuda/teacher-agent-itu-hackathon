import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";

import { useTeachingWorkspace } from "@/features/teaching-workspace/context/TeachingWorkspaceContext";
import { arrangeLearners, type LearnerOrder } from "../lib/arrangeLearners";
import { classLearnersQuery } from "../lib/classLearnersQuery";

/** The learners of the class the teacher has open, each with their latest class test. */
export function useLearnerList() {
  const { currentWorkspace } = useTeachingWorkspace();
  const [search, setSearch] = useState("");
  const [order, setOrder] = useState<LearnerOrder>("attention");
  const workspaceId = currentWorkspace?.id ?? "";

  const learnersQuery = useQuery(classLearnersQuery(workspaceId));

  const everyone = learnersQuery.data?.learners;
  const learners = useMemo(() => arrangeLearners(everyone ?? [], search, order), [everyone, search, order]);
  const notesToReview = (everyone ?? []).reduce((sum, learner) => sum + learner.notes_to_review, 0);

  return {
    learnersQuery,
    learners,
    total: everyone?.length ?? 0,
    notesToReview,
    search,
    setSearch,
    order,
    setOrder,
  };
}
