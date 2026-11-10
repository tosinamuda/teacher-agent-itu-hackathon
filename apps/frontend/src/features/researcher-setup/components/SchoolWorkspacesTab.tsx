import { Card } from "@/shared/components/ui/Card";

import { SchoolSetupCatalog, SchoolSetupWorkspace } from "../types";
import { AddTeacherForm } from "./AddTeacherForm";
import { SchoolWorkspaceForm } from "./SchoolWorkspaceForm";

type SchoolWorkspacesTabProps = {
  catalog?: SchoolSetupCatalog;
  isLoading: boolean;
  workspaces: SchoolSetupWorkspace[];
  onCreate: (
    values: {
      class_name: string;
      grade_level_name: string;
      subject_code: string;
      term: string;
      academic_year: string;
      teacher_id: string;
    }
  ) => Promise<void>;
};

/** Renders the workspace management tab for a selected school. */
export function SchoolWorkspacesTab({
  catalog,
  isLoading,
  workspaces,
  onCreate,
}: SchoolWorkspacesTabProps) {
  return (
    <Card variant="glass" padding="lg" className="space-y-5">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[color:var(--muted)]">
          Classes &amp; teachers
        </p>
        <h2 className="mt-1 text-lg font-semibold text-[color:var(--ink)]">
          Set up a class: add its teacher, then create the class workspace
        </h2>
      </div>
      <div className="space-y-2 border-b border-(--line) pb-5">
        <h3 className="text-xs font-semibold uppercase tracking-[0.16em] text-(--accent-deep)">
          Step 1 · Onboard the teacher
        </h3>
        <p className="text-xs text-(--muted)">
          Add the teacher first if they&apos;re not in the list below — their login code is how
          they sign in to author and freeze their lesson plans.
        </p>
        <AddTeacherForm />
      </div>
      <div className="space-y-2">
        <h3 className="text-xs font-semibold uppercase tracking-[0.16em] text-(--accent-deep)">
          Step 2 · Create the class workspace
        </h3>
        <p className="text-xs text-(--muted)">
          Name the class and attach its subject, term, and the teacher you added above.
        </p>
        <SchoolWorkspaceForm catalog={catalog} isLoading={isLoading} onSubmit={onCreate} />
      </div>
      <div className="space-y-3">
        <h3 className="text-base font-semibold text-[color:var(--ink)]">Existing workspaces</h3>
        {workspaces.length === 0 ? (
          <p className="text-sm text-[color:var(--muted)]">
            No workspaces have been created for this school yet.
          </p>
        ) : (
          workspaces.map((workspace) => (
            <div
              key={workspace.workspace_id}
              className="rounded-3xl border border-[color:var(--line)] bg-(--surface) p-4 text-sm text-[color:var(--muted)]"
            >
              <p className="font-semibold text-[color:var(--ink)]">{workspace.workspace_name}</p>
              <p className="mt-1">
                {workspace.class_name} · {workspace.subject_name} · {workspace.term} ·{" "}
                {workspace.academic_year}
              </p>
              <p className="mt-1">{workspace.teacher_name ?? "Teacher"}</p>
            </div>
          ))
        )}
      </div>
    </Card>
  );
}
