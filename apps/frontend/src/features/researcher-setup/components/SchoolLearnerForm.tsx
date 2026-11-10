import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { Button } from "@/shared/components/ui/Button";

import { researcherSetupFieldClass } from "../constants";
import { CreateResearchLearnerRequest } from "../types";

const learnerSchema = z.object({
  code: z.string().min(1, "Learner code is required."),
  full_name: z.string().min(1, "Learner name is required."),
  track: z.string().min(1, "Track is required."),
});

type SchoolLearnerFormProps = {
  classId: string;
  grade: string;
  isLoading: boolean;
  onSubmit: (values: CreateResearchLearnerRequest) => Promise<void>;
};

type LearnerFormValues = z.infer<typeof learnerSchema>;

/** Renders the inline learner creation form for a selected class. */
export function SchoolLearnerForm({
  classId,
  grade,
  isLoading,
  onSubmit,
}: SchoolLearnerFormProps) {
  "use no memo"; // react-hook-form 7 fills a registered input only when register() runs again on render.
  const form = useForm<LearnerFormValues>({
    resolver: zodResolver(learnerSchema),
    defaultValues: {
      code: "",
      full_name: "",
      track: "General",
    },
  });

  return (
    <form
      className="grid gap-3 md:grid-cols-3"
      onSubmit={form.handleSubmit(async (values) => {
        await onSubmit({
          ...values,
          class_id: classId,
          grade,
        });
        form.reset({
          code: "",
          full_name: "",
          track: values.track,
        });
      })}
    >
      <input
        className={researcherSetupFieldClass}
        placeholder="Learner code"
        {...form.register("code")}
      />
      <input
        className={researcherSetupFieldClass}
        placeholder="Learner full name"
        {...form.register("full_name")}
      />
      <input
        className={researcherSetupFieldClass}
        placeholder="Track"
        {...form.register("track")}
      />
      <div className="md:col-span-3">
        <Button isLoading={isLoading} type="submit">
          Add learner
        </Button>
      </div>
    </form>
  );
}
