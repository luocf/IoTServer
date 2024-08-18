from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    phone_number: Optional[str] = None
    is_admin: Optional[bool] = False

class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str]
    phone_number: Optional[str]
    is_admin: bool
    is_active: bool

    class Config:
        from_attributes = True

class SpaceCreate(BaseModel):
    name: str
    description: Optional[str] = None

class SpaceResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_date: datetime

    class Config:
        from_attributes = True

class DeviceCreate(BaseModel):
    name: str
    eui: str
    device_type: str
    timeout: int
    space_id: int
    online_status: Optional[bool] = False
    power_status: Optional[bool] = False
    set_temperature: Optional[float] = None
    fan_speed: Optional[str] = None
    mode: Optional[str] = None

class DeviceResponse(BaseModel):
    id: int
    name: str
    eui: str
    device_type: str
    timeout: int
    space_id: int
    online_status: bool
    power_status: bool
    set_temperature: Optional[float]
    fan_speed: Optional[str]
    mode: Optional[str]
    created_date: datetime

    class Config:
        from_attributes = True
