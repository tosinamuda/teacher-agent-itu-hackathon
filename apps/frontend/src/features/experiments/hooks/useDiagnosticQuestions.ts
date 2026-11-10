import { useQuery } from "@tanstack/react-query";

import { getDiagnosticQuestions } from "../lib/api";

/** Loads the lesson's MCQ diagnostic for the journey's "diagnostic" step. */
export const useDiagnosticQuestions = (planVersionId: string | null | undefined) =>
  useQuery({
    queryKey: ["diagnosticQuestions", planVersionId ?? "empty"],
    queryFn: () => getDiagnosticQuestions(planVersionId ?? ""),
    enabled: Boolean(planVersionId),
  });
