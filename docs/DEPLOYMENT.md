# Deployment

Autevra is local-first: `make dev` on the Mac is the primary way to run it. This page
describes a hosted demo of the same code.

## Shape

| Part | What it is | Host |
|---|---|---|
| Website, workspace, studio | Static files from `npm run build` (`frontend/dist`) | Netlify (`netlify.toml`) |
| Backend API | FastAPI + CadQuery/OCCT in the `backend/Dockerfile` image (linux/amd64) | Any container host with **≥ 1 GB RAM** and x86_64 (options below) |
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

## 1. Database: Neon

1. Create a Neon project (Postgres 17) and copy the connection string from the
   dashboard (`postgresql://…@ep-….neon.tech/neondb?sslmode=require`).
2. The backend accepts it unchanged: `postgres://` and `postgresql://` URLs are rewritten
   to the psycopg 3 driver, and migrations run automatically at startup.
3. Keep it out of git; enter it only as a secret environment variable on the backend host.

## 2. Backend: pick one host

Environment for every host:

| Variable | Value |
|---|---|
| `AUTEVRA_DATABASE_URL` | the Neon connection string (secret) |
| `AUTEVRA_CORS_ORIGINS` | `["https://<your-site>.netlify.app"]` (JSON list) |
| `AUTEVRA_LLM_PROVIDER` | `off` |
| `AUTEVRA_DATA_DIR` | `/tmp/autevra` |

The image listens on `$PORT` when the host sets it (Render, Cloud Run, Spaces), otherwise 8000.
Health check: `GET /api/health`.

**a. Google Cloud Run (recommended for a low-traffic demo).** 2 GiB instances that scale
to zero, so a demo usually stays inside the monthly free allowance; it needs a Google
Cloud billing account.

```sh
# once: store the Neon URL in Secret Manager
printf '%s' 'postgresql://…' | gcloud secrets create autevra-database-url --data-file=-

# "^|^" makes "|" the separator, because the CORS list is JSON
gcloud run deploy autevra-api --source backend --region europe-west1 \
  --memory 2Gi --cpu 1 --allow-unauthenticated \
  --set-env-vars '^|^AUTEVRA_LLM_PROVIDER=off|AUTEVRA_DATA_DIR=/tmp/autevra|AUTEVRA_CORS_ORIGINS=["https://<your-site>.netlify.app"]' \
  --set-secrets AUTEVRA_DATABASE_URL=autevra-database-url:latest
```

**b. Render.** Connect the GitHub repository as a Blueprint (`render.yaml`); it deploys on
every push to `main`. The blueprint uses the `standard` plan (2 GB) because the 512 MB plans
are too small. Enter the two `sync: false` variables in the dashboard.

**c. Hugging Face Spaces (Docker).** The free CPU tier has enough memory. The Space is its
own git repository, so it needs the backend copied in with `app_port: 8000` in the Space
README. It sleeps when unused.

## 3. Frontend: Netlify

1. Import the GitHub repository in Netlify. `netlify.toml` sets the base directory
   (`frontend`), the build command, the publish directory and the client-side route fallback.
2. In the site's environment variables, set `VITE_API_URL` to the backend URL
   (for example `https://autevra-api-….run.app`), then trigger a deploy.
3. Add the Netlify URL to the backend's `AUTEVRA_CORS_ORIGINS`.

## 4. Check the deployment

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
