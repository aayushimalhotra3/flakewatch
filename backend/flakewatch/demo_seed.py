import asyncio
from datetime import datetime, timedelta, timezone
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .database import async_session
from .models import Repository, TestCase, TestRun


async def ensure_repo(session: AsyncSession, name: str) -> Repository:
    result = await session.execute(select(Repository).where(Repository.name == name))
    repo = result.scalar_one_or_none()
    if repo:
        return repo
    repo = Repository(name=name)
    session.add(repo)
    await session.flush()
    return repo


async def ensure_test_case(session: AsyncSession, repository_id: int, suite: str, name: str) -> TestCase:
    full_name = f"{suite}::{name}"
    result = await session.execute(
        select(TestCase).where(TestCase.repository_id == repository_id, TestCase.full_name == full_name)
    )
    tc = result.scalar_one_or_none()
    if tc:
        return tc
    tc = TestCase(repository_id=repository_id, suite_name=suite, test_name=name, full_name=full_name)
    session.add(tc)
    await session.flush()
    return tc


async def seed() -> None:
    now = datetime.now(timezone.utc)
    async with async_session() as session:
        repos = ["demo-backend", "demo-service"]
        for rname in repos:
            repo = await ensure_repo(session, rname)
            tests = [
                ("tests.api.users", "test_create_user", ["passed"] * 10),
                ("tests.api.users", "test_delete_user", ["failed"] * 10),
                (
                    "tests.api.orders",
                    "test_checkout",
                    ["passed" if i % 2 == 0 else "failed" for i in range(10)],
                ),
            ]
            for suite, name, statuses in tests:
                tc = await ensure_test_case(session, repo.id, suite, name)
                for i, status in enumerate(statuses):
                    at = now - timedelta(days=(len(statuses) - 1 - i))
                    run = TestRun(
                        test_case_id=tc.id,
                        commit_sha=f"{rname[:3]}{i:05d}seed",
                        branch="main",
                        status=status,
                        duration_ms=800 + i * 20,
                        environment_json={"seed": True, "repo": rname},
                        error_message=("AssertionError: demo failure" if status == "failed" else None),
                        stack_trace=("Traceback..." if status == "failed" else None),
                        run_at=at,
                    )
                    session.add(run)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())
