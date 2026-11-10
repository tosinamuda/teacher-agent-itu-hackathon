import { QueryClient, useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { useGenerateContent } from "@/features/content/hooks/useContent";
import { runJob } from "@/shared/api/jobs";
import { followedJobKey, useFollowJob } from "@/shared/hooks/useFollowJob";

import {
  AUTHOR_EXPERIMENT_PLAN,
  RUN_CONDITIONED_EXECUTION,
  authorExperimentPlan,
  createExperiment,
  createReviewNote,
  exportExperimentPackets,
  freezeExperimentPlan,
  getExperiment,
  getExperimentExecution,
  getExperimentSummary,
  launchExperimentExecution,
  listExperimentApprovedVersions,
  listExperimentWorkspaceLessons,
  listExperimentWorkspaces,
  listExperiments,
  retryExperimentCondition,
  sendAssessment,
  setExperimentSandbox,
  updateExperimentFocalLearners,
} from "../lib/api";
import {
  ExperimentCreateRequest,
  ExperimentExecutionCreateRequest,
  ExperimentFilters,
} from "../lib/experiments";

export const experimentKey = (experimentId: string) => ["experiment", experimentId] as const;
const executionKey = (executionId: string) => ["experimentExecution", executionId] as const;

/** Lists experiment containers using the current filter state. */
export const useExperiments = (filters: ExperimentFilters) =>
  useQuery({
    queryKey: [
      "experiments",
      filters.schoolId,
      filters.teacherWorkspaceId,
      filters.experimentCode,
      filters.query,
      filters.hypothesis,
      filters.status,
    ],
    queryFn: () => listExperiments(filters),
    placeholderData: (previousData) => previousData,
  });

/** Fetches a single experiment detail payload. */
export const useExperiment = (experimentId: string | null) =>
  useQuery({
    queryKey: experimentId ? experimentKey(experimentId) : ["experiment", "empty"],
    queryFn: () => getExperiment(experimentId ?? ""),
    enabled: Boolean(experimentId),
  });

/**
 * Fetches one experiment's header only — the teacher-accessible read used by the
 * lesson-prep + plan-review pages (the teacher role can't call the researcher
 * detail endpoint behind {@link useExperiment}).
 *
 * Shares the ``experimentKey`` cache key with {@link useExperiment} on purpose:
 * the teacher gate mutations (author / freeze / create-note / assessment) all
 * invalidate that key, so the lesson-prep checklist still advances after each
 * action. The two are never mounted together (teacher vs researcher routes), and
 * the header is a strict subset of the detail, so the shared cache is safe.
 */
export const useExperimentSummary = (experimentId: string | null) =>
  useQuery({
    queryKey: experimentId ? experimentKey(experimentId) : ["experiment", "empty"],
    queryFn: () => getExperimentSummary(experimentId ?? ""),
    enabled: Boolean(experimentId),
  });

/** Fetches a single execution detail payload. */
export const useExperimentExecution = (executionId: string | null) =>
  useQuery({
    queryKey: executionId ? executionKey(executionId) : ["experimentExecution", "empty"],
    queryFn: () => getExperimentExecution(executionId ?? ""),
    enabled: Boolean(executionId),
  });

/** Lists workspace options for experiment creation and filtering. */
export const useExperimentWorkspaces = (schoolId?: string) =>
  useQuery({
    queryKey: ["experimentWorkspaces", schoolId ?? "all"],
    queryFn: () => listExperimentWorkspaces(schoolId),
  });

/** Lists lesson options for a selected workspace. */
export const useExperimentWorkspaceLessons = (workspaceId: string | null) =>
  useQuery({
    queryKey: ["experimentWorkspaceLessons", workspaceId ?? "empty"],
    queryFn: () => listExperimentWorkspaceLessons(workspaceId ?? ""),
    enabled: Boolean(workspaceId),
  });

/** Lists approved baseline versions for a selected workspace lesson. */
export const useExperimentApprovedVersions = (
  workspaceId: string | null,
  lessonPeriodId: string | null
) =>
  useQuery({
    queryKey: [
      "experimentApprovedVersions",
      workspaceId ?? "empty",
      lessonPeriodId ?? "empty",
    ],
    queryFn: () =>
      listExperimentApprovedVersions(workspaceId ?? "", lessonPeriodId ?? ""),
    enabled: Boolean(workspaceId && lessonPeriodId),
  });

/** Creates a new experiment and refreshes the list cache. */
export const useCreateExperiment = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: ExperimentCreateRequest) => createExperiment(payload),
    onSuccess: (data) => {
      void queryClient.invalidateQueries({ queryKey: ["experiments"] });
      void queryClient.setQueryData(experimentKey(data.experiment_id), data);
    },
  });
};

/**
 * The assigned teacher authors the experiment's own plan (mints a fresh plan), as a job.
 * `isPending` holds until the plan is bound, and across a reload of the page.
 */
export const useAuthorExperimentPlan = (experimentId: string) => {
  const queryClient = useQueryClient();
  const refresh = () => {
    void queryClient.invalidateQueries({ queryKey: experimentKey(experimentId) });
    void queryClient.invalidateQueries({ queryKey: ["experiments"] });
  };
  const followed = useFollowJob(AUTHOR_EXPERIMENT_PLAN, experimentId, refresh);
  const mutation = useMutation({
    mutationFn: () =>
      runJob(async () => {
        const accepted = await authorExperimentPlan(experimentId);
        void queryClient.invalidateQueries({
          queryKey: followedJobKey(AUTHOR_EXPERIMENT_PLAN, experimentId),
        });
        return accepted;
      }),
    onSuccess: refresh,
  });
  return {
    mutateAsync: mutation.mutateAsync,
    isPending: mutation.isPending || followed.running,
    isError: mutation.isError,
    error: mutation.error,
  };
};

/** The teacher accepts (freezes) the experiment's plan — triggers generation.
 *  Pass the revised head ``acceptedVersionId`` so feedback-loop edits aren't lost. */
export const useFreezeExperimentPlan = (experimentId: string) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (acceptedVersionId?: string | null) =>
      freezeExperimentPlan(experimentId, acceptedVersionId),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: experimentKey(experimentId) });
      void queryClient.invalidateQueries({ queryKey: ["experiments"] });
    },
  });
};

/**
 * Teacher action: generate the class revision note (runs the background build).
 * Invalidates the experiment + list + pending-notes queries so the lesson-prep
 * checklist advances once generation is queued.
 */
/**
 * Follow a conditioned execution while it runs, such as the build of the class revision note
 * or a lab's P0/P1 generation, so its page refreshes as soon as it ends. `executionId` is null
 * when there is none to follow.
 */
export const useFollowExecution = (experimentId: string, executionId: string | null) => {
  const queryClient = useQueryClient();
  return useFollowJob(RUN_CONDITIONED_EXECUTION, executionId, () => {
    void queryClient.invalidateQueries({ queryKey: experimentKey(experimentId) });
    void queryClient.invalidateQueries({ queryKey: ["experiments"] });
    void queryClient.invalidateQueries({ queryKey: ["content"] });
  });
};

export const useCreateReviewNote = (experimentId: string) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: () => createReviewNote(experimentId),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: experimentKey(experimentId) });
      void queryClient.invalidateQueries({ queryKey: ["experiments"] });
      void queryClient.invalidateQueries({ queryKey: ["pendingStudentNotes"] });
    },
  });
};

/** What shows the lesson's assessment: its checklist, the lists, its status and its content card. */
const refreshAssessment = (queryClient: QueryClient, experimentId: string) => {
  void queryClient.invalidateQueries({ queryKey: experimentKey(experimentId) });
  void queryClient.invalidateQueries({ queryKey: ["experiments"] });
  void queryClient.invalidateQueries({ queryKey: ["assessmentStatus"] });
  void queryClient.invalidateQueries({ queryKey: ["content"] });
};

/** Teacher action: create the exit assessment for a lesson, as a job the gate follows. */
export const useCreateAssessment = (planVersionId: string | null) => {
  const generation = useGenerateContent(planVersionId, "class-test");
  return {
    mutate: () => generation.create({}),
    isPending: generation.isPending,
    isError: generation.isError,
  };
};

/** Teacher action: send (release) the lesson's assessment to students. */
export const useSendAssessment = (experimentId: string, planVersionId: string | null) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: () => sendAssessment(planVersionId ?? ""),
    onSuccess: () => refreshAssessment(queryClient, experimentId),
  });
};

/** Launches an execution for the current experiment. */
export const useLaunchExperimentExecution = (experimentId: string | null) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: ExperimentExecutionCreateRequest) => {
      if (!experimentId) {
        throw new Error("experiment_not_selected");
      }
      return launchExperimentExecution(experimentId, payload);
    },
    onSuccess: (data) => {
      void queryClient.invalidateQueries({ queryKey: ["experiments"] });
      if (experimentId) {
        void queryClient.invalidateQueries({ queryKey: experimentKey(experimentId) });
      }
      void queryClient.setQueryData(executionKey(data.execution_id), data);
    },
  });
};

/** Marks/unmarks an experiment as a throwaway sandbox + refreshes caches. */
export const useSetExperimentSandbox = (experimentId: string | null) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (isSandbox: boolean) => {
      if (!experimentId) {
        throw new Error("experiment_not_selected");
      }
      return setExperimentSandbox(experimentId, isSandbox);
    },
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["experiments"] });
      if (experimentId) {
        void queryClient.invalidateQueries({ queryKey: experimentKey(experimentId) });
      }
    },
  });
};

/** Retries one FAILED H1 condition + refreshes the experiment detail cache. */
export const useRetryExperimentCondition = (experimentId: string | null) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (conditionCode: string) => {
      if (!experimentId) {
        throw new Error("experiment_not_selected");
      }
      return retryExperimentCondition(experimentId, conditionCode);
    },
    onSuccess: () => {
      if (experimentId) {
        void queryClient.invalidateQueries({ queryKey: experimentKey(experimentId) });
      }
    },
  });
};

/** Saves focal learners and refreshes the experiment detail cache. */
export const useUpdateExperimentFocalLearners = (experimentId: string | null) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (learnerIds: string[]) => {
      if (!experimentId) {
        throw new Error("experiment_not_selected");
      }
      return updateExperimentFocalLearners(experimentId, learnerIds);
    },
    onSuccess: () => {
      if (experimentId) {
        void queryClient.invalidateQueries({ queryKey: experimentKey(experimentId) });
      }
    },
  });
};

/** Exports evaluation packets for the current execution. */
export const useExportExperimentPackets = (executionId: string | null) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: () => {
      if (!executionId) {
        throw new Error("execution_not_selected");
      }
      return exportExperimentPackets(executionId);
    },
    onSuccess: () => {
      if (executionId) {
        void queryClient.invalidateQueries({ queryKey: executionKey(executionId) });
      }
    },
  });
};
