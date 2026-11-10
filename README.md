> **ITU AI for Good Lab Hackathon (UAE, 2026) entry: Teacher Agent.** The hackathon material is in [`hackathon/`](hackathon/README.md): the Y.3172 node-to-code map, the knowledge base and the seed data. Everything else in this repository is the original project.

# LPCG: Lesson-Plan-Grounded, Personalised Content Generation

A research platform that makes revision material from a teacher's lesson plan.
Blinded expert raters then evaluate the material.

1. A teacher approves a lesson plan, a lesson note, and a class test.
2. The system writes a class revision note from them.
3. Each student takes the class test and gets a personal revision note.
4. A researcher runs the same generation as the H1 and H2 experiments.
5. Raters score the output blind.

Live: frontend <https://lpcg.pages.dev> · API <https://lpcg-api.tosinamuda.com/api>

## Install

You need Node 20 or later, [uv](https://docs.astral.sh/uv/), and MySQL 9.

```bash
mysql -uroot <<'SQL'
CREATE DATABASE lpcg CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_cs;
CREATE USER 'lpcg'@'localhost' IDENTIFIED BY 'lpcg';
GRANT ALL PRIVILEGES ON lpcg.* TO 'lpcg'@'localhost';
SQL
cp apps/backend/.env.example apps/backend/.env   # set DATABASE_URL and BEDROCK_MANTLE_API_KEY
npm install
export HF_TOKEN=...   # a Hugging Face read token with access to the gated tosinamuda/ng-jss1-math-* datasets
cd apps/backend && PYTHONPATH=. uv run python scripts/seed_all.py   # the schema, the corpus, then the seed data
```

The setup downloads the seed corpus into `dataset/processed/`, and the raters' delivered documents into `apps/backend/experiments/human_rating/delivered/`, at the versions `dataset/datasets.lock.json` pins, and checks every file. The folders it fills are ignored by git.
The last line of the setup is `✓ Database setup complete (migrate + seed).`

## Run

```bash
npm run dev    # the frontend on :3000, the API on :8000
```

The API also runs the background jobs, so this is the whole system.

## Files

```
apps/frontend/     the web app (README inside)
apps/backend/      the API (README inside)
dataset/processed/ the curriculum, textbook, and linkage data the seed chain loads: fetched from Hugging Face, not committed
deploy/ansible/    the server setup and deploy (README inside)
docs/              how the system works
```

## Deploy

`main` deploys to staging. Production deploys a release tag.

- The API: [`deploy/ansible/README.md`](deploy/ansible/README.md).
- The frontend: Cloudflare Pages builds `apps/frontend` with `npm run build`.
  See [Frontend](deploy/ansible/README.md#frontend) for the branches and `VITE_API_BASE_URL`.
