---
title: Autevra API
emoji: 🚗
colorFrom: blue
colorTo: gray
sdk: docker
app_port: 8000
pinned: false
short_description: Backend API of Autevra, a parametric automotive CAD platform
---

# Autevra API

The engineering backend (FastAPI, CadQuery/OCCT, vehicle simulation) of
[Autevra](https://github.com/UtkarshMehta7/autevra). This Space is deployed
automatically from the `backend/` directory of that repository; do not edit it here.

- Health: `/api/health`
- API documentation: `/docs`

The free tier sleeps when unused, so the first request after a pause takes a minute or
two. Projects are stored in an external Postgres database, not in the Space.
