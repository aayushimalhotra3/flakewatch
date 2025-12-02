from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_session
from .models import Repository

router = APIRouter()

@router.get("/repositories")
async def repositories_count(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(func.count()).select_from(Repository))
    return {"count": result.scalar_one()}
