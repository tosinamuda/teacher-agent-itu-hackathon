// @vitest-environment jsdom
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import type { ReactElement } from "react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { AddTeacherForm } from "./AddTeacherForm";
import { SchoolDetailsForm } from "./SchoolDetailsForm";
import { SchoolLearnerForm } from "./SchoolLearnerForm";
import { SchoolWorkspaceForm } from "./SchoolWorkspaceForm";

vi.mock("../api", async (actual) => ({
  ...(await actual()),
  createTeacher: vi.fn(async () => ({ id: "t-new" })),
}));

afterEach(cleanup);

const inQueryClient = (ui: ReactElement) =>
  render(<QueryClientProvider client={new QueryClient()}>{ui}</QueryClientProvider>);

const input = (placeholder: string) => screen.getByPlaceholderText(placeholder) as HTMLInputElement;

const type = (placeholder: string, value: string) =>
  fireEvent.change(input(placeholder), { target: { value } });

describe("researcher setup forms reset what they show", () => {
  it("clears the learner's code and name after adding one, and keeps the track", async () => {
    const onSubmit = vi.fn(async () => {});
    render(<SchoolLearnerForm classId="c1" grade="JSS1" isLoading={false} onSubmit={onSubmit} />);
    type("Learner code", "stu-9");
    type("Learner full name", "Ada Obi");
    type("Track", "Further");

    fireEvent.click(screen.getByRole("button", { name: "Add learner" }));

    await waitFor(() => expect(onSubmit).toHaveBeenCalled());
    await waitFor(() => expect(input("Learner code").value).toBe(""));
    expect(input("Learner full name").value).toBe("");
    expect(input("Track").value).toBe("Further");
  });

  it("clears the class name after adding a workspace, and keeps the choices", async () => {
    const onSubmit = vi.fn(async () => {});
    render(
      <SchoolWorkspaceForm
        catalog={{
          grade_levels: [{ id: "g1", name: "JSS1" }],
          subjects: [{ id: "s1", name: "Mathematics", code: "MTH" }],
          teachers: [{ id: "t1", full_name: "Mrs Okoro", auth_id: "code|t1", email: "o@x.ng" }],
          academic_years: ["2025/2026"],
          suggested_terms: ["First Term"],
        }}
        isLoading={false}
        onSubmit={onSubmit}
      />
    );
    type("Class name e.g. JSS1A", "JSS1A");
    const [grade, subject, teacher] = screen.getAllByRole("combobox") as HTMLSelectElement[];
    fireEvent.change(grade, { target: { value: "JSS1" } });
    fireEvent.change(subject, { target: { value: "MTH" } });
    fireEvent.change(teacher, { target: { value: "t1" } });

    fireEvent.click(screen.getByRole("button", { name: "Add workspace" }));

    await waitFor(() => expect(onSubmit).toHaveBeenCalled());
    await waitFor(() => expect(input("Class name e.g. JSS1A").value).toBe(""));
    expect([grade.value, subject.value, teacher.value]).toEqual(["JSS1", "MTH", "t1"]);
  });

  it("clears the new teacher's fields after adding them", async () => {
    inQueryClient(<AddTeacherForm />);
    type("Teacher full name", "Mrs Okoro");
    type("Email", "okoro@school.ng");
    type("Login code e.g. mrs-okoro", "mrs-okoro");

    fireEvent.click(screen.getByRole("button", { name: "Add teacher" }));

    await waitFor(() => expect(input("Teacher full name").value).toBe(""));
    expect(input("Email").value).toBe("");
    expect(input("Login code e.g. mrs-okoro").value).toBe("");
  });

  it("shows a school that loads after the form, and submits it", async () => {
    const onSubmit = vi.fn(async () => {});
    const props = { isLoading: false, submitLabel: "Save", onSubmit };
    const { rerender } = render(
      <SchoolDetailsForm initialValues={{ name: "", school_code: "" }} {...props} />
    );

    rerender(
      <SchoolDetailsForm initialValues={{ name: "Greenfield", school_code: "GSS-01" }} {...props} />
    );

    await waitFor(() => expect(input("e.g. Greenfield Secondary School").value).toBe("Greenfield"));
    expect(input("e.g. GSS-01").value).toBe("GSS-01");
    fireEvent.click(screen.getByRole("button", { name: "Save" }));
    await waitFor(() =>
      expect(onSubmit).toHaveBeenCalledWith(
        { name: "Greenfield", school_code: "GSS-01" },
        expect.anything()
      )
    );
  });
});
