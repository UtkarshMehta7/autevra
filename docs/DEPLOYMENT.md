# Deployment

Autevra is local-first: `make dev` on the Mac is the primary way to run it. This page
describes a hosted demo of the same code.

**Live since 2026-10-14:** website at <https://autevra.netlify.app>, API at
<https://autevra.onrender.com> (`/api/health`), database on Neon. Netlify and Render both
deploy `main` automatically.

## Shape

| Part | What it is | Host |
|---|---|---|
| Website, workspace, studio | Static files from `npm run build` (`frontend/dist`) | Netlify (`netlify.toml`) |
| Backend API | FastAPI + CadQuery/OCCT in the `backend/Dockerfile` image (linux/amd64) | Render (free plan), or any x86_64 container host |
| Database | Postgres | Neon |
| Local LLM | Not deployed. Set `AUTEVRA_LLM_PROVIDER=off`; the deterministic parser and every engineering feature still work, and the UI says the model is off | — |

The frontend calls the API directly at `VITE_API_URL` (set at build time) and the API
allows that origin through `AUTEVRA_CORS_ORIGINS`. Direct calls avoid proxy time limits:
an optimisation study or engineering loop can run for longer than a CDN rewrite allows.

### Backend constraints (measured)

- **Memory:** on the Mac, peak RSS is about 470 MB after import (CadQuery, OCP, VTK) and
  545 MB after one model build. In the linux/amd64 container it is much lower: 295 MiB at
  peak through a full session including an optimisation study (cgroup `memory.peak`, CI).
  CI runs that session under a 512 MB cap on every pull request.
- **Architecture:** `cadquery-ocp` 7.9.x has no Linux arm64 wheel, so the image is
  linux/amd64. ARM-only hosts (for example Oracle's free Ampere VMs) cannot run it yet.
- **Disk:** only regenerable STEP exports are written to `AUTEVRA_DATA_DIR`, so an
  ephemeral disk is fine once the database is in Neon.
- **Cold start:** about 5 s to import the CAD kernel, plus one model build on first use.

## Free setup: Neon + Render + Netlify

All three have free tiers that need no payment card. The backend runs on Render's free web
service (512 MB, 0.1 CPU, x86_64) from `render.yaml` and redeploys on every push to `main`.

### 1. Database: Neon

1. Sign up at neon.tech and create a project (Postgres 17, the region closest to you).
2. Copy the connection string from the dashboard
   (`postgresql://…@ep-….neon.tech/neondb?sslmode=require`). It is a password: keep it out
   of git and chats.
3. Nothing else to do: the backend rewrites the URL for the psycopg 3 driver and runs the
   migrations at startup.

### 2. Backend: Render

1. Sign up at render.com with GitHub and allow it to read the `autevra` repository.
2. **New → Blueprint**, pick the repository. Render reads `render.yaml`: one Docker web
   service `autevra-api`, plan **Free**, root directory `backend`, health check `/api/health`.
3. It asks for the two values marked `sync: false`:
   - `AUTEVRA_DATABASE_URL` = the Neon connection string;
   - `AUTEVRA_CORS_ORIGINS` = `["https://<your-site>.netlify.app"]` (if the Netlify site does
     not exist yet, enter `[]` and change it after step 3).
4. **Apply.** The first image build takes several minutes.

   If the service was created as a plain **Web Service** instead of a Blueprint (the live
   one was), `render.yaml` is not read, so set the same things by hand: **Root Directory**
   `backend`, **Dockerfile Path** `./Dockerfile`, **Health Check Path** `/api/health`,
   instance type **Free**, and the four environment variables `AUTEVRA_DATABASE_URL`,
   `AUTEVRA_CORS_ORIGINS`, `AUTEVRA_LLM_PROVIDER=off`, `AUTEVRA_DATA_DIR=/tmp/autevra`.
   Without the root directory the build fails with "open Dockerfile: no such file". The API is then at
   `https://autevra-api.onrender.com` (Render adds a suffix if the name is taken; the
   dashboard shows the real address). Check `…/api/health`.

What to expect from the free instance (measured in CI with the same limits; see below):

- It sleeps after 15 minutes without traffic, and the next visitor waits while it starts.
  The website retries reads during that time and shows "Starting the engineering backend";
  writes are never retried, so nothing is applied twice.
- Measured in a container with the free instance's limits (512 MB, 0.1 CPU, CI on
  2026-10-14): ready 26 s after start; peak memory 295 MiB, never killed; a full visitor
  session (model, integration checks, both simulations, a 40-evaluation optimisation
  study, STEP export) took 13.7 minutes, most of it the optimisation study. It works, but
  slowly: the paid `starter` plan has more CPU when that matters.
- Disk is wiped on every deploy and restart. Only regenerable STEP exports live there; the
  projects are in Neon.

### 3. Frontend: Netlify

1. Sign up at netlify.com, **Add new site → Import an existing project → GitHub**, pick
   this repository. `netlify.toml` sets the base directory (`frontend`), the build
   command, the publish directory and the client-side route fallback.
2. `netlify.toml` sets `VITE_API_URL = "https://autevra.onrender.com"`. For another backend
   address, change it there or override it in **Site configuration → Environment
   variables**, then **Deploys → Trigger deploy**.
3. Put the Netlify address into Render's `AUTEVRA_CORS_ORIGINS`
   (**autevra-api → Environment**); Render restarts the service with it.

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

**Render, paid plans.** Change `plan:` in `render.yaml` to `starter` or `standard` for
more CPU and memory and no sleeping.

**Hugging Face Spaces (Docker).** Docker Spaces need a PRO subscription. If you have one,
`deploy/huggingface/build-space.sh` assembles the Space (Space card, LLM off, uid 1000)
and `.github/workflows/deploy-space.yml` pushes it after green CI on `main` once the
repository has the `HF_TOKEN` secret and the `HF_SPACE` variable (`<user>/autevra-api`).

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
