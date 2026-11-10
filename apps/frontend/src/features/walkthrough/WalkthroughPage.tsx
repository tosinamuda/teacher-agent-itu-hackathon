import type { ReactElement } from "react";

import { Picker } from "@/shared/components/ui/Picker";
import { JourneySlide, JourneySlides } from "@/features/experiments/components/JourneySlides";
import { useInvestigation } from "@/features/experiments/hooks/useInvestigations";
import { useStudyRatingsTally } from "@/features/study-ratings/useStudyRatings";

import {
  ComparedStep,
  GroundingStep,
  LearnerStep,
  LessonStep,
  RatedNoteStep,
  RatersStep,
} from "./lessonSteps";
import { CleanedStep, PagesStep, ScriptStep, TranscribedStep } from "./dataSteps";
import { DesignStep, ProvenanceStep, ResultsStep } from "./studySteps";
import { useLessonRecord } from "./useLessonRecord";
import { useLessonTranscripts, useStudyDesign } from "./useStudyData";
import { useWalkthroughState } from "./useWalkthroughState";

const NotInPart2 = () => (
  <p className="text-sm text-(--ink-2)">
    This lesson was not in the study&apos;s Part 2. Choose a lesson with learners to see this step.
  </p>
);

/**
 * The study walked through for an audience, a step at a time, on an example that can be
 * switched at any point: the lesson, the draw and the learner are chosen beside the steps, and
 * every step redraws on the new example while the walk stays where it is.
 */
export default function WalkthroughPage({ investigationId }: { investigationId: string }) {
  const investigation = useInvestigation(investigationId).data;
  const [state, update] = useWalkthroughState();
  const lessons = [...(investigation?.experiments ?? [])].sort((a, b) =>
    a.experiment_code.localeCompare(b.experiment_code),
  );
  const tallies =
    useStudyRatingsTally(
      lessons.flatMap((lesson) => (lesson.plan_version_id ? [lesson.plan_version_id] : [])),
    ).data ?? [];
  const inPart2 = (planVersionId: string | null | undefined) =>
    tallies.some((tally) => tally.plan_version_id === planVersionId && tally.judgements > 0);
  const lesson =
    lessons.find((each) => each.experiment_code === state.lesson) ??
    lessons.find((each) => inPart2(each.plan_version_id)) ??
    lessons[0];
  const record = useLessonRecord(lesson?.experiment_id);
  const transcripts = useLessonTranscripts(lesson?.experiment_id).data;
  const design = useStudyDesign(investigationId).data;
  const learner =
    record.learners.find((each) => each.learner_id === state.learner) ?? record.learners[0];
  const draw = record.draws.includes(state.draw) ? state.draw : (record.draws[0] ?? 1);

  if (!investigation || !lesson) return <p className="text-sm text-(--muted)">Loading…</p>;

  const lessonStep = (body: ReactElement) => (record.experiment ? body : null);
  const learnerStep = (body: ReactElement) => (learner ? body : <NotInPart2 />);
  const slides: JourneySlide[] = [
    {
      chapter: "The study",
      title: "Design",
      subtitle: "Its scope, its two parts, and each lesson's share",
      body: <DesignStep investigation={investigation} design={design} />,
    },
    {
      chapter: "From classroom to data",
      title: "Pages captured",
      subtitle: "What was photographed in the classroom",
      body: <PagesStep transcripts={transcripts} />,
    },
    {
      chapter: "From classroom to data",
      title: "Transcribed as written",
      subtitle: "The teacher's pages word for word; this record is never edited",
      body: <TranscribedStep transcripts={transcripts} />,
    },
    {
      chapter: "From classroom to data",
      title: "Cleaned, with reasons",
      subtitle: "What changed in the copy the study used, and what licensed each change",
      body: <CleanedStep transcripts={transcripts} />,
    },
    {
      chapter: "From classroom to data",
      title: "The structured plan",
      subtitle: "The cleaned pages as the lesson plan every note was written from",
      body: <LessonStep experimentId={lesson.experiment_id} />,
    },
    {
      chapter: "Part 1 · H1",
      title: "Grounding",
      subtitle: `A less grounded note beside C3, draw ${draw}`,
      body: lessonStep(<GroundingStep record={record} draw={draw} />),
    },
    {
      chapter: "Part 1 · H1",
      title: "A class note, rated",
      subtitle: `C3, draw ${draw}, objective by objective`,
      body: lessonStep(<RatedNoteStep record={record} draw={draw} />),
    },
    {
      chapter: "Part 2 · H2",
      title: "A learner's class work",
      subtitle: "Their script as written, and as marked by objective",
      body: learnerStep(
        <ScriptStep
          record={record}
          transcripts={transcripts}
          learnerId={learner?.learner_id ?? ""}
        />,
      ),
    },
    {
      chapter: "Part 2 · H2",
      title: "The learner's bands",
      subtitle: "Their band on each objective, read from the marked work",
      body: learnerStep(<LearnerStep record={record} learnerId={learner?.learner_id ?? ""} />),
    },
    {
      chapter: "Part 2 · H2",
      title: "P0 beside P1, rated",
      subtitle: "The two notes as the raters compared them",
      body: learnerStep(<ComparedStep record={record} learnerId={learner?.learner_id ?? ""} />),
    },
    {
      chapter: "Findings",
      title: "Across the study",
      subtitle: "Every lesson pooled; each objective a data point",
      body: <ResultsStep investigationId={investigationId} />,
    },
    {
      chapter: "Findings",
      title: "How it was rated",
      subtitle: "Who rated what, and in which order",
      body: lessonStep(<RatersStep record={record} />),
    },
    {
      chapter: "Findings",
      title: "Provenance and limits",
      subtitle: "Where the record came from, and what it does not cover",
      body: <ProvenanceStep investigation={investigation} tallies={tallies} record={record} />,
    },
  ];

  const controls = (
    <div className="flex flex-wrap items-end gap-4 lg:block lg:space-y-4">
      <Picker
        stacked
        label="Lesson"
        options={lessons.map((each) => ({
          value: each.experiment_code,
          label: each.lesson_title ?? each.experiment_code,
        }))}
        value={lesson.experiment_code}
        onChange={(code) => update({ lesson: code, learner: null })}
      />
      {record.draws.length > 1 ? (
        <Picker
          stacked
          label="Draw"
          options={record.draws.map((each) => ({ value: String(each), label: `Draw ${each}` }))}
          value={String(draw)}
          onChange={(value) => update({ draw: Number(value) })}
        />
      ) : null}
      {record.learners.length > 0 ? (
        <Picker
          stacked
          label="Learner"
          options={record.learners.map((each) => ({
            value: each.learner_id,
            label: `${each.learner_name ?? each.learner_id} · ${each.focal_type}`,
          }))}
          value={learner?.learner_id}
          onChange={(value) => update({ learner: value })}
        />
      ) : null}
    </div>
  );

  return (
    <JourneySlides
      slides={slides}
      controls={controls}
      index={state.step - 1}
      onIndexChange={(index) => update({ step: index + 1 })}
    />
  );
}
