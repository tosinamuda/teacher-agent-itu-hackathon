import Markdown from "react-markdown";
import remarkBreaks from "remark-breaks";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";

import { splitFigures } from "@/shared/utils/figures";
import { tidyMathMarkdown } from "@/shared/utils/mathMarkdown";

import { mathRehypePlugins, remarkNoIndentedCode } from "./mathPlugins";
import { TikzFigure } from "./TikzFigure";

/**
 * Markdown with maths, and any TikZ drawing in it drawn as a figure. The drawings are lifted
 * out before `prepare` runs on the text, so nothing that tidies prose can alter a drawing.
 * Each newline breaks the line unless `breaks` is off, as it is for hard-wrapped documents.
 */
export function RichText({
  text,
  prepare = (markdown) => markdown,
  tables = false,
  breaks = true,
}: {
  text: string;
  prepare?: (markdown: string) => string;
  tables?: boolean;
  breaks?: boolean;
}) {
  const remarkPlugins = [
    ...(tables ? [remarkGfm] : []),
    ...(breaks ? [remarkBreaks] : []),
    remarkMath,
    remarkNoIndentedCode,
  ];
  return (
    <>
      {splitFigures(text).map((part, index) =>
        part.kind === "figure" ? (
          <TikzFigure key={index} source={part.source} />
        ) : part.text.trim() ? (
          <Markdown
            key={index}
            remarkPlugins={remarkPlugins}
            rehypePlugins={mathRehypePlugins}
          >
            {tidyMathMarkdown(prepare(part.text))}
          </Markdown>
        ) : null,
      )}
    </>
  );
}
