import { useState } from "react";

import { Picker } from "@/shared/components/ui/Picker";
import { ClassworkByObjective } from "@/features/study-classwork/ClassworkByObjective";
import { useLearnerClasswork } from "@/features/study-classwork/useLearnerClasswork";
import { StudyLessonResults } from "@/features/study-ratings/StudyLessonResults";
import { useStudyRatingsTally } from "@/features/study-ratings/useStudyRatings";

import { EvaluationCharts } from "../components/charts/EvaluationCharts";
import { JourneyDiagnostic } from "../components/JourneyDiagnostic";
import { JourneyPack } from "../components/JourneyPack";
import { JourneySlide, JourneySlides } from "../components/JourneySlides";
import { LearnerStateTable } from "../components/LearnerStateTable";
import { SectionCompare } from "../components/SectionCompare";
import { StoryLessonPlan } from "../components/StoryLessonPlan";
import { StoryRatings } from "../components/StoryRatings";
import { useDiagnosticQuestions } from "../hooks/useDiagnosticQuestions";
import { useExperiment } from "../hooks/useExperiments";
import { useExperimentComparison } from "../hooks/useExperimentComparison";
import { useExperimentRatings, useExperimentStatistics } from "../hooks/useExperimentResults";
import { useExperimentStory } from "../hooks/useExperimentStory";
import { objectiveStates } from "../lib/learnerState";

const BAND_LABEL: Record<string, string> = {
  remediate: "Remediate",
  reinforce: "Reinforce",
  extend: "Extend",
  mixed_or_misconception: "Mixed / misconception",
};

/**
 * The Experiment Story: one learner's way through the experiment, a step at a time —
 * scheme of work, lesson plan, the learner's evidence (their marked class work, or the
 * exit diagnostic), how they stood on each objective, the class note beside their
 * personalised note, and the ratings — each rendered from the real artefacts.
 */
export default function ExperimentStoryPage({ experimentId }: { experimentId: string }) {
  const experimentQuery = useExperiment(experimentId);
  const comparison = useExperimentComparison(experimentId);
  const ratings = useExperimentRatings(experimentId);
  const statistics = useExperimentStatistics(experimentId);
  const planVersionId = experimentQuery.data?.plan_version_id ?? null;
  const studyTally = useStudyRatingsTally(planVersionId ? [planVersionId] : []).data?.[0];
  const story = useExperimentStory(experimentId);
  const diagnostic = useDiagnosticQuestions(planVersionId ?? undefined);

  const bands = comparison.data?.h2_bands ?? [];
  const [bandLearner, setBandLearner] = useState<string | null>(null);
  const band = bands.find((entry) => entry.learner_id === bandLearner) ?? bands[0];
  const classwork = useLearnerClasswork(planVersionId, band?.learner_id ?? "").data;

  const experiment = experimentQuery.data;
  const lessonTitle = experiment?.lesson_title ?? band?.base?.topic ?? "Lesson";
  const bandLabel = band ? (BAND_LABEL[band.band] ?? band.band) : "the learner";
  const objectives = (story.data?.lesson_plan?.lesson_plan_objectives ?? []).map((objective) => ({
    id: objective.lesson_objective_id ?? "",
    text: objective.objective_text ?? "",
  }));
  const focalCase = (experiment?.executions ?? [])
    .filter((execution) => execution.hypothesis === "H2")
    .flatMap((execution) => execution.focal_cases ?? [])
    .find((item) => item.learner_id === band?.learner_id);
  const hasClasswork = (classwork?.questions.length ?? 0) > 0;

  const curriculum = story.data?.curriculum;
  const place = [
    curriculum?.subject,
    curriculum?.grade,
    curriculum?.term,
    curriculum?.week != null ? `Week ${curriculum.week}` : null,
  ].filter(Boolean);

  const slides: JourneySlide[] = [
    {
      title: "Scheme of work",
      subtitle: "Where the teacher started",
      body: (
        <div className="space-y-1 text-sm">
          <p className="text-(--muted)">{place.join(" · ")}</p>
          <p className="text-(--ink)">
            <span className="text-(--muted)">{curriculum?.topic ?? "Topic"} › </span>
            <span className="font-medium">{curriculum?.subtopic ?? lessonTitle}</span>
          </p>
        </div>
      ),
    },
    {
      title: "Lesson plan",
      subtitle: "Authored by the teacher",
      body: <StoryLessonPlan plan={story.data?.lesson_plan} />,
    },
    hasClasswork && classwork
      ? {
          title: "Class work",
          subtitle: "What the learner answered, as the teacher marked it",
          body: <ClassworkByObjective classwork={classwork} objectives={objectives} />,
        }
      : {
          title: "Exit assessment",
          subtitle: "What the learner answered",
          body: <JourneyDiagnostic objectives={diagnostic.data?.objectives ?? []} />,
        },
    {
      title: "Learner state",
      subtitle: hasClasswork
        ? "Each objective's band, from the class work"
        : "Each objective's band, from the diagnostic",
      body: band ? (
        <LearnerStateTable
          states={objectiveStates(focalCase?.learner_state_snapshot)}
          objectives={objectives}
        />
      ) : (
        <p className="text-sm text-(--muted)">No focal learner for this lesson.</p>
      ),
    },
    band?.base && band.personalised
      ? {
          title: "Class and personalised notes",
          subtitle: `P0 beside P1 for ${band.learner_id} · ${bandLabel}`,
          body: (
            <SectionCompare
              leftLabel="P0 · class note"
              rightLabel="P1 · personalised"
              rightBadge={bandLabel}
              left={band.base}
              right={band.personalised}
              onSurface
            />
          ),
        }
      : {
          title: "Class note",
          subtitle: "The class revision note every learner starts from",
          body: <JourneyPack manifest={band?.base ?? null} />,
        },
    {
      title: "Ratings",
      subtitle: "From the blinded evaluation",
      body: studyTally ? (
        <div className="space-y-8">
          <StudyLessonResults experimentId={experimentId} />
        </div>
      ) : (
        <div className="space-y-4">
          <StoryRatings ratings={ratings.data} />
          <EvaluationCharts statistics={statistics.data} variant="headline" />
        </div>
      ),
    },
  ];

  const learnerPicker =
    bands.length > 0 ? (
      <Picker
        stacked
        label="Learner"
        options={[...bands]
          .sort((a, b) => a.learner_id.localeCompare(b.learner_id))
          .map((entry) => ({
            value: entry.learner_id,
            label: `${entry.learner_id} · ${BAND_LABEL[entry.band] ?? entry.band}`,
          }))}
        value={band?.learner_id}
        onChange={setBandLearner}
      />
    ) : null;

  return (
    <div className="py-6">
      <JourneySlides slides={slides} controls={learnerPicker} />
    </div>
  );
}
