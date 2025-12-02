from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_session
from .schemas_tests import FlakyTestSummary, TestDetail
from .services_tests import get_top_flaky_tests, get_test_detail

router = APIRouter(prefix="/tests", tags=["tests"])

@router.get("/flaky", response_model=list[FlakyTestSummary])
async def list_flaky_tests(
    session: AsyncSession = Depends(get_session),
    limit: int = Query(50, ge=1, le=200),
    min_runs: int = Query(5, ge=1),
    repository: str | None = Query(None),
):
    return await get_top_flaky_tests(
        session=session,
        limit=limit,
        min_runs=min_runs,
        repository_name=repository,
    )

@router.get("/{test_case_id}", response_model=TestDetail)
async def get_test(
    test_case_id: int,
    session: AsyncSession = Depends(get_session),
):
    detail = await get_test_detail(session, test_case_id)
    if detail is None:
        raise HTTPException(status_code=404, detail="Test case not found")
    return detail
