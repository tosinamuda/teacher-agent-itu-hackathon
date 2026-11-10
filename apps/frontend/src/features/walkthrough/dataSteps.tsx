import { Section } from "@/shared/components/ui/Section";
import { ROW_HEAD, TABLE, TD, TH } from "@/shared/components/ui/table";
import { ClassworkByObjective } from "@/features/study-classwork/ClassworkByObjective";
import { useLearnerClasswork } from "@/features/study-classwork/useLearnerClasswork";

import { TranscriptText } from "./TranscriptText";
import { type Transcript, type TranscriptKind, cleaningsOf, roleOf } from "./studyData";
import { type LessonRecord, useLessonObjectives } from "./useLessonRecord";

const Waiting = () => <p className="text-sm text-(--muted)">Loading…</p>;
const Missing = () => <p className="text-sm text-(--muted)">Not published for this lesson.</p>;

const ofKind = (transcripts: Transcript[], kind: TranscriptKind) =>
  transcripts.find((transcript) => transcript.kind === kind);

const field = (transcript: Transcript, name: string): string => {
  const value = transcript.header[name];
  return value == null ? "—" : String(value);
};

/** What was photographed in the classroom: the teacher's pages by what each shows, and the scripts. */
export function PagesStep({ transcripts }: { transcripts: Transcript[] | undefined }) {
  if (!transcripts) return <Waiting />;
  const teacher = ofKind(transcripts, "teacher_record");
  const scripts = transcripts.filter((transcript) => transcript.kind === "learner_script");
  return (
    <div className="space-y-8">
      <p className="text-sm text-(--muted)">The photographs stay private; their transcripts are published.</p>
      <Section title="The teacher's pages" aside={teacher ? `${teacher.pages.length} pages` : null}>
        {teacher ? (
          <table className={TABLE}>
            <thead>
              <tr>
                <th className={TH}>Page</th>
                <th className={TH}>Shows</th>
              </tr>
            </thead>
            <tbody>
              {teacher.pages.map((page) => (
                <tr key={page.file}>
                  <td className={`${TD} font-mono text-xs text-(--ink-2)`}>{page.file}</td>
                  <td className={TD}>{roleOf(page)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <Missing />
        )}
      </Section>
      {scripts.length > 0 ? (
        <Section title="The learners' class work" aside={`${scripts.length} scripts`}>
          <table className={TABLE}>
            <thead>
              <tr>
                <th className={TH}>Learner</th>
                <th className={TH}>Pages</th>
                <th className={TH}>Teacher&apos;s mark</th>
              </tr>
            </thead>
            <tbody>
              {scripts.map((script) => (
                <tr key={script.source_path}>
                  <td className={ROW_HEAD}>{script.student_id}</td>
                  <td className={TD}>{script.pages.length}</td>
                  <td className={TD}>{field(script, "teacher_total")}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Section>
      ) : null}
    </div>
  );
}

/** The teacher's pages as transcribed, word for word; this record is never edited. */
export function TranscribedStep({ transcripts }: { transcripts: Transcript[] | undefined }) {
  if (!transcripts) return <Waiting />;
  const record = ofKind(transcripts, "teacher_record");
  return record ? <TranscriptText text={record.body} /> : <Missing />;
}

/** What the cleaning changed in the copy the study used, each change with what licensed it. */
export function CleanedStep({ transcripts }: { transcripts: Transcript[] | undefined }) {
  if (!transcripts) return <Waiting />;
  const cleaned = ofKind(transcripts, "teacher_cleaned");
  const log = ofKind(transcripts, "cleaning_log");
  if (!cleaned) return <Missing />;
  return (
    <div className="space-y-8">
      <ol className="divide-y divide-(--line) border-y border-(--line)">
        {cleaningsOf(cleaned.header).map((cleaning, i) => (
          <li key={i} className="grid gap-x-6 gap-y-1 py-4 sm:grid-cols-[9rem_minmax(0,1fr)]">
            <p className="text-sm font-medium text-(--ink)">{cleaning.what}</p>
            <div className="space-y-1">
              <TranscriptText text={cleaning.change} />
              <TranscriptText text={cleaning.why} muted />
            </div>
          </li>
        ))}
      </ol>
      {log ? (
        <details className="text-sm">
          <summary className="cursor-pointer text-(--muted) hover:text-(--ink)">
            The full cleaning log
          </summary>
          <div className="mt-4">
            <TranscriptText text={log.body} />
          </div>
        </details>
      ) : null}
    </div>
  );
}

/** The chosen learner's script as written, beside the same work marked objective by objective. */
export function ScriptStep({
  record,
  transcripts,
  learnerId,
}: {
  record: LessonRecord;
  transcripts: Transcript[] | undefined;
  learnerId: string;
}) {
  const planVersionId = record.experiment?.plan_version_id ?? null;
  const classwork = useLearnerClasswork(planVersionId, learnerId).data;
  const objectives = useLessonObjectives(record.experiment?.experiment_id);
  if (!transcripts || !classwork || !objectives) return <Waiting />;
  const script = transcripts.find(
    (transcript) => transcript.kind === "learner_script" && transcript.student_id === learnerId,
  );
  return (
    <div className="grid gap-8 xl:grid-cols-2">
      <Section title="As written">{script ? <TranscriptText text={script.body} /> : <Missing />}</Section>
      <Section title="As marked, by objective">
        <ClassworkByObjective classwork={classwork} objectives={objectives} />
      </Section>
    </div>
  );
}
