# FlakeWatch – Interview Notes

## 30–60 second pitch
FlakeWatch is a developer-facing CI analytics tool that ingests test results, computes a simple flakiness score per test, and surfaces unstable tests in a small React dashboard. The backend uses FastAPI with async SQLAlchemy and Alembic; the frontend is React + TypeScript. It’s designed to quickly highlight instability and provide per-test context with recent runs.

## Key talking points
- Flakiness score: computed as `min(failures, passes) / runs` to capture instability, differentiating flaky from consistently failing tests.
- Flaky vs failing: flaky tests alternate outcomes over time; consistently failing tests are stable but broken. Prioritizing flaky tests reduces noise and developer frustration.
- Extensibility: add failure clustering via normalized stack-trace hashing, test ownership metadata, quarantining flaky tests, and scheduled aggregation jobs.

## Possible questions & short answers
- Q: How do you define a flaky test?
  - A: Using an instability metric based on historical runs: `min(failures, passes) / runs`. If both passes and failures exist, the score rises; if all runs are the same outcome, score is 0.
- Q: How would you scale this?
  - A: Add indexes on key columns (`test_case_id`, `commit_sha`, `branch`, `run_at`), move heavy analytics to background jobs, materialize aggregates, and shard by repository.
- Q: How would you detect failure patterns?
  - A: Normalize stack traces and compute content hashes; group failures by similarity to surface common root causes.
