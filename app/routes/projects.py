from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Project
from app.schemas import ProjectCreate, ProjectResponse
from sqlalchemy.future import select

router = APIRouter()

@router.post("/projects/", response_model=ProjectResponse)
async def create_project(project: ProjectCreate, db: AsyncSession = Depends(get_db)):
    new_project = Project(name=project.name, description=project.description)
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)
    return new_project

@router.get("/projects/", response_model=list[ProjectResponse])
async def get_projects(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project))
    return result.scalars().all()
