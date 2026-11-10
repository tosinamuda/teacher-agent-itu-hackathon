import { useEffect } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { Button } from "@/shared/components/ui/Button";

import { researcherSetupFieldClass } from "../constants";
import { CreateSchoolWorkspaceRequest, SchoolSetupCatalog } from "../types";

const workspaceSchema = z.object({
  class_name: z.string().min(1, "Class name is required."),
  grade_level_name: z.string().min(1, "Grade level is required."),
  subject_code: z.string().min(1, "Subject is required."),
  term: z.string().min(2, "Term is required."),
  academic_year: z.string().min(4, "Academic year is required."),
  teacher_id: z.string().min(1, "Teacher is required."),
});

type SchoolWorkspaceFormProps = {
  catalog?: SchoolSetupCatalog;
  isLoading: boolean;
  onSubmit: (values: Omit<CreateSchoolWorkspaceRequest, "school_id">) => Promise<void>;
};

type WorkspaceFormValues = z.infer<typeof workspaceSchema>;

/** Renders the inline workspace creation form for a selected school. */
export function SchoolWorkspaceForm({
  catalog,
  isLoading,
  onSubmit,
}: SchoolWorkspaceFormProps) {
  "use no memo"; // react-hook-form 7 fills a registered input only when register() runs again on render.
  const form = useForm<WorkspaceFormValues>({
    resolver: zodResolver(workspaceSchema),
    defaultValues: {
      class_name: "",
      grade_level_name: "",
      subject_code: "",
      term: "First Term",
      academic_year: "2025/2026",
      teacher_id: "",
    },
  });

  useEffect(() => {
    const defaultYear = catalog?.academic_years[0];
    const defaultTerm = catalog?.suggested_terms[0];
    if (!defaultYear || !defaultTerm) {
      return;
    }
    if (!catalog.academic_years.includes(form.getValues("academic_year"))) {
      form.setValue("academic_year", defaultYear);
    }
    if (!catalog.suggested_terms.includes(form.getValues("term"))) {
      form.setValue("term", defaultTerm);
    }
  }, [catalog, form]);

  return (
    <form
      className="grid gap-3 md:grid-cols-2"
      onSubmit={form.handleSubmit(async (values) => {
        await onSubmit(values);
        form.reset({ ...values, class_name: "" });
      })}
    >
      <input
        className={researcherSetupFieldClass}
        placeholder="Class name e.g. JSS1A"
        {...form.register("class_name")}
      />
      <select className={researcherSetupFieldClass} {...form.register("grade_level_name")}>
        <option value="">Select grade</option>
        {(catalog?.grade_levels ?? []).map((grade) => (
          <option key={grade.id} value={grade.name}>
            {grade.name}
          </option>
        ))}
      </select>
      <select className={researcherSetupFieldClass} {...form.register("subject_code")}>
        <option value="">Select subject</option>
        {(catalog?.subjects ?? []).map((subject) => (
          <option key={subject.id} value={subject.code}>
            {subject.name}
          </option>
        ))}
      </select>
      <select className={researcherSetupFieldClass} {...form.register("teacher_id")}>
        <option value="">Assign teacher</option>
        {(catalog?.teachers ?? []).map((teacher) => (
          <option key={teacher.id} value={teacher.id}>
            {teacher.full_name ?? teacher.email}
          </option>
        ))}
      </select>
      <select className={researcherSetupFieldClass} {...form.register("academic_year")}>
        {(catalog?.academic_years ?? []).map((year) => (
          <option key={year} value={year}>
            {year}
          </option>
        ))}
      </select>
      <select className={researcherSetupFieldClass} {...form.register("term")}>
        {(catalog?.suggested_terms ?? []).map((term) => (
          <option key={term} value={term}>
            {term}
          </option>
        ))}
      </select>
      <div className="md:col-span-2">
        <Button isLoading={isLoading} type="submit">
          Add workspace
        </Button>
      </div>
    </form>
  );
}
