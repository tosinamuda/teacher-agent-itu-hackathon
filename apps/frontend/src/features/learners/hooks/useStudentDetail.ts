import { useState, useMemo, useEffect } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { useForm, useWatch } from "react-hook-form";
import { useRouter } from "@/shared/router";

import { useTeachingWorkspace } from "@/features/teaching-workspace/context/TeachingWorkspaceContext";
import { apiFetch } from "@/shared/api/client";
import {
  LearnerProfile,
  LearnerFormState,
  SubjectOfferingCatalog,
  ClassResponse,
} from "../types";
import {
  emptyForm,
  mapProfileToForm,
  toApiPayload,
} from "../services/studentService";

export function useLearnerDetail(learnerId?: string) {
  const router = useRouter();
  const { currentWorkspace } = useTeachingWorkspace();
  const [formError, setFormError] = useState<string | null>(null);

  const form = useForm<LearnerFormState>({
    defaultValues: emptyForm(),
  });

  // Fetch learner data if ID provided
  const learnerQuery = useQuery({
    queryKey: ["learner", learnerId],
    queryFn: () =>
      apiFetch<LearnerProfile>(`/learners/${learnerId}`),
    enabled: !!learnerId && learnerId !== "new",
  });

  // Populate form on load
  useEffect(() => {
    if (learnerQuery.data) {
      form.reset(mapProfileToForm(learnerQuery.data));
    } else if (!learnerId) {
      // Initialize for a new learner with workspace defaults
      form.reset(
        emptyForm({
          grade: currentWorkspace?.grade_level || "SS1",
        })
      );
    }
  }, [learnerQuery.data, learnerId, currentWorkspace, form]);

  const watchedGrade =
    useWatch({ control: form.control, name: "grade" }) || "SS1";
  const selectedFieldOfStudy =
    useWatch({ control: form.control, name: "field_of_study" }) ?? "";
  const watchedCoreSubjects = useWatch({
    control: form.control,
    name: "field_core_subjects",
  });
  const selectedCoreSubjects = useMemo(
    () => watchedCoreSubjects ?? [],
    [watchedCoreSubjects]
  );
  const selectedTradeSubject =
    useWatch({ control: form.control, name: "trade_subject" }) ?? "";

  // Auto-generate code from name for new learners
  const watchedFullName = useWatch({
    control: form.control,
    name: "full_name",
  });

  useEffect(() => {
    // Only auto-generate if we are creating a new learner (no props ID or "new")
    // and the user hasn't manually edited the Code (we assume strict auto-gen for now)
    const isNew = !learnerId || learnerId === "new";
    if (isNew && watchedFullName) {
      const slug = watchedFullName
        .toLowerCase()
        .trim()
        .replace(/[^a-z0-9\s-]/g, "") // remove special chars
        .replace(/\s+/g, "-"); // replace spaces with hyphens

      form.setValue("code", slug);
    }
  }, [watchedFullName, learnerId, form]);

  // Queries
  const catalogQuery = useQuery({
    queryKey: ["subjectOfferings"],
    queryFn: () => apiFetch<SubjectOfferingCatalog>("/school/subject-offerings"),
  });

  const classesQuery = useQuery({
    queryKey: ["classes", watchedGrade],
    queryFn: () => {
      const params = new URLSearchParams();
      if (watchedGrade) params.set("grade", watchedGrade);
      return apiFetch<ClassResponse[]>(
        `/classes?${params.toString()}`
      );
    },
  });

  const classOptions = useMemo(() => {
    if (!classesQuery.data) return [];
    return classesQuery.data.map((c) => ({ value: c.id, label: c.name }));
  }, [classesQuery.data]);

  const fieldOptions = useMemo(() => {
    const catalog = catalogQuery.data?.fields_of_study ?? {};
    return selectedFieldOfStudy ? catalog[selectedFieldOfStudy] ?? [] : [];
  }, [catalogQuery.data, selectedFieldOfStudy]);

  const subjectSummary = useMemo(() => {
    if (!catalogQuery.data) return [];
    const compulsory = catalogQuery.data.core_compulsory_subjects ?? [];
    const core = selectedCoreSubjects ?? [];
    const trade = selectedTradeSubject ? [selectedTradeSubject] : [];
    return [
      ...compulsory.filter((subject) => subject !== "One Trade Subject"),
      ...core,
      ...trade,
    ];
  }, [catalogQuery.data, selectedCoreSubjects, selectedTradeSubject]);

  // Mutations
  const createMutation = useMutation({
    mutationFn: (payload: LearnerFormState) =>
      apiFetch<LearnerProfile>("/learners", {
        method: "POST",
        body: JSON.stringify(toApiPayload(payload)),
      }),
    onSuccess: (student) => {
      setFormError(null);
      // Redirect to the new learner's detail page (using Code or ID? Backend returns ID)
      // We should probably redirect to the Code if we want friendly URLs,
      // but the route accepts both. Let's redirect to code if available, else ID.
      const redirectId = student.code || student.student_id;
      router.replace(`/research/teacher/learners/${redirectId}`);
    },
    onError: (error) => {
      setFormError(
        error instanceof Error ? error.message : "Failed to create learner."
      );
    },
  });

  const updateMutation = useMutation({
    mutationFn: (payload: LearnerFormState) =>
      apiFetch<LearnerProfile>(
        `/learners/${payload.student_id}`,
        {
          method: "PUT",
          body: JSON.stringify(toApiPayload(payload)),
        }
      ),
    onSuccess: () => {
      setFormError(null);
      // Invalidate query to refresh data
      learnerQuery.refetch();
    },

    onError: (error) => {
      setFormError(
        error instanceof Error ? error.message : "Failed to update learner."
      );
    },
  });

  const onSubmit = form.handleSubmit((values) => {
    if (learnerId && learnerId !== "new") {
      updateMutation.mutate(values);
    } else {
      createMutation.mutate(values);
    }
  });

  const toggleCoreSubject = (subject: string) => {
    const current = form.getValues("field_core_subjects") ?? [];
    if (current.includes(subject)) {
      form.setValue(
        "field_core_subjects",
        current.filter((item) => item !== subject)
      );
      return;
    }
    if (current.length >= 3) {
      setFormError("Select exactly 3 field core subjects.");
      return;
    }
    setFormError(null);
    form.setValue("field_core_subjects", [...current, subject]);
  };

  const handleFieldOfStudyChange = (nextField: string) => {
    const options = catalogQuery.data?.fields_of_study?.[nextField] ?? [];
    const currentCore = form.getValues("field_core_subjects") ?? [];
    form.setValue("field_of_study", nextField);
    form.setValue(
      "field_core_subjects",
      nextField
        ? currentCore.filter((subject) => options.includes(subject))
        : []
    );
  };

  return {
    form,
    learnerQuery,
    classOptions,
    fieldOptions,
    catalogQuery,
    formError,
    submitHandler: onSubmit,
    toggleCoreSubject,
    subjectSummary,
    isBusy: createMutation.isPending || updateMutation.isPending,
    selectedCoreSubjects,
    selectedTradeSubject,
    handleFieldOfStudyChange,
  };
}
