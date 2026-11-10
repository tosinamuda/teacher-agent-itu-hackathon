# UI / UX

The frontend screens, by role. The code is in `apps/frontend/src/`: `routes/` for the route table, `features/` for pages, and `shared/` for shared components. Generation flows: [revision-note-generation.md](revision-note-generation.md).

## Stack

| Concern | Library |
|---|---|
| Build and dev server | Vite |
| UI | React 19 |
| Routing | React Router 7 |
| Server data | TanStack Query (React Query) |
| Forms | react-hook-form with zod |
| Styles | Tailwind 4 |
| Maths and markdown | react-markdown, remark-math, rehype-katex |
| Rich-text editing | TipTap |
| Charts | Recharts |

- Each feature has its own folder under `src/features/`, with `api`, `hooks`, `components` and `pages` as it needs them.
- Code that two or more features use goes in `src/shared/`.

## Sign-in and roles

- Every role signs in at `/` with an access code. The backend resolves the code to a role.
- A signed-in user goes to `/research`. That page shows the home for the user's role.
- `ResearchRoleGuard` stops a user from opening a page that belongs to another role. The backend enforces the same rules.

| Area | Roles |
|---|---|
| `/research/teacher/*` | `teacher`, `research_manager` |
| `/research/student/*` | `student`, `research_manager` |
| `/research/rater/*` | `rater`, `research_manager` |
| `/research/setup/*`, `/research/learners`, `/research/ops` | `admin`, `research_manager` |
| every other `/research/*` page | `research_manager` |

## Teacher

The teacher prepares each lesson through a checklist, then reviews each student's revision note.

```
plan ─▶ accept plan ─▶ lesson note ─▶ accept note ─▶ class revision note ─▶ accept it
     ─▶ class test ─▶ send to students ─▶ students answer ─▶ review each student's note
```

| Task | Route |
|---|---|
| See subtopics that need a lesson plan | `/research/teacher/to-do` |
| Open the list of lessons to prepare | `/research/teacher/experiment-plans` |
| Open every lesson, finished ones too | `/research/teacher/experiment-plans/all` |
| Work through one lesson's checklist | `/research/teacher/experiment-plans/:experimentId` |
| Review and accept the lesson plan | `/research/teacher/experiment-plans/:experimentId/plan` |
| Enter a lesson plan by hand | `/research/teacher/experiment-plans/:experimentId/manual`, `/research/teacher/lesson-plan/manual` |
| Reuse an existing lesson plan | `/research/teacher/experiment-plans/:experimentId/reuse` |
| Enter the lesson's classwork by hand | `/research/teacher/experiment-plans/:experimentId/classwork` |
| Enter students' results for them: per question, as marked work, or as scores | `/research/teacher/experiment-plans/:experimentId/responses` |
| Draft or edit a lesson plan. The page shows what the agent is doing while it drafts. **Chat with the agent** revises the plan, and selected text on the plan goes with the message. | `/research/teacher/lesson-plan/new`, `/research/teacher/lesson-plan/:planId` |
| Review any content: approve it, or revise it by instruction | `/research/teacher/content/:contentId` |
| Review the class test | `/research/teacher/diagnostics/:planVersionId` |
| Review revision notes that wait for approval | `/research/teacher/pack-reviews`, `/research/teacher/pack-reviews/:artefactId` |
| Read a lesson's revision note | `/research/teacher/lesson-preview`, `/research/teacher/lesson-preview/:artefactId` |
| Manage the class roster | `/research/teacher/learners`, `/research/teacher/learners/new`, `/research/teacher/learners/:learnerId` |
| Browse the scheme of work | `/research/teacher/syllabus` |

- The checklist shows the next step and links to the screen for it. The steps are in `features/experiments/services/lessonPrep.ts`.
- The study conditions run in the background. The teacher never sees a condition code.
- Classwork that is not multiple choice is entered as **Marked work** on the results page. The teacher enters the classwork's questions once, with the model answer and the objective each checks. Then, for each student, they mark each question correct, incorrect or not marked, and add the student's working and, for an incorrect one, the mistake it shows. A question not marked counts for nothing. The marks give the objective's score and the missed questions' evidence, the same way a student's answers to a class test do, so the learner's band and note follow from them. `POST /assessments/exit-assessment/{planVersionId}/responses/manual` takes them as `marked_work`.

## Student

| Task | Route |
|---|---|
| See my lessons, by subject | `/research/student` |
| See one lesson's stages: test, survey, revision note | `/research/student/lesson/:planVersionId` |
| Take the class test, then the survey | `/research/student/exit-assessment` |
| Read an approved revision note | `/research/student/pack-runner` |

- The test shows all questions as one numbered list.
- The survey opens after the student submits the answers. It groups its items by objective ("About Objective N").
- The reader shows one section at a time.

## Rater

Raters rate blinded packets. A packet never shows a condition code.

| Task | Route |
|---|---|
| Rater home | `/research/rater` |
| Rate H1 packets (the C0–C3 notes of one lesson) | `/research/rater/h1`, `/research/rater/h1/:packetId` |
| Rate H2 packets (a base note against a personalized note) | `/research/rater/h2`, `/research/rater/h2/:packetId` |
| Score source-grounding audit items | `/research/rater/audit`, `/research/rater/audit/:itemId` |

Rubric dimensions: the pre-registration, which is not in this repository.

## Researcher

The `research_manager` role sees a tab rail: Studies, Experiments, Setup, Ops.

| Task | Route |
|---|---|
| Studies | `/research`, `/research/investigations/new`, `/research/investigations/:investigationId` |
| Study results and walkthrough | `/research/investigations/:investigationId/results`, `…/walkthrough` |
| Experiments | `/research/experiments`, `/research/experiments/new` |
| Experiments by hypothesis | `/research/h1`, `/research/h2` |
| Experiments by scheme of work | `/research/story` |
| School setup and users | `/research/setup`, `/research/setup/:schoolId/{details,classes,learners}`, `/research/setup/users` |
| Learner directory | `/research/learners` |
| Job queue and recovery | `/research/ops` |

One experiment has these tabs under `/research/experiments/:experimentId`:

| Tab | Path | Shows |
|---|---|---|
| Overview | (none) | study context and readiness |
| H1 setup | `/h1` | conditions C0–C4 |
| H2 setup | `/h2`, `/h2/learners/:learnerId` | P0 and P1, and one learner's two notes |
| Test | `/run` | an end-to-end test run |
| Live | `/live` | the event stream of a running test |
| Raters | `/raters` | rater assignments |
| Results | `/results` | rater statistics and progress |
| Story | `/story` | the journey of each learner |
| Compare | `/compare` | C0–C3 side by side, and base against P1 |

Other experiment pages: `/lesson-plan`, `/assessment`, and `/:conditionCode` for the note of one condition.

## Admin

| Task | Route |
|---|---|
| Users | `/research/setup/users` |
| Schools, workspaces and learners | `/research/setup` |
| Study roster | `/research/learners` |

## Pages outside `/research`

| Route | Page |
|---|---|
| `/`, `/home` | sign-in |
| `/lesson-plan`, `/lesson-plan/new`, `/lesson-plan/:planId` | the lesson-plan generator |

Older URLs such as `/experiments/*`, `/learners` and `/pack-runner` redirect into `/research`. See `src/routes/redirects.tsx`.

## Shared content renderer

`src/shared/components/renderer/` renders lesson plans and revision notes with the same components.

| Component | Renders |
|---|---|
| `ContentBlockRenderer` | one block, by `block.type`: `explanation`, `worked_example`, `practice`, `visual` |
| `VisualBlock` | an `image` from the local figure cache (remote URL as fallback), or a `diagram_tikz` |
| `TikzFigure` | a TikZ drawing as an SVG that the backend draws (`/figures/<id>.svg`) |
| `RichText` | markdown and maths |
| `ReviewNoteSections`, `ReviewNoteSectionCard` | the sections of a revision note |
| `ReviewNoteReader` | a revision note, one section at a time, with Previous and Next |

## Code

| Concern | Path |
|---|---|
| Route table | `apps/frontend/src/routes/` |
| Role guard | `apps/frontend/src/shared/components/layouts/ResearchRoleGuard.tsx` |
| Role homes | `apps/frontend/src/features/home/pages/ResearchHome.tsx` |
| Feature modules | `apps/frontend/src/features/` |
| Shared renderer | `apps/frontend/src/shared/components/renderer/` |
| Run and test commands | `apps/frontend/README.md` |
