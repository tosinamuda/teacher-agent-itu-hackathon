import { withFractionsAsMath } from "@/shared/utils/fractionMarkup";

import { RichText } from "./RichText";

/** A class-test stem or option, its maths set as the lesson notes set theirs. */
export function ClassTestText({ text }: { text: string }) {
  return (
    <div className="min-w-0">
      <RichText text={text} prepare={withFractionsAsMath} />
    </div>
  );
}
