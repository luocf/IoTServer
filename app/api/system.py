from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import SystemListRequest, SystemListResponse, AddStaffRequest, AddStaffResponse, StaffListRequest, StaffListResponse
from app.services.system_service import (
    query_system_list, add_system_staff, query_system_staff
)
from app.db import get_db

router = APIRouter()

@router.get("/system/list", response_model=SystemListResponse)
def get_system_list(request: SystemListRequest, db: Session = Depends(get_db)):
    response = query_system_list(db, request)
    if response.code != "0":
        raise HTTPException(status_code=400, detail=response.errMsg)
    return response

@router.post("/system/staff/add", response_model=AddStaffResponse)
def add_staff(request: AddStaffRequest, db: Session = Depends(get_db)):
    response = add_system_staff(db, request)
    if response.code != "0":
        raise HTTPException(status_code=400, detail=response.errMsg)
    return response

@router.get("/system/staff/list", response_model=StaffListResponse)
def get_staff_list(request: StaffListRequest, db: Session = Depends(get_db)):
    response = query_system_staff(db, request)
    if response.code != "0":
        raise HTTPException(status_code=400, detail=response.errMsg)
    return response
