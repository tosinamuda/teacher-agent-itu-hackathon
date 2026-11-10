import { useMutation, useQueryClient } from "@tanstack/react-query";
import { apiFetch } from "@/shared/api/client";
import { SchemeOfWork, LessonPeriod } from "./useSchemeOfWork";

export interface UpdateWeekPayload {
  title?: string;
  objectives?: Record<string, unknown>;
}

export interface AddLessonPeriodPayload {
  period_number: number;
  subtopic_id: string;
}

export interface UpdateLessonPeriodPayload {
  subtopic_id?: string;
  period_number?: number;
}

export const useSyllabusMutations = () => {
  const queryClient = useQueryClient();

  const invalidateScheme = () => {
    queryClient.invalidateQueries({ queryKey: ["teaching", "term-class-subject"] });
  };

  const updateWeek = useMutation({
    mutationFn: async ({
      weekId,
      payload,
    }: {
      weekId: string;
      payload: UpdateWeekPayload;
    }) => {
      return apiFetch<SchemeOfWork>(`/teaching/scheme-of-work/${weekId}`, {
        method: "PUT",
        body: JSON.stringify(payload),
      });
    },
    onSuccess: () => invalidateScheme(),
  });

  const addDay = useMutation({
    mutationFn: async ({
      weekId,
      payload,
    }: {
      weekId: string;
      payload: AddLessonPeriodPayload;
    }) => {
      return apiFetch<LessonPeriod>(`/teaching/scheme-of-work/${weekId}/lesson-periods`, {
        method: "POST",
        body: JSON.stringify(payload),
      });
    },
    onSuccess: () => invalidateScheme(),
  });

  const updateDay = useMutation({
    mutationFn: async ({
      dayId,
      payload,
    }: {
      dayId: string;
      payload: UpdateLessonPeriodPayload;
    }) => {
      return apiFetch<LessonPeriod>(`/teaching/lesson-periods/${dayId}`, {
        method: "PUT",
        body: JSON.stringify(payload),
      });
    },
    onSuccess: () => invalidateScheme(),
  });

  const deleteDay = useMutation({
    mutationFn: async (dayId: string) => {
      return apiFetch<void>(`/teaching/lesson-periods/${dayId}`, {
        method: "DELETE",
      });
    },
    onSuccess: () => invalidateScheme(),
  });

  return {
    updateWeek,
    addDay,
    updateDay,
    deleteDay,
  };
};
