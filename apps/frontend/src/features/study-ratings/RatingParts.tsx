import { ROW_HEAD, TABLE, TD, TH } from "@/shared/components/ui/table";

import { cellOf, judgementLabel, ratersOf } from "./ratingGrid";
import {
  ComparativeJudgement,
  CriterionScore,
  InstrumentCriterion,
  RatingDocument,
  StudyInstrument,
} from "./types";

/** Each rater's name as their rating documents give it, by rater id. */
export function raterNames(documents: RatingDocument[]): Map<string, string> {
  return new Map(documents.map((document) => [document.rater, document.rater_name]));
}

function CriterionName({ criterion }: { criterion: InstrumentCriterion }) {
  return <span title={criterion.question}>{criterion.name}</span>;
}

function Comment({ text }: { text: string | null }) {
  return text ? <p className="mt-0.5 text-xs text-(--ink-2)">{text}</p> : null;
}

/** One objective's scores: a row per criterion, a column per rater, comments under each score. */
export function ObjectiveScores({
  scores,
  criteria,
  names,
}: {
  scores: CriterionScore[];
  criteria: InstrumentCriterion[];
  names: Map<string, string>;
}) {
  if (scores.length === 0) return <p className="text-sm text-(--muted)">No scores.</p>;
  const raters = ratersOf(scores);
  return (
    <div className="overflow-x-auto">
      <table className={`${TABLE} table-fixed`}>
        <thead>
          <tr>
            <th className={`${TH} w-2/5`}>Criterion</th>
            {raters.map((rater) => (
              <th key={rater} className={TH}>
                {names.get(rater) ?? rater}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {criteria.map((criterion) => (
            <tr key={criterion.id}>
              <th scope="row" className={ROW_HEAD}>
                <CriterionName criterion={criterion} />
              </th>
              {raters.map((rater) => {
                const score = cellOf(scores, rater, criterion.id);
                return (
                  <td key={rater} className={TD}>
                    <span className="font-medium text-(--ink)">
                      {score ? `${score.score} / 5` : "—"}
                    </span>
                    <Comment text={score?.comment ?? null} />
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

/** One objective's comparison: a row per criterion, a column per rater, in terms of P0 and P1. */
export function ObjectiveJudgements({
  judgements,
  criteria,
  names,
}: {
  judgements: ComparativeJudgement[];
  criteria: InstrumentCriterion[];
  names: Map<string, string>;
}) {
  if (judgements.length === 0) return <p className="text-sm text-(--muted)">No comparison.</p>;
  const raters = ratersOf(judgements);
  return (
    <div className="overflow-x-auto">
      <table className={`${TABLE} table-fixed`}>
        <thead>
          <tr>
            <th className={`${TH} w-2/5`}>Criterion</th>
            {raters.map((rater) => (
              <th key={rater} className={TH}>
                {names.get(rater) ?? rater}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {criteria.map((criterion) => (
            <tr key={criterion.id}>
              <th scope="row" className={ROW_HEAD}>
                <CriterionName criterion={criterion} />
              </th>
              {raters.map((rater) => {
                const judgement = cellOf(judgements, rater, criterion.id);
                return (
                  <td key={rater} className={TD}>
                    <span
                      className="font-medium text-(--ink)"
                      title={
                        judgement ? `${judgement.choice} (P1 was ${judgement.shown_as})` : undefined
                      }
                    >
                      {judgement ? judgementLabel(judgement) : "—"}
                    </span>
                    <Comment text={judgement?.comment ?? null} />
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const SHORT: Record<RatingDocument["state"], string | null> = {
  complete: null,
  partial: "partly answered",
  untouched: "returned unanswered",
};

/** Who rated the note: each rater's set, when they finished it, and any closing comment. */
export function RaterSets({ documents }: { documents: RatingDocument[] }) {
  if (documents.length === 0) return <p className="text-sm text-(--muted)">Not rated.</p>;
  return (
    <ul className="space-y-1 text-sm">
      {documents.map((document) => (
        <li key={document.packet}>
          <span className="font-medium text-(--ink)">{document.rater_name}</span>
          <span className="text-(--muted)">
            {document.shown_as
              ? ` · ${document.shown_as === "A" ? "A: P1 · B: P0" : "A: P0 · B: P1"}`
              : ""}
            {document.date_completed ? ` · ${document.date_completed}` : ""}
          </span>
          {SHORT[document.state] ? (
            <span className="text-(--warning-ink)"> · {SHORT[document.state]}</span>
          ) : null}
          {document.closing_comment ? (
            <p className="mt-0.5 text-(--ink-2)">“{document.closing_comment}”</p>
          ) : null}
        </li>
      ))}
    </ul>
  );
}

/** The criteria as the raters read them: each question, and what every point on its scale means. */
export function InstrumentDetails({
  criteria,
  instrument,
  comparative,
}: {
  criteria: InstrumentCriterion[];
  instrument: StudyInstrument;
  comparative: boolean;
}) {
  return (
    <details className="text-sm text-(--ink-2)">
      <summary className="cursor-pointer text-(--muted) hover:text-(--ink)">
        The criteria as the raters read them
      </summary>
      <div className="mt-2 space-y-3">
        <p className="text-xs text-(--muted)">
          {comparative
            ? `Each criterion was marked once on: ${instrument.comparison.join(" · ")}.`
            : `Each criterion was scored 1 to 5: ${instrument.scale
                .map(([score, meaning]) => `${score} — ${meaning}`)
                .join("; ")}.`}
        </p>
        {criteria.map((criterion, index) => (
          <div key={criterion.id} className="space-y-1">
            <p className="font-medium text-(--ink)">
              {index + 1}. {criterion.name}
            </p>
            <p>{criterion.question}</p>
            {comparative ? (
              criterion.better ? (
                <p className="text-xs">Better means: {criterion.better}</p>
              ) : null
            ) : (
              <ol className="list-decimal pl-5 text-xs">
                {criterion.descriptors.map((descriptor) => (
                  <li key={descriptor}>{descriptor}</li>
                ))}
              </ol>
            )}
            {criterion.notes.map((note) => (
              <p key={note} className="text-xs text-(--muted)">
                {note}
              </p>
            ))}
          </div>
        ))}
      </div>
    </details>
  );
}
