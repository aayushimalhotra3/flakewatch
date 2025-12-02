from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class FlakyTestSummary(BaseModel):
    test_case_id: int
    repository: str
    suite_name: str
    test_name: str
    runs: int
    failures: int
    passes: int
    failure_rate: float
    flakiness_score: float
    last_run_at: Optional[datetime]

class TestRunSummary(BaseModel):
    id: int
    status: str
    commit_sha: str
    branch: str
    duration_ms: int | None
    run_at: datetime
    error_message: str | None

class TestDetail(BaseModel):
    test_case_id: int
    repository: str
    suite_name: str
    test_name: str
    runs: int
    failures: int
    passes: int
    failure_rate: float
    flakiness_score: float
    last_run_at: datetime | None
    recent_runs: List[TestRunSummary]
