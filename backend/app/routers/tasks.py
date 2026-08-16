from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..ai_parser import mock_parse

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=schemas.TaskResponse, status_code=201)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/", response_model=List[schemas.TaskResponse])
def list_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()

@router.get("/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task_update.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}", status_code=200)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}

@router.post("/quick-add", response_model=schemas.TaskResponse, status_code=201)
def quick_add_task(data: dict, db: Session = Depends(get_db)):
    description = data.get("description", "")
    project_id = data.get("project_id")

    if not description or not project_id:
        raise HTTPException(status_code=422, detail="description and project_id are required")

    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=422, detail="Project not found")

    parsed = mock_parse(description)

    new_task = models.Task(
        title=parsed["title"],
        priority=parsed["priority"],
        due_date=parsed["due_date"],
        project_id=project_id,
        status="pending"
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task 
from ..algorithms import insertion_sort, binary_search, linear_search

@router.get("/sorted")
def get_sorted_tasks(sort: str = "priority", db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    records = [
        {
            "id": t.id,
            "title": t.title,
            "priority": t.priority,
            "due_date": t.due_date,
            "status": t.status,
            "project_id": t.project_id,
            "priority_rank": {"low": 1, "medium": 2, "high": 3}.get(t.priority, 2)
        }
        for t in tasks
    ]

    if sort == "priority":
        insertion_sort(records, "priority_rank")
    else:
        insertion_sort(records, "title")

    for r in records:
        r.pop("priority_rank", None)

    return records


@router.get("/search")
def search_task(title: str, algo: str = "binary", db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    records = [{"id": t.id, "title": t.title} for t in tasks]

    if algo == "binary":
        insertion_sort(records, "title")
        idx = binary_search(records, title, "title")
    else:
        idx = linear_search(records, title, "title")

    if idx == -1:
        raise HTTPException(status_code=404, detail="Task not found")

    task_id = records[idx]["id"]
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    return task

