# Deployment

Autevra is local-first: `make dev` on the Mac is the primary way to run it. This page
describes a hosted demo of the same code.

## Shape

| Part | What it is | Host |
|---|---|---|
| Website, workspace, studio | Static files from `npm run build` (`frontend/dist`) | Netlify (`netlify.toml`) |
| Backend API | FastAPI + CadQuery/OCCT in the `backend/Dockerfile` image (linux/amd64) | Hugging Face Spaces (free), or any container host with **≥ 1 GB RAM** and x86_64 |
| Database | Postgres | Neon |
| Local LLM | Not deployed. Set `AUTEVRA_LLM_PROVIDER=off`; the deterministic parser and every engineering feature still work, and the UI says the model is off | — |

The frontend calls the API directly at `VITE_API_URL` (set at build time) and the API
allows that origin through `AUTEVRA_CORS_ORIGINS`. Direct calls avoid proxy time limits:
an optimisation study or engineering loop can run for longer than a CDN rewrite allows.

### Backend constraints (measured)

- **Memory:** about 470 MB after import (CadQuery, OCP, VTK) and 545 MB after one model
  build. Plans with 512 MB (Render Free and Starter, Koyeb Free) run out of memory.
- **Architecture:** `cadquery-ocp` 7.9.x has no Linux arm64 wheel, so the image is
  linux/amd64. ARM-only hosts (for example Oracle's free Ampere VMs) cannot run it yet.
- **Disk:** only regenerable STEP exports are written to `AUTEVRA_DATA_DIR`, so an
  ephemeral disk is fine once the database is in Neon.
- **Cold start:** about 5 s to import the CAD kernel, plus one model build on first use.

## Free setup: Neon + Hugging Face Spaces + Netlify

All three have free tiers that need no payment card. The backend runs as a Docker Space on
the free CPU tier (enough memory, x86_64). GitHub Actions deploys it after every green CI
run on `main` (`.github/workflows/deploy-space.yml`).

### 1. Database: Neon

1. Sign up at neon.tech and create a project (Postgres 17, the region closest to you).
2. Copy the connection string from the dashboard
   (`postgresql://…@ep-….neon.tech/neondb?sslmode=require`). It is a password: keep it out
   of git and chats.
3. Nothing else to do: the backend rewrites the URL for the psycopg 3 driver and runs the
   migrations at startup.

### 2. Backend: Hugging Face Space

1. Sign up at huggingface.co, then **New Space**: name `autevra-api`, SDK **Docker**,
   template **Blank**, hardware **CPU basic (free)**, visibility **Public** (a private
   Space cannot be called from the website).
2. In the Space, **Settings → Variables and secrets**:
   - secret `AUTEVRA_DATABASE_URL` = the Neon connection string;
   - variable `AUTEVRA_CORS_ORIGINS` = `["https://<your-site>.netlify.app"]` (fill in once
     the Netlify site exists, step 3).
3. In your Hugging Face account, **Settings → Access Tokens → Create new token**, type
   **Write**. Copy it.
4. In the GitHub repository, **Settings → Secrets and variables → Actions**:
   - **Secrets** tab: `HF_TOKEN` = the token;
   - **Variables** tab: `HF_SPACE` = `<your-hf-username>/autevra-api`.
5. Start the first deploy: **Actions → Deploy backend to Hugging Face Spaces → Run
   workflow** (or `gh workflow run deploy-space.yml`). Later deploys run by themselves.
6. The Space builds the image (about 5 minutes the first time) and serves the API at
   `https://<your-hf-username>-autevra-api.hf.space`; check `…/api/health`.

What the workflow pushes is built by `deploy/huggingface/build-space.sh`: the backend
sources, `uv.lock`, the Dockerfile with `AUTEVRA_LLM_PROVIDER=off`, and the Space card
(`deploy/huggingface/README.md`, `app_port: 8000`). The container runs as uid 1000, as
Spaces require. CI builds the same bundle, runs it as uid 1000, creates a project, builds
the model and exports a STEP file.

The free Space sleeps when unused. While it starts, the website retries read requests for
up to three minutes and shows "Starting the engineering backend"; writes are never
retried, so nothing is applied twice. Without `AUTEVRA_DATABASE_URL` the Space falls back
to SQLite on its own disk, which is wiped on every restart.

### 3. Frontend: Netlify

1. Sign up at netlify.com, **Add new site → Import an existing project → GitHub**, pick
   this repository. `netlify.toml` sets the base directory (`frontend`), the build
   command, the publish directory and the client-side route fallback.
2. **Site configuration → Environment variables**: `VITE_API_URL` =
   `https://<your-hf-username>-autevra-api.hf.space`, then **Deploys → Trigger deploy**.
3. Put the Netlify address into the Space's `AUTEVRA_CORS_ORIGINS` (step 2.2); the Space
   restarts with it.

## Other backend hosts (paid or card required)

The image listens on `$PORT` when the host sets it, otherwise 8000; health check
`GET /api/health`. Set the same variables as above plus `AUTEVRA_LLM_PROVIDER=off` and
`AUTEVRA_DATA_DIR=/tmp/autevra`.

**Google Cloud Run.** 2 GiB instances that scale to zero; a demo usually stays inside the
monthly free allowance, but it needs a billing account.

```sh
# once: store the Neon URL in Secret Manager
printf '%s' 'postgresql://…' | gcloud secrets create autevra-database-url --data-file=-

# "^|^" makes "|" the separator, because the CORS list is JSON
gcloud run deploy autevra-api --source backend --region europe-west1 \
  --memory 2Gi --cpu 1 --allow-unauthenticated \
  --set-env-vars '^|^AUTEVRA_LLM_PROVIDER=off|AUTEVRA_DATA_DIR=/tmp/autevra|AUTEVRA_CORS_ORIGINS=["https://<your-site>.netlify.app"]' \
  --set-secrets AUTEVRA_DATABASE_URL=autevra-database-url:latest
```

**Render.** Connect the repository as a Blueprint (`render.yaml`, `standard` plan with
2 GB; the 512 MB plans are too small) and enter the two `sync: false` variables.

## Check the deployment

- `curl https://<backend>/api/health` returns `{"status":"ok",…}`.
- Open the Netlify site, create a project from `/app`, open it in the studio, change a
  parameter, run the quarter-car test and download a STEP file.

## Before sharing the link widely

- **There are no user accounts yet.** Every visitor sees, edits and can delete every
  project. Treat the hosted instance as a shared demo, not a place for real work.
- The contact form stores messages in the database with no rate limit or spam filter.
- The local LLM is off on the hosted instance; that is a choice, not a fault.

Per-visitor workspaces, rate limits and accounts are tracked in `ROADMAP.md`.

## Testing against Postgres locally

```sh
createdb autevra_test
AUTEVRA_TEST_DATABASE_URL=postgresql://localhost/autevra_test uv run pytest -q
```

Each test starts from an empty `public` schema. CI runs the suite on SQLite and on
`postgres:17`.
