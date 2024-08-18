from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import app.crud, app.schemas as schemas
from app.db import get_db
from typing import List

router = APIRouter()

@router.post("/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)

@router.get("/", response_model=List[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_tasks(db=db, skip=skip, limit=limit)
