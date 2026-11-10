import { useMemo, useState } from "react";

import { useMutation, useQuery } from "@tanstack/react-query";
import { useForm, useWatch } from "react-hook-form";

import {
  attachExitAssessmentSurvey,
  getExitAssessmentQuestions,
  listMyClassLessons,
  listSubmissions,
  submitExitAssessment,
  SurveyScale,
} from "@/features/student/api/exitAssessment";
import { isSurveyComplete } from "@/features/student/lib/surveyCompletion";

/** Wizard step for the exit-assessment flow. */
export type ExitAssessmentStep = "select" | "assess";

/** Sub-phase within "assess": test first, survey only after the score is in. */
export type ExitAssessmentPhase = "questions" | "survey" | "done";

/** Per-item selected option (react-hook-form field). */
export type AssessmentAnswerField = {
  item_id: string;
  lesson_objective_id: string;
  selected_option: string;
};

/** Per-objective survey (react-hook-form field): 1-5 per the learner-model spec. */
export type AssessmentSurveyField = {
  lesson_objective_id: string;
  confidence: SurveyScale | null;
  perceived_difficulty: SurveyScale | null;
};

/** The full react-hook-form value shape. */
export type AssessmentFormValues = {
  answers: AssessmentAnswerField[];
  survey: AssessmentSurveyField[];
  /** Session-level Interest + Affect (asked once for the whole session). */
  session: { interest: SurveyScale | null; affect: SurveyScale | null };
};

/**
 * Glue hook for the student MCQ exit-assessment: lesson + question queries, a
 * react-hook-form for the selected options + survey, diagnostic generation (if
 * the lesson has no items yet), submission (graded server-side), and pack
 * generation. UI/wizard state uses local state; form inputs use react-hook-form.
 */
export const useExitAssessment = (
  studentId: string | null,
  initialPlanVersionId?: string | null
) => {
  const [step, setStep] = useState<ExitAssessmentStep>(
    initialPlanVersionId ? "assess" : "select"
  );
  const [planVersionId, setPlanVersionId] = useState<string | null>(
    initialPlanVersionId ?? null
  );
  const [diagnosticId, setDiagnosticId] = useState<string | null>(null);
  const [surveyDone, setSurveyDone] = useState(false);

  const lessonsQuery = useQuery({
    queryKey: ["exitAssessmentLessons", studentId],
    queryFn: listMyClassLessons,
    enabled: Boolean(studentId) && step === "select",
  });

  const questionsQuery = useQuery({
    queryKey: ["exitAssessmentQuestions", planVersionId],
    queryFn: () => getExitAssessmentQuestions(planVersionId as string),
    enabled: Boolean(planVersionId) && step === "assess",
  });

  // A student who already answered comes back to the survey, or to the finished screen.
  const submissionsQuery = useQuery({
    queryKey: ["studentSubmissions", studentId],
    queryFn: () => listSubmissions(studentId as string),
    enabled: Boolean(studentId) && Boolean(planVersionId) && step === "assess",
  });
  const earlier = submissionsQuery.data?.find((row) => row.plan_version_id === planVersionId);
  const activeDiagnosticId = diagnosticId ?? earlier?.diagnostic_id ?? null;
  const alreadySubmitted = !diagnosticId && Boolean(earlier);

  const objectives = useMemo(
    () => questionsQuery.data?.objectives ?? [],
    [questionsQuery.data]
  );
  const hasItems = objectives.some((objective) => objective.items.length > 0);

  const formValues = useMemo<AssessmentFormValues>(
    () => ({
      answers: objectives.flatMap((objective) =>
        objective.items.map((item) => ({
          item_id: item.item_id,
          lesson_objective_id: objective.lesson_objective_id,
          selected_option: "",
        }))
      ),
      survey: objectives.map((objective) => ({
        lesson_objective_id: objective.lesson_objective_id,
        confidence: null,
        perceived_difficulty: null,
      })),
      session: { interest: null, affect: null },
    }),
    [objectives]
  );

  const form = useForm<AssessmentFormValues>({ values: formValues });

  const itemOffsets = useMemo(() => {
    const offsets: number[] = [];
    let acc = 0;
    for (const objective of objectives) {
      offsets.push(acc);
      acc += objective.items.length;
    }
    return offsets;
  }, [objectives]);

  const watchedAnswers = useWatch({ control: form.control, name: "answers" });
  const answeredByObjective = useMemo(() => {
    const out: Record<string, { answered: number; total: number }> = {};
    for (const answer of watchedAnswers ?? []) {
      const tally = out[answer.lesson_objective_id] ?? { answered: 0, total: 0 };
      tally.total += 1;
      if (answer.selected_option) tally.answered += 1;
      out[answer.lesson_objective_id] = tally;
    }
    return out;
  }, [watchedAnswers]);

  const [watchedSurvey, watchedSession] = useWatch({
    control: form.control,
    name: ["survey", "session"],
  });
  const surveyComplete = isSurveyComplete({
    survey: watchedSurvey ?? [],
    session: watchedSession ?? { interest: null, affect: null },
  });


  // Step 1: answers only — graded immediately; the survey screen follows.
  // survey_pending defers pack generation until the survey is attached.
  const submitMutation = useMutation({
    mutationFn: () => {
      const values = form.getValues();
      return submitExitAssessment({
        student_id: studentId as string,
        plan_version_id: planVersionId as string,
        answers: values.answers.filter((answer) => answer.selected_option),
        survey: [],
        survey_pending: true,
      });
    },
    onSuccess: (data) => setDiagnosticId(data.diagnostic_id),
  });

  // Step 2: the post-class survey — completes the evidence; the backend then
  // generates the student's pack as a pending artefact for teacher review.
  const surveyMutation = useMutation({
    mutationFn: () => {
      const values = form.getValues();
      return attachExitAssessmentSurvey(activeDiagnosticId as string, {
        survey: values.survey,
        session_survey: values.session,
      });
    },
    onSuccess: () => setSurveyDone(true),
  });

  // questions -> (answers graded) -> survey -> done. The survey only appears
  // AFTER the score is submitted so it can't colour how students answer.
  const phase: ExitAssessmentPhase = !activeDiagnosticId
    ? "questions"
    : surveyDone || (alreadySubmitted && !earlier?.survey_pending)
      ? "done"
      : "survey";

  return {
    step,
    phase,
    objectives,
    hasItems,
    itemOffsets,
    form,
    lessonsQuery,
    questionsQuery,
    answeredByObjective,
    diagnosticId: activeDiagnosticId,
    alreadySubmitted,
    isCheckingSubmission: submissionsQuery.isLoading,
    selectLesson: (versionId: string) => {
      setPlanVersionId(versionId);
      setStep("assess");
    },
    submit: submitMutation.mutate,
    isSubmitting: submitMutation.isPending,
    submitSurvey: surveyMutation.mutate,
    isSubmittingSurvey: surveyMutation.isPending,
    surveyComplete,
    hasError: submitMutation.isError || surveyMutation.isError,
  };
};
