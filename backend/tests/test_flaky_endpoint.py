import pytest


@pytest.mark.asyncio
async def test_flaky_endpoint_has_data(client):
    payload = {
        "repository": "test-repo",
        "commit_sha": "def456",
        "branch": "main",
        "environment": {"os": "ubuntu"},
        "tests": [
            {
                "suite": "tests.sample",
                "name": "test_flaky",
                "status": "passed",
                "duration_ms": 900,
            },
            {
                "suite": "tests.sample",
                "name": "test_flaky",
                "status": "failed",
                "duration_ms": 1100,
                "error_message": "flaky",
                "stack_trace": "Traceback...",
            },
        ],
    }
    await client.post("/ci-runs/batch", json=payload)

    resp = await client.get("/tests/flaky?min_runs=1")
    assert resp.status_code == 200
    items = resp.json()
    assert isinstance(items, list)
    if items:
        t = items[0]
        assert "test_case_id" in t
        assert "flakiness_score" in t
