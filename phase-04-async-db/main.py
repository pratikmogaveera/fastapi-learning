from datetime import datetime

from database import get_db
from fastapi import Depends, FastAPI, HTTPException
from models import Links
from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

# Phase 4 — Async Database (SQLAlchemy + Alembic)
# Complete Phase 1–3 first, then come back here.
# See PLAN.md Phase 4 for tasks.


class CreateLinkRequest(BaseModel):
    short_code: str = Field(pattern="^[-_a-z0-9]+$")
    original_url: AnyHttpUrl


class LinkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    short_code: str
    original_url: str
    created_at: datetime


@app.get("/links", response_model=list[LinkResponse])
async def get_links(session: AsyncSession = Depends(get_db)):
    query = select(Links)
    result = await session.execute(query)

    return result.scalars().all()


@app.get("/links/{short_code}", response_model=LinkResponse)
async def get_links_by_short_code(short_code: str, session: AsyncSession = Depends(get_db)):
    query = select(Links).where(Links.short_code == short_code)
    result = await session.execute(query)
    link = result.scalar_one_or_none()
    if link is None:
        raise HTTPException(status_code=404, detail="Link not found")
    return link


@app.post("/links", response_model=LinkResponse)
async def create_link(payload: CreateLinkRequest, session: AsyncSession = Depends(get_db)):
    new_link = Links(short_code=payload.short_code, original_url=str(payload.original_url))
    session.add(new_link)
    await session.commit()
    await session.refresh(new_link)

    return new_link
