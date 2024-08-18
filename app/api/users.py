from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import create_user, get_user_by_id
from app.schemas import UserCreate, UserResponse
from app.db import get_db
import redis

router = APIRouter()
r = redis.Redis(host='localhost', port=6379, db=0)

@router.post("/users/", response_model=UserResponse)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Username already registered")
    return db_user

@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = r.get(f"user:{user_id}")
    if user:
        return UserResponse.model_validate_json(user)
    
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    r.setex(f"user:{user_id}", 3600, user.json())  # Cache user info for 1 hour
    return user
