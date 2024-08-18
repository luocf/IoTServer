from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import create_space, get_space_by_id
from app.schemas import SpaceCreate, SpaceResponse
from app.db import get_db

router = APIRouter()

@router.post("/spaces/", response_model=SpaceResponse)
def create_space_endpoint(space: SpaceCreate, db: Session = Depends(get_db)):
    return create_space(db, space)

@router.get("/spaces/{space_id}", response_model=SpaceResponse)
def read_space(space_id: int, db: Session = Depends(get_db)):
    space = get_space_by_id(db, space_id)
    if space is None:
        raise HTTPException(status_code=404, detail="Space not found")
    return space
