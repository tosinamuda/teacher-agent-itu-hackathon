import { Link } from "@/shared/router";

import { EvaluationPacket } from "../lib/experiments";

type ExperimentPacketTableProps = {
  packets: EvaluationPacket[];
  /** Base href for per-condition pack preview links (e.g. `/research/experiments/{id}`). */
  experimentBaseHref?: string;
};

/** Conditions whose pack has a dedicated researcher preview route. */
const PREVIEWABLE = new Set(["C0", "C1", "C2", "C3"]);

/**
 * Pull the bits of `export_refs` a researcher actually wants at a glance —
 * which condition this packet rates and (for H2) which focal case it belongs to.
 */
function readExportRefs(refs: Record<string, unknown> | null | undefined): {
  conditionCode: string | null;
  focalCaseType: string | null;
} {
  if (!refs || typeof refs !== "object") {
    return { conditionCode: null, focalCaseType: null };
  }
  const conditionCode = typeof refs.condition_code === "string" ? refs.condition_code : null;
  const focalCaseType = typeof refs.focal_case_type === "string" ? refs.focal_case_type : null;
  return { conditionCode, focalCaseType };
}

/** Friendly truncation of an id like `EPK-xxxxxxxx…` (full id available via `title`). */
function shortId(id: string): string {
  if (id.length <= 18) return id;
  return `${id.slice(0, 10)}…${id.slice(-4)}`;
}

/**
 * Evaluation packets exported for the selected execution, in a table
 * (design-system `.tbl` style). Each row drills into its condition's pack
 * preview so the researcher can actually go somewhere from it.
 */
export function ExperimentPacketTable({ packets, experimentBaseHref }: ExperimentPacketTableProps) {
  if (packets.length === 0) {
    return (
      <p className="text-sm text-[color:var(--muted)]">
        No packets have been exported for this execution yet.
      </p>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse text-sm">
        <thead>
          <tr className="text-left text-[11px] font-medium uppercase tracking-[0.08em] text-(--muted)">
            <th className="border-b border-(--line) px-2 pb-3.5">Packet</th>
            <th className="border-b border-(--line) px-2 pb-3.5">Status</th>
            <th className="border-b border-(--line) px-2 pb-3.5">Condition</th>
            <th className="border-b border-(--line) px-2 pb-3.5">Focal case</th>
            <th className="border-b border-(--line) px-2 pb-3.5 text-right">Action</th>
          </tr>
        </thead>
        <tbody>
          {packets.map((packet) => {
            const refs = readExportRefs(packet.export_refs);
            const code = refs.conditionCode;
            const previewHref =
              experimentBaseHref && code && PREVIEWABLE.has(code.toUpperCase())
                ? `${experimentBaseHref}/${code.toLowerCase()}`
                : null;
            return (
              <tr key={packet.packet_id} className="border-b border-(--line) last:border-0">
                <td className="px-2 py-4">
                  <div className="font-medium text-(--ink)" title={packet.packet_id}>
                    {packet.packet_code}
                  </div>
                  <div className="font-mono text-xs text-(--muted)">
                    {shortId(packet.packet_id)}
                  </div>
                </td>
                <td className="px-2 py-4">
                  <span className="inline-flex rounded-none bg-(--success-tint) px-2.5 py-0.5 text-[11px] font-semibold uppercase tracking-[0.06em] text-(--success-ink)">
                    {packet.status}
                  </span>
                </td>
                <td className="px-2 py-4">
                  {code ? (
                    <span className="inline-flex rounded-none bg-(--accent-soft) px-2.5 py-0.5 text-[11px] font-semibold text-(--accent-deep)">
                      {code}
                    </span>
                  ) : (
                    <span className="text-(--muted)">—</span>
                  )}
                </td>
                <td className="px-2 py-4">
                  {refs.focalCaseType ? (
                    <span className="inline-flex rounded-none border border-(--line) px-2.5 py-0.5 text-[11px] font-medium text-(--ink-2)">
                      {refs.focalCaseType}
                    </span>
                  ) : (
                    <span className="text-(--muted)">—</span>
                  )}
                </td>
                <td className="px-2 py-4 text-right">
                  {previewHref ? (
                    <Link
                      href={previewHref}
                      className="text-xs font-semibold text-(--accent-deep) hover:underline"
                    >
                      Open pack →
                    </Link>
                  ) : (
                    <span className="text-xs text-(--muted)">—</span>
                  )}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
