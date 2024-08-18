from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, DateTime, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import json

import sqlalchemy
print(sqlalchemy.__version__)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    email = Column(String, nullable=True, unique=True)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    logs = relationship('OperationLog', back_populates='user')

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, is_admin={self.is_admin})>"

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'phone_number': self.phone_number,
            'email': self.email,
            'is_admin': self.is_admin,
            'is_active': self.is_active,
        }

    def json(self):
        return json.dumps(self.to_dict())



class Space(Base):
    __tablename__ = 'spaces'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    created_date = Column(DateTime, default=func.now())
    devices = relationship('Device', back_populates='space')
    scenes = relationship('Scene', back_populates='space')

    def __repr__(self):
        return f"<Space(id={self.id}, name={self.name})>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_date': self.created_date.isoformat() if self.created_date else None,
        }

    def json(self):
        return json.dumps(self.to_dict())

class Device(Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    eui = Column(String, unique=True, nullable=False)
    device_type = Column(String, nullable=False)
    timeout = Column(Integer, nullable=False)
    space_id = Column(Integer, ForeignKey('spaces.id'))
    online_status = Column(Boolean, default=False)
    power_status = Column(Boolean, default=False)
    set_temperature = Column(Float, nullable=True)
    fan_speed = Column(String, nullable=True)
    mode = Column(String, nullable=True)
    created_date = Column(DateTime, default=func.now())
    space = relationship('Space', back_populates='devices')
    schedules = relationship('DeviceSchedule', back_populates='device')
    alerts = relationship('Alert', back_populates='device')

    def __repr__(self):
        return f"<Device(id={self.id}, name={self.name}, device_type={self.device_type})>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'eui': self.eui,
            'device_type': self.device_type,
            'timeout': self.timeout,
            'space_id': self.space_id,
            'online_status': self.online_status,
            'power_status': self.power_status,
            'set_temperature': self.set_temperature,
            'fan_speed': self.fan_speed,
            'mode': self.mode,
            'created_date': self.created_date.isoformat() if self.created_date else None,
        }

    def json(self):
        return json.dumps(self.to_dict())

class Scene(Base):
    __tablename__ = 'scenes'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    space_id = Column(Integer, ForeignKey('spaces.id'))
    device_id = Column(Integer, ForeignKey('devices.id'))
    description = Column(String, nullable=True)
    created_date = Column(DateTime, default=func.now())
    space = relationship('Space', back_populates='scenes')
    device = relationship('Device')

    def __repr__(self):
        return f"<Scene(id={self.id}, name={self.name})>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'space_id': self.space_id,
            'device_id': self.device_id,
            'description': self.description,
            'created_date': self.created_date.isoformat() if self.created_date else None,
        }

    def json(self):
        return json.dumps(self.to_dict())


class DeviceSchedule(Base):
    __tablename__ = 'device_schedules'
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('devices.id'))
    task_template = Column(String, nullable=True)
    scene_template = Column(String, nullable=True)
    holiday_template = Column(String, nullable=True)
    online_status = Column(Boolean, default=False)
    created_date = Column(DateTime, default=func.now())
    device = relationship('Device', back_populates='schedules')

    def __repr__(self):
        return f"<DeviceSchedule(id={self.id}, device_id={self.device_id})>"

    def to_dict(self):
        return {
            'id': self.id,
            'device_id': self.device_id,
            'task_template': self.task_template,
            'scene_template': self.scene_template,
            'holiday_template': self.holiday_template,
            'online_status': self.online_status,
            'created_date': self.created_date.isoformat() if self.created_date else None,
        }

    def json(self):
        return json.dumps(self.to_dict())


class ScheduledTask(Base):
    __tablename__ = 'scheduled_tasks'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    task_type = Column(String, nullable=False)
    device_id = Column(Integer, ForeignKey('devices.id'))
    execution_period = Column(String, nullable=False)
    execution_date_id = Column(Integer, ForeignKey('execution_dates.id'))
    status = Column(Boolean, default=True)
    notes = Column(String, nullable=True)
    created_date = Column(DateTime, default=func.now())

    device = relationship('Device')
    execution_dates = relationship("ExecutionDate", back_populates="task", foreign_keys="[ExecutionDate.task_id]")

    def __repr__(self):
        return f"<ScheduledTask(id={self.id}, name={self.name}, task_type={self.task_type})>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'task_type': self.task_type,
            'device_id': self.device_id,
            'execution_period': self.execution_period,
            'execution_date_id': self.execution_date_id,
            'status': self.status,
            'notes': self.notes,
            'created_date': self.created_date.isoformat() if self.created_date else None,
        }

    def json(self):
        return json.dumps(self.to_dict())
    
class ExecutionDate(Base):
    __tablename__ = 'execution_dates'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    task_id = Column(Integer, ForeignKey('scheduled_tasks.id'))
    created_date = Column(DateTime, default=func.now())

    task = relationship("ScheduledTask", back_populates="execution_dates", foreign_keys="[ExecutionDate.task_id]")

    def __repr__(self):
        return f"<ExecutionDate(id={self.id}, name={self.name})>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'task_id': self.task_id,
            'created_date': self.created_date.isoformat() if self.created_date else None,
        }

    def json(self):
        return json.dumps(self.to_dict())

class Alert(Base):
    __tablename__ = 'alerts'
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('devices.id'))
    energy_type = Column(String, nullable=False)
    time_scale = Column(String, nullable=False)
    upper_limit = Column(Float, nullable=False)
    lower_limit = Column(Float, nullable=False)
    alert_bot = Column(String, nullable=True)
    created_date = Column(DateTime, default=func.now())
    device = relationship('Device', back_populates='alerts')

    def __repr__(self):
        return f"<Alert(id={self.id}, device_id={self.device_id}, energy_type={self.energy_type})>"

    def to_dict(self):
        return {
            'id': self.id,
            'device_id': self.device_id,
            'energy_type': self.energy_type,
            'time_scale': self.time_scale,
            'upper_limit': self.upper_limit,
            'lower_limit': self.lower_limit,
            'alert_bot': self.alert_bot,
            'created_date': self.created_date.isoformat() if self.created_date else None,
        }

    def json(self):
        return json.dumps(self.to_dict())


class OperationLog(Base):
    __tablename__ = 'operation_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    operation_description = Column(String, nullable=False)
    operation_time = Column(DateTime, default=func.now())
    user = relationship('User', back_populates='logs')

    def __repr__(self):
        return f"<OperationLog(id={self.id}, user_id={self.user_id}, operation_description={self.operation_description})>"

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'operation_description': self.operation_description,
            'operation_time': self.operation_time.isoformat() if self.operation_time else None,
        }

    def json(self):
        return json.dumps(self.to_dict())

class MonitoringDashboard(Base):
    __tablename__ = 'monitoring_dashboard'
    id = Column(Integer, primary_key=True)
    space_id = Column(Integer, ForeignKey('spaces.id'))
    device_online_rate = Column(Float, nullable=False)
    total_electricity_today = Column(Float, nullable=False)
    total_water_today = Column(Float, nullable=False)
    indoor_environment = Column(String, nullable=True)
    outdoor_environment = Column(String, nullable=True)
    created_date = Column(DateTime, default=func.now())
    space = relationship('Space')

    def __repr__(self):
        return f"<MonitoringDashboard(id={self.id}, space_id={self.space_id}, device_online_rate={self.device_online_rate})>"

    def to_dict(self):
        return {
            'id': self.id,
            'space_id': self.space_id,
            'device_online_rate': self.device_online_rate,
            'total_electricity_today': self.total_electricity_today,
            'total_water_today': self.total_water_today,
            'indoor_environment': self.indoor_environment,
            'outdoor_environment': self.outdoor_environment,
            'created_date': self.created_date.isoformat() if self.created_date else None,
        }

    def json(self):
        return json.dumps(self.to_dict())

