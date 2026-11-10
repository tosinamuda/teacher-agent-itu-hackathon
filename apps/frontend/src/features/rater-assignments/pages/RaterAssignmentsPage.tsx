import { useMemo, useState } from "react";

import { useExperiment } from "@/features/experiments/hooks/useExperiments";

import { getBlindingKey } from "../api";
import {
  useAssignAudit,
  useAssignBundle,
  useAssignH1,
  useAssignH2,
  useExperimentAssignments,
  useRaters,
} from "../hooks/useRaterAssignments";
import { ConcludedRaters } from "../components/ConcludedRaters";
import { RaterChips, SECTION_CLASS } from "../components/RaterChips";
import type {
  AssignedRater,
  AuditAssignmentSlot,
  H1AssignmentSlot,
  H2AssignmentSlot,
  RaterOption,
} from "../types";

const SELECT_CLASS =
  "h-9 min-w-48 border border-(--line-2) bg-(--surface) px-3 text-sm text-(--ink) outline-none focus:border-(--accent)";
const ASSIGN_BTN_CLASS =
  "inline-flex h-9 items-center bg-(--accent) px-3 text-sm font-semibold text-white transition hover:bg-(--accent-bright) disabled:opacity-50";

/** Admin / researcher view: assign raters to every slot of one experiment.
 *  Renders the protocol's three sections — H1 lesson, H2 focal cases, audit
 *  items — each with its current raters and an inline picker.
 */
export function RaterAssignmentsPage({ experimentId }: { experimentId: string }) {
  const { data: view, isLoading, isError } = useExperimentAssignments(experimentId);
  const { data: raters } = useRaters();
  const { data: experiment } = useExperiment(experimentId);

  if (isLoading) {
    return <main className="py-10 text-sm text-(--muted)">Loading assignments…</main>;
  }
  if (isError || !view) {
    return (
      <main className="py-10 text-sm text-(--danger)">
        Couldn&apos;t load the assignment view for this experiment.
      </main>
    );
  }

  return (
    <main className="flex w-full flex-col gap-8 py-6">
      {experiment?.lifecycle_status === "ended" ? (
        <ConcludedRaters experiment={experiment} view={view} />
      ) : (
        <>
          <p className="text-sm text-(--muted)">
            Up to 3 raters for the lesson and for each focal learner; each audit item takes 2
            raters and an adjudicator.
          </p>
          <BundleSection experimentId={experimentId} raters={raters ?? []} />
          <BlindingKeySection experimentId={experimentId} />
          <H1Section
            experimentId={experimentId}
            slot={view.h1}
            raters={raters ?? []}
          />
          <H2Section
            experimentId={experimentId}
            slots={view.h2}
            raters={raters ?? []}
          />
          <AuditSection
            experimentId={experimentId}
            slots={view.audit}
            raters={raters ?? []}
          />
        </>
      )}
    </main>
  );
}

/** RESEARCHER-ONLY: download the candidate-label -> condition key as CSV so
 *  printed offline worksheets ("Candidate A/B…") can be transcribed correctly.
 *  Never share this with raters — it unblinds the study. */
function BlindingKeySection({ experimentId }: { experimentId: string }) {
  const [isDownloading, setIsDownloading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const download = async () => {
    setIsDownloading(true);
    setError(null);
    try {
      const rows = await getBlindingKey(experimentId);
      const header = [
        "rater_name",
        "rater_id",
        "hypothesis",
        "group",
        "packet_code",
        "candidate_label",
        "condition_code",
      ];
      const csv = [
        header.join(","),
        ...rows.map((row) =>
          [
            row.rater_name,
            row.rater_id,
            row.hypothesis,
            row.group,
            row.packet_code,
            row.candidate_label,
            row.condition_code,
          ]
            .map((value) => `"${String(value).replaceAll('"', '""')}"`)
            .join(",")
        ),
      ].join("\n");
      const blob = new Blob([csv], { type: "text/csv" });
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = `${experimentId}-blinding-key.csv`;
      anchor.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Couldn't load the blinding key.");
    } finally {
      setIsDownloading(false);
    }
  };

  return (
    <section className={SECTION_CLASS}>
      <h2 className="text-lg font-semibold text-(--ink)">Blinding key (researcher only)</h2>
      <p className="text-sm text-(--muted)">
        Printed worksheets show only anonymous candidate labels. This CSV maps each
        assigned rater&apos;s &quot;Candidate A/B/…&quot; back to the real condition
        (C0–C3 / P0–P1) for transcribing offline ratings.{" "}
        <strong>Never share it with raters.</strong>
      </p>
      <div className="flex items-center gap-3">
        <button
          className={ASSIGN_BTN_CLASS}
          disabled={isDownloading}
          onClick={() => void download()}
          type="button"
        >
          {isDownloading ? "Preparing…" : "Download blinding key (CSV)"}
        </button>
        {error ? <span className="text-sm text-(--danger)">{error}</span> : null}
      </div>
    </section>
  );
}

/** One-action fan-out: assign a rater to the lesson + every focal case at once.
 *  Run it once per rater — three raters gives every candidate its 3 ratings. */
function BundleSection({
  experimentId,
  raters,
}: {
  experimentId: string;
  raters: RaterOption[];
}) {
  const [raterId, setRaterId] = useState("");
  const [includeAudit, setIncludeAudit] = useState(false);
  const assign = useAssignBundle(experimentId);

  return (
    <section className={SECTION_CLASS}>
      <h2 className="text-lg font-semibold text-(--ink)">Assign to whole experiment</h2>
      <p className="text-sm text-(--muted)">
        One action assigns the selected rater to the H1 lesson and every H2 focal
        learner (optionally every audit item). Repeat per rater — three raters give
        every candidate its three expert ratings.
      </p>
      <div className="flex flex-wrap items-center gap-3">
        <select
          className={SELECT_CLASS}
          value={raterId}
          onChange={(event) => setRaterId(event.target.value)}
        >
          <option value="">Select a rater…</option>
          {raters.map((rater) => (
            <option key={rater.rater_id} value={rater.rater_id}>
              {rater.display_name}
            </option>
          ))}
        </select>
        <label className="flex items-center gap-2 text-sm text-(--ink-2)">
          <input
            checked={includeAudit}
            onChange={(event) => setIncludeAudit(event.target.checked)}
            type="checkbox"
          />
          Include audit items
        </label>
        <button
          className={ASSIGN_BTN_CLASS}
          disabled={!raterId || assign.isPending}
          onClick={() => assign.mutate({ raterId, includeAudit })}
          type="button"
        >
          {assign.isPending ? "Assigning…" : "Assign to everything"}
        </button>
        {assign.isSuccess ? (
          <span className="text-sm text-(--accent-deep)">
            Assigned — lesson {assign.data.h1_assigned ? "✓" : "—"} · {assign.data.h2_assigned}{" "}
            focal case{assign.data.h2_assigned === 1 ? "" : "s"}
            {assign.data.audit_assigned ? ` · ${assign.data.audit_assigned} audit items` : ""}
          </span>
        ) : null}
        {assign.isError ? (
          <span className="text-sm text-(--danger)">
            {assign.error instanceof Error ? assign.error.message : "Couldn't assign."}
          </span>
        ) : null}
      </div>
    </section>
  );
}

function H1Section({
  experimentId,
  slot,
  raters,
}: {
  experimentId: string;
  slot: H1AssignmentSlot | null;
  raters: RaterOption[];
}) {
  const assign = useAssignH1(experimentId);

  if (slot === null) {
    return (
      <section className={SECTION_CLASS}>
        <h2 className="text-lg font-semibold text-(--ink)">H1 · Lesson</h2>
        <p className="text-sm text-(--muted)">
          No lesson is bound to this experiment yet — assign one from the
          experiment detail page first.
        </p>
      </section>
    );
  }

  const available = filterAvailable(raters, slot.raters);
  return (
    <section className={SECTION_CLASS}>
      <header className="flex items-baseline justify-between gap-3">
        <h2 className="text-lg font-semibold text-(--ink)">
          H1 · {slot.lesson_title ?? "Lesson"}
        </h2>
        <span className="text-xs text-(--muted)">
          {slot.raters.length} / {slot.capacity} raters
        </span>
      </header>
      <RaterChips raters={slot.raters} />
      <SlotPicker
        options={available}
        disabled={slot.raters.length >= slot.capacity}
        pending={assign.isPending}
        onAssign={(raterId) =>
          assign.mutate({ raterId, lessonPeriodId: slot.lesson_period_id })
        }
      />
    </section>
  );
}

function H2Section({
  experimentId,
  slots,
  raters,
}: {
  experimentId: string;
  slots: H2AssignmentSlot[];
  raters: RaterOption[];
}) {
  if (slots.length === 0) {
    return (
      <section className={SECTION_CLASS}>
        <h2 className="text-lg font-semibold text-(--ink)">H2 · Focal cases</h2>
        <p className="text-sm text-(--muted)">
          No focal learners selected yet. Pick them on the experiment detail page
          and they&apos;ll appear here.
        </p>
      </section>
    );
  }
  return (
    <section className={SECTION_CLASS}>
      <h2 className="text-lg font-semibold text-(--ink)">H2 · Focal cases</h2>
      <div className="space-y-4">
        {slots.map((slot) => (
          <H2SlotRow
            key={slot.focal_case_id}
            experimentId={experimentId}
            slot={slot}
            raters={raters}
          />
        ))}
      </div>
    </section>
  );
}

function H2SlotRow({
  experimentId,
  slot,
  raters,
}: {
  experimentId: string;
  slot: H2AssignmentSlot;
  raters: RaterOption[];
}) {
  const assign = useAssignH2(experimentId);
  const available = filterAvailable(raters, slot.raters);
  return (
    <div className="border border-(--line-2) bg-(--bg) p-4">
      <header className="flex items-baseline justify-between gap-3">
        <div>
          <p className="font-medium text-(--ink)">
            {slot.student_full_name ?? slot.student_id}
          </p>
          <p className="text-xs uppercase tracking-wide text-(--muted)">
            {slot.focal_case_type}
            {slot.student_full_name ? (
              <span className="ml-2 font-mono normal-case tracking-normal text-[11px]">
                · {slot.student_id}
              </span>
            ) : null}
          </p>
        </div>
        <span className="text-xs text-(--muted)">
          {slot.raters.length} / {slot.capacity} raters
        </span>
      </header>
      <div className="mt-2">
        <RaterChips raters={slot.raters} />
      </div>
      <div className="mt-3">
        <SlotPicker
          options={available}
          disabled={slot.raters.length >= slot.capacity}
          pending={assign.isPending}
          onAssign={(raterId) =>
            assign.mutate({ raterId, focalCaseId: slot.focal_case_id })
          }
        />
      </div>
    </div>
  );
}

function AuditSection({
  experimentId,
  slots,
  raters,
}: {
  experimentId: string;
  slots: AuditAssignmentSlot[];
  raters: RaterOption[];
}) {
  if (slots.length === 0) {
    return (
      <section className={SECTION_CLASS}>
        <h2 className="text-lg font-semibold text-(--ink)">Audit · Source items</h2>
        <p className="text-sm text-(--muted)">
          No source-audit items have been generated for this experiment yet.
        </p>
      </section>
    );
  }
  return (
    <section className={SECTION_CLASS}>
      <h2 className="text-lg font-semibold text-(--ink)">Audit · Source items</h2>
      <div className="space-y-4">
        {slots.map((slot, index) => (
          <AuditSlotRow
            key={slot.audit_item_id}
            experimentId={experimentId}
            slot={slot}
            index={index}
            raters={raters}
          />
        ))}
      </div>
    </section>
  );
}

function AuditSlotRow({
  experimentId,
  slot,
  index,
  raters,
}: {
  experimentId: string;
  slot: AuditAssignmentSlot;
  index: number;
  raters: RaterOption[];
}) {
  const assign = useAssignAudit(experimentId);
  // Audit slot picker exposes a role-toggle since one item has two cap slots.
  const [role, setRole] = useState<"rater" | "adjudicator">("rater");
  const taken = useMemo(
    () => [...slot.raters, ...slot.adjudicators],
    [slot.raters, slot.adjudicators]
  );
  const available = filterAvailable(raters, taken);
  const targetIsAdjudicator = role === "adjudicator";
  const targetFull = targetIsAdjudicator
    ? slot.adjudicators.length >= slot.adjudicator_capacity
    : slot.raters.length >= slot.capacity;
  return (
    <div className="border border-(--line-2) bg-(--bg) p-4">
      <header className="flex items-baseline justify-between gap-3">
        <div>
          <p className="font-medium text-(--ink)">Audit item #{index + 1}</p>
          <p className="font-mono text-[11px] text-(--muted)">{slot.audit_item_id}</p>
        </div>
        <span className="text-xs text-(--muted)">
          {slot.raters.length} / {slot.capacity} raters ·{" "}
          {slot.adjudicators.length} / {slot.adjudicator_capacity} adjudicator
        </span>
      </header>
      <div className="mt-2 space-y-2">
        <RaterChips raters={slot.raters} />
        <RaterChips raters={slot.adjudicators} />
      </div>
      <div className="mt-3 flex flex-wrap items-center gap-2">
        <select
          value={role}
          onChange={(event) =>
            setRole(event.target.value === "adjudicator" ? "adjudicator" : "rater")
          }
          className={SELECT_CLASS}
        >
          <option value="rater">As rater</option>
          <option value="adjudicator">As adjudicator</option>
        </select>
        <SlotPicker
          options={available}
          disabled={targetFull}
          pending={assign.isPending}
          onAssign={(raterId) =>
            assign.mutate({
              auditItemId: slot.audit_item_id,
              raterId,
              isAdjudicator: targetIsAdjudicator,
            })
          }
        />
      </div>
    </div>
  );
}

/** Picker = select + assign button. State stays local so submission can clear it. */
function SlotPicker({
  options,
  disabled,
  pending,
  onAssign,
}: {
  options: RaterOption[];
  disabled: boolean;
  pending: boolean;
  onAssign: (raterId: string) => void;
}) {
  const [selected, setSelected] = useState<string>("");
  const submit = () => {
    if (!selected) return;
    onAssign(selected);
    setSelected("");
  };
  if (disabled) {
    return (
      <p className="text-xs italic text-(--muted)">
        Slot at capacity — remove a rater to add another.
      </p>
    );
  }
  if (options.length === 0) {
    return (
      <p className="text-xs italic text-(--muted)">
        Every rater is already assigned here.
      </p>
    );
  }
  return (
    <div className="flex flex-wrap items-center gap-2">
      <select
        value={selected}
        onChange={(event) => setSelected(event.target.value)}
        className={SELECT_CLASS}
        disabled={pending}
      >
        <option value="">Select a rater…</option>
        {options.map((rater) => (
          <option key={rater.rater_id} value={rater.rater_id}>
            {rater.display_name}
          </option>
        ))}
      </select>
      <button
        type="button"
        onClick={submit}
        disabled={!selected || pending}
        className={ASSIGN_BTN_CLASS}
      >
        {pending ? "Assigning…" : "Assign"}
      </button>
    </div>
  );
}

/** Drop raters already on the slot — the picker should only offer fresh ones. */
function filterAvailable(
  all: RaterOption[],
  taken: AssignedRater[]
): RaterOption[] {
  const takenIds = new Set(taken.map((r) => r.rater_id));
  return all.filter((rater) => !takenIds.has(rater.rater_id));
}
