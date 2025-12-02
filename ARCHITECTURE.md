# FlakeWatch Architecture

## Goal
FlakeWatch helps teams identify CI test flakiness by ingesting test runs over time and computing per-test instability. It focuses on time-series data of test executions and lightweight analytics.

## Domain model
- Repository: a code repository under analysis.
- TestCase: a specific test within a repository (suite_name, test_name, full_name).
- TestRun: a single execution of a test case with status, timing, environment, and error info.

Flakiness is computed directly from `TestRun` aggregates for now; there is no separate stats table.

## Key flows
- CI run ingestion
  - Client posts a batch → `POST /ci-runs/batch`
  - Backend upserts repository and test cases → inserts runs
- Flaky tests query
  - `GET /tests/flaky` performs a grouped query on `test_runs` and computes `flakiness_score` as `min(failures, passes) / runs`
- Test detail
  - `GET /tests/{id}` aggregates stats for one test and returns recent runs

## Architecture
- Backend: FastAPI app with async SQLAlchemy; Alembic migrations manage schema.
- Frontend: SPA (React + Vite) calling `GET /tests/flaky` and `GET /tests/{id}`.
- Dev environment: Postgres via Docker Compose; seed script populates demo data.
