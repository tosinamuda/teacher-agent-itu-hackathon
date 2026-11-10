# Frontend

The Plan-to-Tutor web app: a React single-page app built with Vite.

## Run

```bash
npm run dev           # the app at http://localhost:3000
npm test              # the unit tests (Vitest)
npm run type-check    # ESLint, then TypeScript
npm run build         # the static build in dist/
```

The app calls the API at `VITE_API_BASE_URL`. The default is `http://localhost:8000`.

## End-to-end tests

The two Cypress specs drive the real app, API, database, job runner and model.
`everyday_path` takes a new lesson from no plan to a student reading their own revision note.
`research_path` then runs H2, exports the packets, and has a rater score one.

```bash
npm run e2e    # both specs; about 7 minutes and 41 model calls
```

Start the backend and the app first.
The specs sign in with the seeded codes `teacher-1`, `researcher`, `rater-1` and `student-1` to `student-3`.

| Variable | Sets | Default |
| --- | --- | --- |
| `CYPRESS_BASE_URL` | The app address | `http://localhost:3000` |
| `CYPRESS_API_URL` | The API address | `http://localhost:8010` |
| `CYPRESS_LESSON_ID` | The lesson for `everyday_path` | A random lesson that no experiment studies |
| `CYPRESS_EXPERIMENT_ID` | The experiment for `research_path` | The experiment that `everyday_path` made |

## Files

```
src/main.tsx       the entry point
src/routes/        the route table
src/features/      one folder per feature: pages, components, hooks, and API calls
src/shared/        the API client, UI components, and hooks that features share
cypress/           the end-to-end tests
public/_redirects  sends every deep link to the app on Cloudflare Pages
```
