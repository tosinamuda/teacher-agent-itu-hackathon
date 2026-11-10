import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { apiFetch } from "@/shared/api/client";
import { runJob, type JobAccepted } from "@/shared/api/jobs";
import {
  approveLessonPlan,
  closeLessonPlan,
  generateContent,
} from "@/features/content/api/content";
import type { FormValues } from "../schemas";

/** What a plan is generated from: the lesson, and the teacher it is for. */
export type GenerateRequest = Pick<FormValues, "session_id" | "teacher_id">;

import { LessonStepStructured } from "@/shared/types/lesson-schema";

type CurriculumObjectiveRef = {
  curriculum_objective_id: string;
  objective_text: string;
  objective_order: number;
};

type LessonPlanObjective = {
  lesson_objective_id: string;
  objective_text: string;
  objective_order: number;
  curriculum_objective_id: string;
  curriculum_objective_text: string;
  kc_type: "concept" | "procedure" | "representation";
  kc_focus: string;
  source_form?: string | null;
  target_form?: string | null;
};

/** Response from plan generation or fetch, including optional NERDC fields. */
export type PlanGenerationResponse = {
  plan_id: string;
  version_id: string;
  session_plan: {
    steps: LessonStepStructured[];
    curriculum_objectives?: CurriculumObjectiveRef[] | null;
    lesson_plan_objectives?: LessonPlanObjective[] | null;
    course_id?: string;
    /** NERDC curriculum theme. */
    theme?: string | null;
    /** Expected prior knowledge from the previous lesson. */
    entry_behaviour?: string[] | null;
    /** Teaching/learning materials and resources. */
    instructional_materials?: string[] | null;
    /** Textbook and reference citations. */
    references?: string[] | null;
    /** Subject name. */
    subject?: string;
    /** Grade level. */
    grade?: string;
    /** Academic term. */
    term?: string;
    /** Week number. */
    week?: number;
    /** Curriculum topic. */
    topic?: string;
    /** Curriculum subtopic. */
    subtopic?: string;
    /** Track/stream. */
    track?: string;
  };
  session_id?: string;
  /** Where the plan breaks the lesson document or leaves the lesson-plan spec unmet. */
  unmet_requirements?: string[];
  run_metadata?: {
    course_id?: string;
    [key: string]: unknown;
  };
  /** `draft`, `approved`, or `rejected` and `withdrawn` for a version the teacher closed. */
  version_status?: string;
  /** Why the teacher discarded this draft or took its approval back. */
  closed_reason?: string | null;
  closed_at?: string | null;
  approved_at?: string | null;
  approved_by?: string | null;
  artefact_id?: string;
};

/**
 * A plan as it stands. A page opened by a version's id shows that plan's latest version, since a
 * chat with the agent that wrote it adds versions to the plan, not to the one that was opened.
 */
export async function latestVersionOf(
  id: string,
): Promise<PlanGenerationResponse> {
  const opened = await apiFetch<PlanGenerationResponse>(
    `/artefacts/lesson-plans/${id}`,
  );
  return opened.plan_id === id
    ? opened
    : apiFetch<PlanGenerationResponse>(
        `/artefacts/lesson-plans/${opened.plan_id}`,
      );
}

export const usePlanGenerator = (initialPlanId?: string) => {
  const queryClient = useQueryClient();
  const activePlanId =
    initialPlanId && initialPlanId !== "new" ? initialPlanId : undefined;

  const {
    data: fetchedPlan,
    isLoading: isFetching,
    isError: loadFailed,
    refetch,
  } = useQuery({
    queryKey: ["plan", activePlanId],
    queryFn: () => latestVersionOf(activePlanId as string),
    enabled: !!activePlanId,
  });

  // Drafting runs as a job for its minutes; asking again for the same lesson while it runs
  // follows the same job. The plan it made is then read as any saved plan is.
  const generateMutation = useMutation({
    mutationFn: async (payload: GenerateRequest) => {
      const drafted = await runJob<{ plan_id: string }>(() =>
        apiFetch<JobAccepted>("/artefacts/lesson-plans/generate", {
          method: "POST",
          body: JSON.stringify({
            session_id: payload.session_id,
            teacher_id: payload.teacher_id,
          }),
        }),
      );
      return apiFetch<PlanGenerationResponse>(
        `/artefacts/lesson-plans/${drafted.plan_id}`,
      );
    },
    onSuccess: (data) => {
      // Pre-populate the cache for the new plan so it's ready upon redirect
      queryClient.setQueryData(["plan", data.plan_id], data);
    },
  });

  const approveMutation = useMutation({
    // The approver is the signed-in teacher, read server-side. A plan made here gets its class
    // test queued on approval; if that fails the teacher can still create it from the lesson.
    mutationFn: async (versionId: string) => {
      const plan = await approveLessonPlan(versionId);
      await generateContent(versionId, "class-test").catch(() => undefined);
      return plan;
    },
    onSuccess: (plan) => {
      void queryClient.invalidateQueries({ queryKey: ["plan", plan.id] });
      void queryClient.invalidateQueries({ queryKey: ["content"] });
    },
  });

  const closeMutation = useMutation({
    mutationFn: ({
      versionId,
      reason,
    }: {
      versionId: string;
      reason: string;
    }) => closeLessonPlan(versionId, reason),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["plan"] });
      void queryClient.invalidateQueries({ queryKey: ["sessionPlans"] });
      void queryClient.invalidateQueries({ queryKey: ["content"] });
    },
  });

  // Prefer fetched plan (persistent), fallback to just-generated plan (ephemeral before redirect)
  const planData = fetchedPlan || generateMutation.data || null;

  return {
    planData,
    generate: generateMutation.mutate,
    approve: approveMutation.mutate,
    close: closeMutation.mutate,
    isClosing: closeMutation.isPending,
    closeError: closeMutation.error,
    isGenerating: generateMutation.isPending,
    isApproving: approveMutation.isPending,
    isFetching,
    loadFailed,
    reload: refetch,
    generateError: generateMutation.error,
    approveError: approveMutation.error,
  };
};
