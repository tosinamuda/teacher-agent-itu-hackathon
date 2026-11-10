import { useRouter } from "@/shared/router";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { Button } from "@/shared/components/ui/Button";
import { Card } from "@/shared/components/ui/Card";

import { useCreateInvestigation } from "../hooks/useInvestigations";

const formSchema = z.object({
  title: z.string().min(1, "Name the study."),
  description: z.string().optional(),
});

type FormValues = z.infer<typeof formSchema>;

const fieldClass =
  "w-full rounded-none border border-[color:var(--line)] bg-(--surface) px-4 py-2 text-sm text-[color:var(--ink)] outline-none transition focus:border-[color:var(--accent)]";

/** Create a study: a name + optional description. Experiments are added afterwards. */
export default function NewInvestigationPage() {
  const router = useRouter();
  const createMutation = useCreateInvestigation();

  const { register, handleSubmit, formState } = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: { title: "", description: "" },
  });

  const submit = handleSubmit(async (values) => {
    const investigation = await createMutation.mutateAsync({
      title: values.title,
      description: values.description?.trim() || null,
    });
    router.push(`/research/investigations/${investigation.investigation_id}`);
  });

  return (
    <main className="mx-auto w-full max-w-3xl px-6 py-10">
      <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[color:var(--accent)]">
        New study
      </p>
      <h1 className="mt-1 text-2xl font-semibold text-(--ink)">Create a study</h1>
      <p className="mt-1 text-sm text-(--muted)">
        A study groups experiments under a shared hypothesis — it can span several schools and
        subjects. Name it now; add experiments to it next.
      </p>

      <form onSubmit={submit} className="mt-6 space-y-6">
        <Card padding="lg" className="space-y-4">
          <label className="block space-y-1">
            <span className="text-sm font-semibold text-(--ink)">Study name</span>
            <input
              className={fieldClass}
              placeholder="e.g. Grounding depth and curriculum alignment"
              {...register("title")}
            />
            {formState.errors.title ? (
              <span className="text-xs text-(--danger)">{formState.errors.title.message}</span>
            ) : null}
          </label>

          <label className="block space-y-1">
            <span className="text-sm font-semibold text-(--ink)">
              Description <span className="font-normal text-(--muted)">(optional)</span>
            </span>
            <textarea
              className={`${fieldClass} min-h-24 resize-y`}
              placeholder="The hypothesis this study tests, and what it pools across."
              {...register("description")}
            />
          </label>
        </Card>

        <div className="flex items-center justify-end gap-3">
          {createMutation.isError ? (
            <p className="text-sm text-(--danger)">Couldn&apos;t create the study.</p>
          ) : null}
          <Button type="submit" isLoading={createMutation.isPending}>
            Create study
          </Button>
        </div>
      </form>
    </main>
  );
}
