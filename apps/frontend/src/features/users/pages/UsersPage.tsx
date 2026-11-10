import { useState } from "react";

import { useExperiments } from "@/features/experiments/hooks/useExperiments";
import { Badge } from "@/shared/components/ui/Badge";

import { useUsers } from "../hooks/useUsers";
import { ONBOARDABLE_ROLES, OnboardableRole, UserSummary } from "../types";
import { CreateUserForm } from "./CreateUserForm";

const ROLE_FILTERS: readonly { value: string; label: string }[] = [
  { value: "", label: "All roles" },
  { value: "research_manager", label: "Researchers" },
  { value: "teacher", label: "Teachers" },
  { value: "rater", label: "Raters" },
  { value: "admin", label: "Admins" },
  { value: "student", label: "Students" },
] as const;

/** Admin-only: every user across every role, filterable, with a quick onboard form. */
export function UsersPage() {
  const [roleFilter, setRoleFilter] = useState<string>("");
  const [experimentFilter, setExperimentFilter] = useState<string>("");
  const [creating, setCreating] = useState(false);
  const { data: users, isLoading, isError } = useUsers(
    roleFilter || null,
    experimentFilter || null
  );

  return (
    <main className="flex w-full flex-col gap-6 py-8">
      <header className="flex flex-wrap items-end justify-between gap-3">
        <div className="space-y-1">
          <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-(--accent)">
            Admin · Users
          </p>
          <h1 className="text-2xl font-semibold text-(--ink)">Manage users</h1>
          <p className="text-sm text-(--muted)">
            Every researcher, teacher, rater, student and admin identity. New users
            arrive with a login code; raters automatically get an evaluation profile.
          </p>
        </div>
        <button
          type="button"
          onClick={() => setCreating((value) => !value)}
          className="inline-flex h-9 items-center bg-(--accent) px-4 text-sm font-semibold text-white transition hover:bg-(--accent-bright)"
        >
          {creating ? "Cancel" : "Add user"}
        </button>
      </header>

      {creating ? (
        <CreateUserForm
          onSuccess={() => setCreating(false)}
          onCancel={() => setCreating(false)}
        />
      ) : null}

      <div className="flex flex-wrap items-center gap-2 text-sm">
        <span className="text-(--muted)">Role:</span>
        {ROLE_FILTERS.map((option) => (
          <button
            key={option.value}
            type="button"
            onClick={() => {
              setRoleFilter(option.value);
              // Experiment scoping only applies to students; clear when leaving.
              if (option.value !== "student") setExperimentFilter("");
            }}
            className={`border px-3 py-1 transition ${
              roleFilter === option.value
                ? "border-(--accent) bg-(--accent-soft) font-semibold text-(--accent)"
                : "border-(--line-2) bg-(--surface) text-(--ink-2) hover:border-(--accent)"
            }`}
          >
            {option.label}
          </button>
        ))}
      </div>

      {roleFilter === "student" ? (
        <ExperimentFilter
          value={experimentFilter}
          onChange={setExperimentFilter}
        />
      ) : null}

      {isLoading ? (
        <p className="text-sm text-(--muted)">Loading users…</p>
      ) : isError ? (
        <p className="text-sm text-(--danger)">Couldn&apos;t load users.</p>
      ) : !users?.length ? (
        <p className="text-sm text-(--muted)">No users match this filter.</p>
      ) : (
        <UserTable users={users} />
      )}
    </main>
  );
}

/** Narrows the student list to one experiment's participants. */
function ExperimentFilter({
  value,
  onChange,
}: {
  value: string;
  onChange: (next: string) => void;
}) {
  const { data: experiments, isLoading } = useExperiments({});
  return (
    <div className="flex flex-wrap items-center gap-2 text-sm">
      <span className="text-(--muted)">In experiment:</span>
      <select
        value={value}
        onChange={(event) => onChange(event.target.value)}
        disabled={isLoading}
        className="h-9 min-w-64 border border-(--line-2) bg-(--surface) px-3 text-sm text-(--ink) outline-none focus:border-(--accent)"
      >
        <option value="">Any experiment</option>
        {experiments?.map((experiment) => (
          <option key={experiment.experiment_id} value={experiment.experiment_id}>
            {experiment.experiment_code}
            {experiment.lesson_title ? ` · ${experiment.lesson_title}` : ""}
          </option>
        ))}
      </select>
    </div>
  );
}

function UserTable({ users }: { users: UserSummary[] }) {
  return (
    <div className="overflow-x-auto border border-(--line) bg-(--surface)">
      <table className="w-full text-left text-sm">
        <thead className="border-b border-(--line) text-[11px] font-semibold uppercase tracking-[0.08em] text-(--muted)">
          <tr>
            <th className="px-4 py-3">Name</th>
            <th className="px-4 py-3">Email</th>
            <th className="px-4 py-3">Code</th>
            <th className="px-4 py-3">Role</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <UserRow key={user.id} user={user} />
          ))}
        </tbody>
      </table>
    </div>
  );
}

/** One user row. The role-linked id (EVR / STU) appears as muted subtext under
 *  the role badge — a reference handle, not a link. */
function UserRow({ user }: { user: UserSummary }) {
  const profileId = user.rater_id ?? user.student_id ?? null;
  return (
    <tr className="border-b border-(--line) last:border-b-0 align-top">
      <td className="px-4 py-3 font-medium text-(--ink)">
        {user.full_name ?? "—"}
      </td>
      <td className="px-4 py-3 font-mono text-xs text-(--muted)">
        {user.email ?? "—"}
      </td>
      <td className="px-4 py-3 font-mono text-xs text-(--ink-2)">
        {extractCode(user.auth_id)}
      </td>
      <td className="px-4 py-3">
        <Badge variant={user.role === "research_manager" ? "accent" : "outline"}>
          {user.role}
        </Badge>
        {profileId ? (
          <div className="mt-1 font-mono text-[11px] text-(--muted)">
            {profileId}
          </div>
        ) : null}
      </td>
    </tr>
  );
}

/** ``auth_id`` is shaped ``code|<value>`` for the login-code provider; surface
 *  just the value as the user-facing code, or fall back to the raw id. */
function extractCode(authId: string): string {
  const idx = authId.indexOf("|");
  return idx >= 0 ? authId.slice(idx + 1) : authId;
}

// Re-export the onboardable roles enum constant so the form's import is local.
export { ONBOARDABLE_ROLES };
export type { OnboardableRole };
