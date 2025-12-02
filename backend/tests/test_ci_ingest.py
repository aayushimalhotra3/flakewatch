import pytest


@pytest.mark.asyncio
async def test_ci_batch_creates_runs(client):
    payload = {
        "repository": "test-repo",
        "commit_sha": "abc123",
        "branch": "main",
        "environment": {"os": "ubuntu"},
        "tests": [
            {
                "suite": "tests.sample",
                "name": "test_ok",
                "status": "passed",
                "duration_ms": 1000,
            },
            {
                "suite": "tests.sample",
                "name": "test_fail",
                "status": "failed",
                "duration_ms": 1200,
                "error_message": "boom",
                "stack_trace": "Traceback...",
            },
        ],
    }

    resp = await client.post("/ci-runs/batch", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["repository"] == "test-repo"
    assert data["runs_created"] == 2
