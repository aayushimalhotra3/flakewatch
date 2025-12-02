from typing import List
from sqlalchemy import select, func, case
from sqlalchemy.ext.asyncio import AsyncSession

from .models import TestRun, TestCase, Repository
from .schemas_tests import FlakyTestSummary, TestDetail, TestRunSummary

async def get_top_flaky_tests(
    session: AsyncSession,
    limit: int = 50,
    min_runs: int = 5,
    repository_name: str | None = None,
) -> List[FlakyTestSummary]:
    status_failed = case((TestRun.status == "failed", 1), else_=0)
    status_passed = case((TestRun.status == "passed", 1), else_=0)
    stmt = (
        select(
            TestCase.id.label("test_case_id"),
            Repository.name.label("repository"),
            TestCase.suite_name,
            TestCase.test_name,
            func.count(TestRun.id).label("runs"),
            func.sum(status_failed).label("failures"),
            func.sum(status_passed).label("passes"),
            func.max(TestRun.run_at).label("last_run_at"),
        )
        .join(TestRun, TestRun.test_case_id == TestCase.id)
        .join(Repository, Repository.id == TestCase.repository_id)
        .group_by(TestCase.id, Repository.name, TestCase.suite_name, TestCase.test_name)
    )
    if repository_name:
        stmt = stmt.where(Repository.name == repository_name)
    result = await session.execute(stmt)
    rows = result.all()
    summaries: List[FlakyTestSummary] = []
    for r in rows:
        runs = int(r.runs)
        if runs < min_runs:
            continue
        failures = int(r.failures or 0)
        passes = int(r.passes or 0)
        failure_rate = (failures / runs) if runs else 0.0
        flakiness_score = (min(failures, passes) / runs) if runs else 0.0
        summaries.append(
            FlakyTestSummary(
                test_case_id=int(r.test_case_id),
                repository=str(r.repository),
                suite_name=str(r.suite_name),
                test_name=str(r.test_name),
                runs=runs,
                failures=failures,
                passes=passes,
                failure_rate=failure_rate,
                flakiness_score=flakiness_score,
                last_run_at=r.last_run_at,
            )
        )
    summaries.sort(key=lambda x: (x.flakiness_score, x.failure_rate), reverse=True)
    return summaries[:limit]

async def get_test_detail(
    session: AsyncSession,
    test_case_id: int,
    recent_limit: int = 50,
) -> TestDetail | None:
    status_failed = case((TestRun.status == "failed", 1), else_=0)
    status_passed = case((TestRun.status == "passed", 1), else_=0)
    agg_stmt = (
        select(
            TestCase.id.label("test_case_id"),
            Repository.name.label("repository"),
            TestCase.suite_name,
            TestCase.test_name,
            func.count(TestRun.id).label("runs"),
            func.sum(status_failed).label("failures"),
            func.sum(status_passed).label("passes"),
            func.max(TestRun.run_at).label("last_run_at"),
        )
        .join(TestRun, TestRun.test_case_id == TestCase.id)
        .join(Repository, Repository.id == TestCase.repository_id)
        .where(TestCase.id == test_case_id)
        .group_by(TestCase.id, Repository.name, TestCase.suite_name, TestCase.test_name)
    )
    agg_result = await session.execute(agg_stmt)
    row = agg_result.fetchone()
    if row is None:
        return None
    runs = int(row.runs or 0)
    failures = int(row.failures or 0)
    passes = int(row.passes or 0)
    failure_rate = (failures / runs) if runs > 0 else 0.0
    flakiness_score = (min(failures, passes) / runs) if runs > 0 else 0.0
    runs_stmt = (
        select(
            TestRun.id,
            TestRun.status,
            TestRun.commit_sha,
            TestRun.branch,
            TestRun.duration_ms,
            TestRun.run_at,
            TestRun.error_message,
        )
        .where(TestRun.test_case_id == test_case_id)
        .order_by(TestRun.run_at.desc())
        .limit(recent_limit)
    )
    runs_result = await session.execute(runs_stmt)
    recent_runs = [
        TestRunSummary(
            id=r.id,
            status=r.status,
            commit_sha=r.commit_sha,
            branch=r.branch,
            duration_ms=r.duration_ms,
            run_at=r.run_at,
            error_message=r.error_message,
        )
        for r in runs_result.fetchall()
    ]
    return TestDetail(
        test_case_id=int(row.test_case_id),
        repository=str(row.repository),
        suite_name=str(row.suite_name),
        test_name=str(row.test_name),
        runs=runs,
        failures=failures,
        passes=passes,
        failure_rate=failure_rate,
        flakiness_score=flakiness_score,
        last_run_at=row.last_run_at,
        recent_runs=recent_runs,
    )
