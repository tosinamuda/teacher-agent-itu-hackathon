import { useState } from "react";

import {
  useContentTypes,
  useSetDefaultGenerator,
} from "@/features/content/hooks/useContent";
import type { ContentTypeInfo, GeneratorInfo } from "@/features/content/types";
import { Badge } from "@/shared/components/ui/Badge";
import { Button } from "@/shared/components/ui/Button";

import { problemsOf } from "../lib/problems";

const NATIVE =
  "One DSPy pipeline from the study is never made the default in place of another.";

/** Researcher: for each kind of content, how it can be made and which way new content uses. */
export function GeneratorsPanel() {
  const types = useContentTypes();
  const choose = useSetDefaultGenerator();
  const [problems, setProblems] = useState<string[]>([]);
  const choices = (types.data ?? []).filter(
    (type) => !type.retired && type.generators.length > 0,
  );

  if (choices.length === 0) return null;
  return (
    <section className="flex flex-col gap-3">
      <p className="max-w-2xl text-sm text-(--muted)">
        Each kind of content can have more than one generator. New content is
        made with the default; content already made keeps the generator it
        records.
      </p>
      {problems.length > 0 ? (
        <div
          role="alert"
          className="border border-[#e7c9c5] bg-(--danger-tint) p-3 text-sm text-(--danger-ink)"
        >
          {problems.join(" ")}
        </div>
      ) : null}
      <div className="overflow-x-auto border border-(--line) bg-(--surface)">
        <table className="w-full text-left text-sm">
          <thead className="border-b border-(--line) text-[11px] font-semibold uppercase tracking-[0.08em] text-(--muted)">
            <tr>
              <th className="px-4 py-3">Content type</th>
              <th className="px-4 py-3">Generator</th>
              <th className="px-4 py-3">Made with</th>
              <th className="px-4 py-3">Status</th>
              <th className="px-4 py-3 text-right">Default</th>
            </tr>
          </thead>
          <tbody>
            {choices.flatMap((type) =>
              type.generators.map((generator) => (
                <GeneratorRow
                  key={`${type.type}-${generator.level}-${generator.ref}`}
                  type={type}
                  generator={generator}
                  busy={choose.isPending}
                  onChoose={() => {
                    setProblems([]);
                    choose.mutate(
                      {
                        type: type.type,
                        level: generator.level,
                        generator: generator.ref,
                      },
                      { onError: (error) => setProblems(problemsOf(error)) },
                    );
                  }}
                />
              )),
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function GeneratorRow({
  type,
  generator,
  busy,
  onChoose,
}: {
  type: ContentTypeInfo;
  generator: GeneratorInfo;
  busy: boolean;
  onChoose: () => void;
}) {
  const isDefault = generator.status === "default";
  const native = generator.harness === "dspy-pipeline";
  const defaultIsNative = type.generators.some(
    (other) =>
      other.level === generator.level &&
      other.status === "default" &&
      other.harness === "dspy-pipeline",
  );
  const locked = native && defaultIsNative;

  return (
    <tr className="border-b border-(--line) last:border-b-0">
      <td className="px-4 py-3">
        <div className="text-(--ink)">{type.label}</div>
        <div className="font-mono text-[11px] text-(--muted)">
          {type.type} · {generator.level}
        </div>
      </td>
      <td className="px-4 py-3 font-mono text-[12px] text-(--ink-2)">
        {generator.ref}
      </td>
      <td className="px-4 py-3 text-(--ink-2)">
        {native ? "DSPy pipeline" : "Content engine"} ·{" "}
        {generator.schema_source === "code"
          ? "schema in code"
          : "schema from a spec"}
        {generator.spec_revision !== null
          ? ` · spec ${generator.spec_revision}`
          : ""}
      </td>
      <td className="px-4 py-3">
        <Badge variant={isDefault ? "success" : "outline"}>
          {isDefault
            ? "Default"
            : generator.status === "retired"
              ? "Retired"
              : "Available"}
        </Badge>
      </td>
      <td className="px-4 py-3 text-right">
        {isDefault ? null : (
          <Button
            size="sm"
            variant="outline"
            disabled={locked || busy || generator.status === "retired"}
            title={locked ? NATIVE : undefined}
            onClick={onChoose}
          >
            Make default
          </Button>
        )}
      </td>
    </tr>
  );
}
