import { useState } from "react";

import { LiveWork } from "@/features/content-chat/LiveWork";
import { Button } from "@/shared/components/ui/Button";

import { failureLine } from "../failure";
import { useGenerationProgress } from "../hooks/useGenerationProgress";
import { useGenerateContent } from "../hooks/useContent";
import { EXPERT_SOURCES, NOT_CREATED, ContentStatus } from "../status";
import { ContentTypeInfo, ExpertSources } from "../types";
import { MaterialRow } from "./MaterialRow";

const CREATING: ContentStatus = { label: "Creating…", variant: "accent" };
const REFUSED = "Couldn't create it. Try again.";

/** Which expert content a revision note is grounded in; the teacher's lesson note by default. */
function SourcesChoice({
  value,
  onChange,
  noteApproved,
}: {
  value: ExpertSources;
  onChange: (sources: ExpertSources) => void;
  noteApproved: boolean;
}) {
  return (
    <label className="flex flex-wrap items-center gap-2 text-xs text-(--ink-2)">
      Grounded in
      <select
        value={value}
        onChange={(event) => onChange(event.target.value as ExpertSources)}
        className="rounded-md border border-(--line) bg-(--surface) px-2 py-1 text-xs text-(--ink)"
      >
        {EXPERT_SOURCES.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      <span className="text-(--muted)">
        {value === "textbook"
          ? "The lesson note is not read."
          : noteApproved
            ? "Your approved lesson note is read; a step it does not cover uses the textbook."
            : "Your lesson note is not approved yet, so the textbook is used until it is."}
      </span>
    </label>
  );
}

/**
 * A material not made yet: one button to make it, options behind a link, and the agent at work
 * in the row while it writes. When the agent stops short, its work stays with the reason.
 */
export function CreateMaterial({
  info,
  planVersionId,
  noteApproved,
}: {
  info: ContentTypeInfo;
  planVersionId: string;
  noteApproved: boolean;
}) {
  const generate = useGenerateContent(planVersionId, info.type);
  const [sources, setSources] = useState<ExpertSources>("lesson-note");
  const [instructions, setInstructions] = useState("");
  const [optionsOpen, setOptionsOpen] = useState(false);
  const choosesSources = info.type === "revision-note";
  const takesInstructions = info.engine === "mcp";
  const failure = generate.failure ?? (generate.isError ? REFUSED : null);
  const progress = useGenerationProgress(
    planVersionId,
    info.type,
    generate.isPending && takesInstructions,
    failure !== null && !generate.isPending && takesInstructions,
  );
  const stopped = !generate.isPending && failure !== null;
  const label = info.label.toLowerCase();

  return (
    <MaterialRow
      info={info}
      status={generate.isPending ? CREATING : NOT_CREATED}
      action={
        <Button
          size="sm"
          variant="secondary"
          isLoading={generate.isPending}
          onClick={() =>
            generate.create({
              sources: choosesSources ? sources : undefined,
              instructions:
                takesInstructions && instructions.trim()
                  ? instructions.trim()
                  : undefined,
            })
          }
        >
          {generate.isPending ? "Creating…" : stopped ? "Try again" : "Create it"}
        </Button>
      }
    >
      {!generate.isPending && (choosesSources || takesInstructions) ? (
        <button
          type="button"
          onClick={() => setOptionsOpen((open) => !open)}
          className="text-xs text-(--accent-deep) hover:underline"
        >
          {optionsOpen
            ? "Hide options"
            : takesInstructions
              ? "Add instructions"
              : "Options"}
        </button>
      ) : null}
      {optionsOpen && !generate.isPending && choosesSources ? (
        <SourcesChoice
          value={sources}
          onChange={setSources}
          noteApproved={noteApproved}
        />
      ) : null}
      {optionsOpen && !generate.isPending && takesInstructions ? (
        <label className="block space-y-1 text-xs text-(--ink-2)">
          Tell the agent what you want
          <textarea
            value={instructions}
            onChange={(event) => setInstructions(event.target.value)}
            rows={3}
            maxLength={4000}
            placeholder="For example: three questions, one of them on word problems, with prices in naira."
            className="block w-full rounded-md border border-(--line) bg-(--surface) px-2 py-1.5 text-sm text-(--ink)"
          />
        </label>
      ) : null}
      {takesInstructions && (generate.isPending || (stopped && progress.length > 0)) ? (
        <LiveWork
          events={progress}
          stopped={stopped}
          title={
            stopped
              ? `The agent could not finish the ${label}`
              : `The agent is writing the ${label}`
          }
          footer={
            stopped
              ? failureLine(failure ?? REFUSED)
              : "It takes a few minutes. When it is made, keep talking to the same agent from its page."
          }
        />
      ) : stopped ? (
        <p className="text-xs text-(--danger-ink)">
          {failureLine(failure ?? REFUSED)}
        </p>
      ) : null}
    </MaterialRow>
  );
}
