import { Link } from "@/shared/router";

import { Card } from "@/shared/components/ui/Card";

import { SchoolDetailsForm } from "../components/SchoolDetailsForm";
import { SchoolLearnersTab } from "../components/SchoolLearnersTab";
import { SchoolSetupProgress } from "../components/SchoolSetupProgress";
import { SchoolSetupTabs } from "../components/SchoolSetupTabs";
import { SchoolWorkspacesTab } from "../components/SchoolWorkspacesTab";
import {
  useResearchSchool,
  useSchoolSetupCatalog,
  useSchoolSetupWorkspaces,
  useUpdateResearchSchool,
  useCreateSchoolSetupWorkspace,
} from "../hooks/useSchoolSetup";
import type { SchoolSetupTab } from "../types";

type ResearchSchoolSetupDetailPageProps = {
  schoolId: string;
  section?: SchoolSetupTab;
};

/** Renders one section of the selected-school setup, driven by the path segment. */
export function ResearchSchoolSetupDetailPage({
  schoolId,
  section = "details",
}: ResearchSchoolSetupDetailPageProps) {
  const activeTab = section;
  const schoolQuery = useResearchSchool(schoolId);
  const catalogQuery = useSchoolSetupCatalog();
  const workspacesQuery = useSchoolSetupWorkspaces(schoolId);
  const updateSchool = useUpdateResearchSchool(schoolId);
  const createWorkspace = useCreateSchoolSetupWorkspace();
  const school = schoolQuery.data;

  if (schoolQuery.isLoading) {
    return (
      <main className="w-full py-8">
        <p className="text-sm text-[color:var(--muted)]">Loading school setup…</p>
      </main>
    );
  }

  if (schoolQuery.isError || !school) {
    return (
      <main className="w-full py-8">
        <Card padding="lg">
          <h1 className="text-2xl font-semibold text-[color:var(--ink)]">School not found</h1>
          <p className="mt-2 text-sm text-[color:var(--muted)]">
            The selected school could not be loaded.
          </p>
          <Link
            className="mt-4 inline-flex text-sm font-semibold text-[color:var(--accent-deep)] hover:underline"
            href="/research/setup"
          >
            Back to school directory
          </Link>
        </Card>
      </main>
    );
  }

  return (
    <main className="flex w-full flex-col gap-6 py-8">
      <header className="flex flex-wrap items-start justify-between gap-4">
        <div className="space-y-3">
          <div className="text-[11px] font-semibold uppercase tracking-[0.18em] text-[color:var(--accent)]">
            Selected school
          </div>
          <div>
            <h1 className="text-4xl font-semibold tracking-tight text-[color:var(--ink)]">
              {school.name}
            </h1>
            <p className="mt-2 text-sm text-[color:var(--muted)]">{school.school_code}</p>
          </div>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <Link
            className="rounded-none border border-[color:var(--line)] px-4 py-2 text-sm font-semibold text-[color:var(--ink)] hover:border-[color:var(--accent)]"
            href="/research/setup"
          >
            School directory
          </Link>
          <Link
            className="rounded-none bg-[color:var(--accent)] px-4 py-2 text-sm font-semibold text-white hover:bg-[color:var(--accent-deep)]"
            href={`/research/experiments/new?schoolId=${school.id}`}
          >
            Create experiment
          </Link>
        </div>
      </header>

      <SchoolSetupProgress schoolId={school.id} workspaceCount={school.workspace_count} />

      <SchoolSetupTabs activeTab={activeTab} schoolId={school.id} />

      {activeTab === "details" && (
        <Card variant="glass" padding="lg" className="space-y-4">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[color:var(--muted)]">
              Details
            </p>
            <h2 className="mt-1 text-lg font-semibold text-[color:var(--ink)]">
              Update school metadata used across experiments
            </h2>
          </div>
          <SchoolDetailsForm
            initialValues={{
              name: school.name,
              school_code: school.school_code,
            }}
            isLoading={updateSchool.isPending}
            submitLabel="Save details"
            onSubmit={(values) => updateSchool.mutateAsync(values).then(() => undefined)}
          />
        </Card>
      )}

      {activeTab === "classes" && (
        <SchoolWorkspacesTab
          catalog={catalogQuery.data}
          isLoading={createWorkspace.isPending}
          workspaces={workspacesQuery.data ?? []}
          onCreate={(values) =>
            createWorkspace.mutateAsync({ ...values, school_id: school.id }).then(() => undefined)
          }
        />
      )}

      {activeTab === "learners" && <SchoolLearnersTab schoolId={school.id} />}
    </main>
  );
}
