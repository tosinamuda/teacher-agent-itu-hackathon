import { useState } from "react";
import { useStudentAuth } from "../context/StudentContext";
import { Button } from "@/shared/components/ui/Button";
import { Card } from "@/shared/components/ui/Card";

export default function StudentLoginPage() {
  const { login, error, isLoading } = useStudentAuth();
  const [code, setCode] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!code.trim()) return;
    await login(code.trim());
  };

  return (
    <main className="min-h-screen flex items-center justify-center p-6 bg-(--bg)">
      <Card className="w-full max-w-md p-8 animate-fade-up">
        <div className="text-center mb-8">
          <div className="mb-4 text-xs font-semibold uppercase tracking-wider text-(--accent)">
            Student Portal
          </div>
          <h1 className="text-2xl font-bold text-(--ink)">Welcome back</h1>
          <p className="text-(--muted) text-sm mt-2">
            Enter your student code to access your lessons.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <label htmlFor="code" className="text-sm font-medium text-(--ink-2)">
              Student Code
            </label>
            <input
              id="code"
              type="text"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder="e.g. ST-0aa8a863"
              className="w-full px-4 py-3 border border-(--line-2) bg-(--surface) focus:outline-hidden focus:ring-2 focus:ring-(--accent) focus:border-(--accent) transition-colors font-mono"
            />
          </div>

          {error && (
            <div className="p-3 border border-(--danger-tint) bg-(--danger-tint) text-(--danger-ink) text-sm">
              {error}
            </div>
          )}

          <Button
            type="submit"
            disabled={!code}
            isLoading={isLoading}
            className="w-full justify-center py-3"
          >
            {isLoading ? "Verifying…" : "Continue"}
          </Button>
        </form>

        <p className="mt-8 text-center text-xs text-(--muted)">
          Don&apos;t have a code? Ask your teacher.
        </p>
      </Card>
    </main>
  );
}
