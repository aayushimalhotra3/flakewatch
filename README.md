FlakeWatch – CI flakiness and test failure analytics with FastAPI and React.

## Overview
FlakeWatch is a CI analytics tool that ingests test results over time, computes a flakiness score per test, and surfaces flaky tests and failure patterns via a React dashboard.

## Features
- CI batch ingestion endpoint (`POST /ci-runs/batch`)
- Flakiness analytics (`GET /tests/flaky`) with a simple instability score
- Per-test detail: recent runs, branches, errors (`GET /tests/{test_case_id}`)
- Seed script to generate demo data (`python -m flakewatch.demo_seed`)
- React dashboard: flaky tests table + test detail view

## Tech stack
- Backend: FastAPI, async SQLAlchemy, Postgres, Alembic, pytest
- Frontend: React, TypeScript, Vite

## Local development
```sh
docker compose up db

cd backend
python -m pip install -r requirements.txt
alembic upgrade head
python -m flakewatch.demo_seed
./dev.sh

# new terminal
cd ../frontend
npm install
npm run dev
```

## API sketch
- `GET /health`
- `POST /ci-runs/batch`
- `GET /tests/flaky`
- `GET /tests/{test_case_id}`
