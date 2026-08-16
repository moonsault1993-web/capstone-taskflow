from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=schemas.ProjectResponse, status_code=201)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    db_project = models.Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.get("/", response_model=List[schemas.ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()

@router.get("/stats")
def project_stats(db: Session = Depends(get_db)):
    results = (
        db.query(
            models.Project.id,
            models.Project.name,
            func.count(models.Task.id).label("task_count")
        )
        .outerjoin(models.Task)
        .group_by(models.Project.id)
        .all()
    )
    return [
        {
            "project_id": r.id,
            "project_name": r.name,
            "task_count": r.task_count
        }
        for r in results
    ]                                                                                                                             