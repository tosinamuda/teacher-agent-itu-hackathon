import { useMutation, useQueryClient } from "@tanstack/react-query";

import { reuseLessonPlan, type PlanSource } from "../api/reusePlan";

/** Use an existing plan as a lesson's plan, and refresh what the lesson shows. */
export const useReuseLessonPlan = (lessonPeriodId: string) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (variables: {
      source: PlanSource;
      choices: Record<string, string>;
    }) => reuseLessonPlan(lessonPeriodId, variables.source, variables.choices),
    onSuccess: (result) => {
      if (result.status !== "reused") return;
      void queryClient.invalidateQueries({ queryKey: ["sessionPlans"] });
      void queryClient.invalidateQueries({ queryKey: ["workspaceLessons"] });
    },
  });
};
