from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Repository, TestCase, TestRun
from .schemas_ci import CiRunBatch

async def get_or_create_repository(session: AsyncSession, name: str) -> Repository:
    result = await session.execute(select(Repository).where(Repository.name == name))
    repo = result.scalar_one_or_none()
    if repo:
        return repo
    repo = Repository(name=name)
    session.add(repo)
    await session.flush()
    return repo

async def get_or_create_test_case(session: AsyncSession, repository_id: int, suite: str, name: str) -> TestCase:
    full_name = f"{suite}::{name}"
    result = await session.execute(
        select(TestCase).where(TestCase.repository_id == repository_id, TestCase.full_name == full_name)
    )
    tc = result.scalar_one_or_none()
    if tc:
        return tc
    tc = TestCase(
        repository_id=repository_id,
        suite_name=suite,
        test_name=name,
        full_name=full_name,
    )
    session.add(tc)
    await session.flush()
    return tc

async def ingest_ci_run_batch(session: AsyncSession, batch: CiRunBatch) -> dict:
    repo = await get_or_create_repository(session, batch.repository)
    created_runs = 0
    for t in batch.tests:
        tc = await get_or_create_test_case(session=session, repository_id=repo.id, suite=t.suite, name=t.name)
        run = TestRun(
            test_case_id=tc.id,
            commit_sha=batch.commit_sha,
            branch=batch.branch,
            status=t.status,
            duration_ms=t.duration_ms,
            environment_json=batch.environment,
            error_message=t.error_message,
            stack_trace=t.stack_trace,
        )
        session.add(run)
        created_runs += 1
    await session.commit()
    return {"repository": batch.repository, "test_cases": len(batch.tests), "runs_created": created_runs}
