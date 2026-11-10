import { Control, Controller, FieldPath } from "react-hook-form";

import { CompactScoreField } from "./CompactScoreField";
import {
  H2_FIELD_COPY,
  H2_MISCONCEPTION_OPTIONS,
  H2_SCORE_OPTIONS,
  H2RubricFormValues,
  H2ScaleValue,
  H2SectionFieldPrefix,
} from "../services/h2Rating";

type H2SectionRatingStripProps = {
  control: Control<H2RubricFormValues>;
  /** Field-name prefix addressing one section's draft, e.g. `section_scores.step-1`. */
  namePrefix: H2SectionFieldPrefix;
};

/**
 * Renders the five-dimension H2 rating strip (Fit / Support / Challenge /
 * Misconception / Goal) bound to one section's draft via the given field-name
 * prefix. Rendered once per blinded candidate.
 */
export function H2SectionRatingStrip({ control, namePrefix }: H2SectionRatingStripProps) {
  const fieldName = (dimension: keyof typeof H2_FIELD_COPY) =>
    `${namePrefix}.${dimension}` as FieldPath<H2RubricFormValues>;

  return (
    <div className="space-y-3">
      <Controller
        control={control}
        name={fieldName("learner_state_suitability")}
        render={({ field }) => (
          <CompactScoreField
            description={H2_FIELD_COPY.learner_state_suitability.description}
            label={H2_FIELD_COPY.learner_state_suitability.label}
            onChange={(nextValue) => field.onChange(nextValue as H2ScaleValue)}
            options={H2_SCORE_OPTIONS}
            value={field.value as unknown as H2ScaleValue | undefined}
          />
        )}
      />

      <Controller
        control={control}
        name={fieldName("scaffolding_appropriateness")}
        render={({ field }) => (
          <CompactScoreField
            description={H2_FIELD_COPY.scaffolding_appropriateness.description}
            label={H2_FIELD_COPY.scaffolding_appropriateness.label}
            onChange={(nextValue) => field.onChange(nextValue as H2ScaleValue)}
            options={H2_SCORE_OPTIONS}
            value={field.value as unknown as H2ScaleValue | undefined}
          />
        )}
      />

      <Controller
        control={control}
        name={fieldName("challenge_calibration")}
        render={({ field }) => (
          <CompactScoreField
            description={H2_FIELD_COPY.challenge_calibration.description}
            label={H2_FIELD_COPY.challenge_calibration.label}
            onChange={(nextValue) => field.onChange(nextValue as H2ScaleValue)}
            options={H2_SCORE_OPTIONS}
            value={field.value as unknown as H2ScaleValue | undefined}
          />
        )}
      />

      <Controller
        control={control}
        name={fieldName("misconception_support")}
        render={({ field }) => (
          <CompactScoreField
            description={H2_FIELD_COPY.misconception_support.description}
            label={H2_FIELD_COPY.misconception_support.label}
            onChange={(nextValue) =>
              field.onChange(nextValue === "na" ? "na" : (Number(nextValue) as H2ScaleValue))
            }
            options={H2_MISCONCEPTION_OPTIONS}
            value={field.value as unknown as H2ScaleValue | "na" | undefined}
          />
        )}
      />

      <Controller
        control={control}
        name={fieldName("objective_preservation")}
        render={({ field }) => (
          <CompactScoreField
            description={H2_FIELD_COPY.objective_preservation.description}
            label={H2_FIELD_COPY.objective_preservation.label}
            onChange={(nextValue) => field.onChange(nextValue as H2ScaleValue)}
            options={H2_SCORE_OPTIONS}
            value={field.value as unknown as H2ScaleValue | undefined}
          />
        )}
      />
    </div>
  );
}
