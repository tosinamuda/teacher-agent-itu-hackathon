import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { Button } from "@/shared/components/ui/Button";

import { researcherSetupFieldClass } from "../constants";
import { useCreateTeacher } from "../hooks/useSchoolSetup";

const schema = z.object({
  full_name: z.string().min(1, "Name is required."),
  email: z.string().email("A valid email is required."),
  code: z.string().min(2, "A login code is required."),
});

type Values = z.infer<typeof schema>;

/**
 * Onboards a new teacher (name + email + login code) so they appear in the
 * "Assign teacher" list below. The code is how the teacher signs in.
 */
export function AddTeacherForm() {
  const create = useCreateTeacher();
  const form = useForm<Values>({
    resolver: zodResolver(schema),
    defaultValues: { full_name: "", email: "", code: "" },
  });

  return (
    <form
      className="grid gap-3 md:grid-cols-[1fr_1fr_0.8fr_auto]"
      onSubmit={form.handleSubmit(async (values) => {
        await create.mutateAsync(values);
        form.reset();
      })}
    >
      <input
        className={researcherSetupFieldClass}
        placeholder="Teacher full name"
        {...form.register("full_name")}
      />
      <input
        className={researcherSetupFieldClass}
        placeholder="Email"
        {...form.register("email")}
      />
      <input
        className={researcherSetupFieldClass}
        placeholder="Login code e.g. mrs-okoro"
        {...form.register("code")}
      />
      <Button isLoading={create.isPending} type="submit">
        Add teacher
      </Button>
      {create.isError ? (
        <p className="text-xs text-(--danger-ink) md:col-span-4">
          Couldn&apos;t add the teacher — the login code or email may already be taken.
        </p>
      ) : null}
    </form>
  );
}
