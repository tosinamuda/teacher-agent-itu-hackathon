import { useEffect, useRef } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { Button } from "@/shared/components/ui/Button";
import { autofillSafeSubmit } from "@/shared/lib/autofillSafeSubmit";

import { researcherSetupFieldClass } from "../constants";
import { UpdateSchoolRequest, suggestSchoolCode } from "../types";

const schoolSchema = z.object({
  name: z.string().min(1, "School name is required."),
  school_code: z.string().min(2, "School code is required."),
});

type SchoolDetailsFormProps = {
  initialValues: UpdateSchoolRequest;
  isLoading: boolean;
  submitLabel: string;
  onSubmit: (values: UpdateSchoolRequest) => Promise<void>;
};

type SchoolFormValues = z.infer<typeof schoolSchema>;

const labelClass = "block text-sm font-medium text-[color:var(--ink)]";
const fieldClass = `${researcherSetupFieldClass} w-full`;

/** Reusable create/update form for a research school — just the school's
 *  identity (name + code). Academic-year/term ("session") are not modelled yet,
 *  so they're intentionally not collected here. */
export function SchoolDetailsForm({
  initialValues,
  isLoading,
  submitLabel,
  onSubmit,
}: SchoolDetailsFormProps) {
  "use no memo"; // react-hook-form 7 fills a registered input only when register() runs again on render.
  const form = useForm<SchoolFormValues>({
    resolver: zodResolver(schoolSchema),
    defaultValues: { name: initialValues.name, school_code: initialValues.school_code },
  });

  // Re-sync ONLY when the initial values actually change (e.g. an edited school
  // loads). Callers pass a fresh object literal every render, so guarding on
  // identity would reset the form on every parent re-render — wiping what the
  // user just typed and making submit fail "required" on a filled form.
  const lastSignatureRef = useRef<string | null>(null);
  useEffect(() => {
    const next = { name: initialValues.name, school_code: initialValues.school_code };
    const signature = JSON.stringify(next);
    if (signature !== lastSignatureRef.current) {
      lastSignatureRef.current = signature;
      form.reset(next);
    }
  }, [form, initialValues]);

  const { errors } = form.formState;

  return (
    <form
      className="space-y-5"
      onSubmit={autofillSafeSubmit(form, ["name", "school_code"], onSubmit)}
    >
      <div className="space-y-1.5">
        <label className={labelClass} htmlFor="school-name">
          School name
        </label>
        <input
          id="school-name"
          className={fieldClass}
          placeholder="e.g. Greenfield Secondary School"
          {...form.register("name")}
        />
        {errors.name && <p className="text-xs text-(--danger-ink)">{errors.name.message}</p>}
      </div>

      <div className="space-y-1.5">
        <label className={labelClass} htmlFor="school-code">
          School code
        </label>
        <div className="flex gap-2">
          <input
            id="school-code"
            className={`${fieldClass} flex-1`}
            placeholder="e.g. GSS-01"
            {...form.register("school_code")}
          />
          <Button
            type="button"
            variant="secondary"
            onClick={() => form.setValue("school_code", suggestSchoolCode(form.getValues("name")))}
          >
            Suggest
          </Button>
        </div>
        {errors.school_code && (
          <p className="text-xs text-(--danger-ink)">{errors.school_code.message}</p>
        )}
      </div>

      <Button isLoading={isLoading} type="submit">
        {submitLabel}
      </Button>
    </form>
  );
}
