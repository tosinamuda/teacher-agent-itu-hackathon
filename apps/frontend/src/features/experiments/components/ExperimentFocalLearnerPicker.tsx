import { useEffect } from "react";
import { useForm, useWatch } from "react-hook-form";

import { Button } from "@/shared/components/ui/Button";
import { Card } from "@/shared/components/ui/Card";

import { ExperimentFocalLearnerOption } from "../lib/experiments";

type ExperimentFocalLearnerPickerProps = {
  candidates: ExperimentFocalLearnerOption[];
  selectedLearnerIds: string[];
  onSave: (learnerIds: string[]) => Promise<void>;
  isSaving: boolean;
};

type FormValues = {
  learnerIds: string[];
};

/** Persists the selected focal learners used to unlock H2 generation. */
export function ExperimentFocalLearnerPicker({
  candidates,
  selectedLearnerIds,
  onSave,
  isSaving,
}: ExperimentFocalLearnerPickerProps) {
  const form = useForm<FormValues>({
    defaultValues: { learnerIds: selectedLearnerIds },
  });

  useEffect(() => {
    form.reset({ learnerIds: selectedLearnerIds });
  }, [form, selectedLearnerIds]);

  const currentValues = useWatch({
    control: form.control,
    name: "learnerIds",
  }) ?? [];

  const toggleLearner = (learnerId: string) => {
    const nextValues = currentValues.includes(learnerId)
      ? currentValues.filter((value) => value !== learnerId)
      : [...currentValues, learnerId];
    form.setValue("learnerIds", nextValues, { shouldDirty: true });
  };

  const submit = form.handleSubmit(async (values) => {
    await onSave(values.learnerIds);
  });

  return (
    <Card variant="glass" padding="lg" className="space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[color:var(--muted)]">
            Focal learners
          </p>
          <h3 className="mt-1 text-lg font-semibold text-[color:var(--ink)]">
            Save the learner shortlist for H2
          </h3>
        </div>
        <span className="text-sm text-[color:var(--muted)]">
          {selectedLearnerIds.length} saved
        </span>
      </div>

      {candidates.length === 0 ? (
        <p className="text-sm text-[color:var(--muted)]">
          No learners are available in this workspace yet.
        </p>
      ) : (
        <form className="space-y-4" onSubmit={submit}>
          <div className="grid gap-3 md:grid-cols-2">
            {candidates.map((candidate) => {
              const checked = currentValues.includes(candidate.learner_id);
              return (
                <label
                  key={candidate.learner_id}
                  className={`rounded-3xl border p-4 transition ${
                    checked
                      ? "border-[color:var(--accent)] bg-[color:var(--accent-soft)]/40"
                      : "border-[color:var(--line)] bg-(--surface)"
                  }`}
                >
                  <div className="flex items-start gap-3">
                    <input
                      checked={checked}
                      className="mt-1"
                      disabled={!candidate.has_evidence}
                      type="checkbox"
                      onChange={() => toggleLearner(candidate.learner_id)}
                    />
                    <div className="space-y-1">
                      <p className="font-semibold text-[color:var(--ink)]">
                        {candidate.learner_name}
                      </p>
                      <p className="text-xs text-[color:var(--muted)]">
                        {candidate.learner_id}
                      </p>
                      <p className="text-xs text-[color:var(--muted)]">
                        {candidate.has_evidence
                          ? `Evidence: ${candidate.latest_diagnostic_id}`
                          : "No learner evidence yet"}
                      </p>
                    </div>
                  </div>
                </label>
              );
            })}
          </div>

          <Button
            disabled={currentValues.length === 0}
            isLoading={isSaving}
            type="submit"
          >
            Save focal learners
          </Button>
        </form>
      )}
    </Card>
  );
}
