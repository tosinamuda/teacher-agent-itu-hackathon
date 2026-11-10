import { useState } from "react";

import { useCreateUser, usePickableLearners } from "../hooks/useUsers";
import { ONBOARDABLE_ROLES, OnboardableRole } from "../types";

const fieldClass =
  "h-10 w-full border border-(--line-2) bg-(--surface) px-3 text-sm text-(--ink) outline-none focus:border-(--accent)";

const ROLE_LABELS: Record<OnboardableRole, string> = {
  research_manager: "Researcher",
  teacher: "Teacher",
  rater: "Rater",
  admin: "Admin",
  student: "Student",
};

/** Small inline form: code · email · full name · role (+ student profile for
 *  role=student). Posts ``/auth/users``; the backend grants the Casbin role and
 *  binds the student profile in the same request. */
export function CreateUserForm({
  onSuccess,
  onCancel,
}: {
  onSuccess: () => void;
  onCancel: () => void;
}) {
  const [code, setCode] = useState("");
  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");
  const [role, setRole] = useState<OnboardableRole>("teacher");
  const [studentId, setStudentId] = useState("");
  const create = useCreateUser();
  const learners = usePickableLearners(role === "student");

  const submit = async (event: React.FormEvent) => {
    event.preventDefault();
    await create.mutateAsync({
      code: code.trim(),
      email: email.trim(),
      full_name: fullName.trim() || null,
      role,
      student_id: role === "student" ? studentId : null,
    });
    setCode("");
    setEmail("");
    setFullName("");
    setStudentId("");
    onSuccess();
  };

  return (
    <form
      onSubmit={submit}
      className="space-y-4 border border-(--line) bg-(--surface) p-5"
    >
      <div className="grid gap-3 md:grid-cols-2">
        <label className="block space-y-1">
          <span className="text-xs font-semibold uppercase tracking-[0.14em] text-(--muted)">
            Login code
          </span>
          <input
            required
            className={fieldClass}
            placeholder="e.g. dr-okonkwo"
            value={code}
            onChange={(event) => setCode(event.target.value)}
          />
        </label>
        <label className="block space-y-1">
          <span className="text-xs font-semibold uppercase tracking-[0.14em] text-(--muted)">
            Email
          </span>
          <input
            required
            type="email"
            className={fieldClass}
            placeholder="name@school.com"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
          />
        </label>
        <label className="block space-y-1">
          <span className="text-xs font-semibold uppercase tracking-[0.14em] text-(--muted)">
            Full name (optional)
          </span>
          <input
            className={fieldClass}
            value={fullName}
            onChange={(event) => setFullName(event.target.value)}
          />
        </label>
        <label className="block space-y-1">
          <span className="text-xs font-semibold uppercase tracking-[0.14em] text-(--muted)">
            Role
          </span>
          <select
            className={fieldClass}
            value={role}
            onChange={(event) => setRole(event.target.value as OnboardableRole)}
          >
            {ONBOARDABLE_ROLES.map((r) => (
              <option key={r} value={r}>
                {ROLE_LABELS[r]}
              </option>
            ))}
          </select>
        </label>
      </div>
      {role === "student" ? (
        <label className="block space-y-1">
          <span className="text-xs font-semibold uppercase tracking-[0.14em] text-(--muted)">
            Student profile
          </span>
          <select
            required
            className={fieldClass}
            value={studentId}
            onChange={(event) => setStudentId(event.target.value)}
          >
            <option value="">
              {learners.isLoading ? "Loading learners…" : "Select a learner…"}
            </option>
            {(learners.data ?? []).map((learner) => (
              <option key={learner.student_id} value={learner.student_id}>
                {learner.full_name}
                {learner.class_name ? ` · ${learner.class_name}` : ""} · {learner.student_id}
                {learner.code ? " · has portal code" : ""}
              </option>
            ))}
          </select>
          <span className="block text-xs text-(--muted)">
            The login code above becomes this learner&apos;s sign-in AND portal code —
            one identity, so their submissions are attributed correctly.
          </span>
        </label>
      ) : null}
      {role === "rater" ? (
        <p className="text-xs text-(--muted)">
          Raters get an evaluation profile automatically. A researcher can then
          assign them to H1 lessons, H2 focal learners or audit items.
        </p>
      ) : null}
      {create.isError ? (
        <p className="text-sm text-(--danger)">
          {create.error instanceof Error ? create.error.message : "Couldn't create user."}
        </p>
      ) : null}
      <div className="flex items-center gap-3">
        <button
          type="submit"
          disabled={create.isPending}
          className="inline-flex h-9 items-center bg-(--accent) px-4 text-sm font-semibold text-white transition hover:bg-(--accent-bright) disabled:opacity-60"
        >
          {create.isPending ? "Creating…" : "Create user"}
        </button>
        <button
          type="button"
          onClick={onCancel}
          className="text-sm text-(--ink-2) underline-offset-2 hover:text-(--ink) hover:underline"
        >
          Cancel
        </button>
      </div>
    </form>
  );
}
