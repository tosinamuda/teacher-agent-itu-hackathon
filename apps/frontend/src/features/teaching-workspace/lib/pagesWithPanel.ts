/** Teacher pages built on `WorkspacePage`: they fill the frame and carry their own padding. */
const PAGES_WITH_PANEL = [
  // The class landing, a lesson's home, its class evidence and one learner's evidence, and where its plan is made;
  // the pages that import, write or reuse a plan or a note are forms, which the frame pads.
  /^\/research\/teacher\/lessons(?:\/[^/]+(?:\/evidence(?:\/[^/]+)?|\/plan\/new)?)?$/,
  // An opened plan; "new" and "manual" are the generator and the manual entry.
  /^\/research\/teacher\/lesson-plan\/(?!new$|manual)[^/]+$/,
  // A material, by its content id or its artefact id.
  /^\/research\/teacher\/(?:content|pack-reviews)\/[^/]+$/,
  // The queue of personalised notes.
  /^\/research\/teacher\/pack-reviews$/,
  // The class's learners, and one learner; "new" is the form to add one.
  /^\/research\/teacher\/learners(?:\/(?!new$)[^/]+)?$/,
];

export const hasPanel = (pathname: string): boolean =>
  PAGES_WITH_PANEL.some((page) => page.test(pathname));
