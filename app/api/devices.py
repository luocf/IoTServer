from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import create_device, get_device_by_id
from app.schemas import DeviceCreate, DeviceResponse
from app.db import get_db
import redis

router = APIRouter()
r = redis.Redis(host='localhost', port=6379, db=0)

@router.post("/devices/", response_model=DeviceResponse)
def create_device_endpoint(device: DeviceCreate, db: Session = Depends(get_db)):
    return create_device(db, device)

@router.get("/devices/{device_id}", response_model=DeviceResponse)
def read_device(device_id: int, db: Session = Depends(get_db)):
    device = r.get(f"device:{device_id}")
    if device:
        return DeviceResponse.model_validate_json(device)
    
    device = get_device_by_id(db, device_id)
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    
    r.setex(f"device:{device_id}", 3600, device.json())  # Cache device info for 1 hour
    return device
