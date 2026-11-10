import { Link } from "@/shared/router";
import { useRouter } from "@/shared/router";
import { useMemo } from "react";

import { Card } from "@/shared/components/ui/Card";

import { SchoolDetailsForm } from "../components/SchoolDetailsForm";
import { useCreateResearchSchool } from "../hooks/useSchoolSetup";

/** Standalone "create a school" page — the form, on its own route, separated from the
 *  directory. On success it returns to the directory with the new school highlighted. */
export function NewResearchSchoolPage() {
  const router = useRouter();
  const createSchool = useCreateResearchSchool();
  const initialValues = useMemo(() => ({ name: "", school_code: "" }), []);

  return (
    <main className="flex w-full max-w-xl flex-col gap-6 py-8">
      <header className="space-y-3">
        <div className="text-[11px] font-semibold uppercase tracking-[0.18em] text-[color:var(--accent)]">
          Add school
        </div>
        <h1 className="text-4xl font-semibold tracking-tight text-[color:var(--ink)]">
          Create the next school in the study
        </h1>
        <p className="text-base leading-relaxed text-[color:var(--muted)]">
          Name the school and give it a short code. You&apos;ll add classes and learners once
          it&apos;s created.
        </p>
      </header>

      <Card variant="glass" padding="lg" className="space-y-4">
        <SchoolDetailsForm
          initialValues={initialValues}
          isLoading={createSchool.isPending}
          submitLabel="Create school"
          onSubmit={async (values) => {
            const school = await createSchool.mutateAsync(values);
            router.push(`/research/setup?created=${school.id}`);
          }}
        />
        <Link
          className="inline-flex text-sm font-semibold text-[color:var(--accent-deep)] hover:underline"
          href="/research/setup"
        >
          ← Back to directory
        </Link>
      </Card>
    </main>
  );
}
