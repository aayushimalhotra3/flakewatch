from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_session
from .schemas_ci import CiRunBatch
from .services_ci import ingest_ci_run_batch

router = APIRouter(prefix="/ci-runs", tags=["ci"])

@router.post("/batch", status_code=status.HTTP_201_CREATED)
async def ingest_batch(payload: CiRunBatch, session: AsyncSession = Depends(get_session)):
    result = await ingest_ci_run_batch(session, payload)
    return result
