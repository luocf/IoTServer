import uuid
from sqlalchemy import Column, String, Integer, Float, Text, ForeignKey, TIMESTAMP, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import sqlalchemy

print(sqlalchemy.__version__)

Base = declarative_base()

def generate_area_id():
    return str(uuid.uuid4())

# 超级管理员表
class SuperAdmin(Base):
    __tablename__ = "super_admins"

    super_admin_id = Column(String(64), primary_key=True)
    password = Column(String(256), nullable=False)
    phone_number = Column(String(15), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
class BackgroundImage(Base):
    __tablename__ = "background_images"

    id = Column(String, primary_key=True, index=True)
    system_id = Column(String, ForeignKey("systems.system_id"), nullable=False)
    file_token = Column(String, unique=True, nullable=False)
    file_path = Column(String, nullable=False)
    original_name = Column(String, nullable=False)
    system = relationship("System", back_populates="background_images")
    
# 系统表
class System(Base):
    __tablename__ = "systems"

    system_id = Column(String(64), primary_key=True)
    system_name = Column(String(128), unique=True, nullable=False)
    admin_id = Column(String(64), ForeignKey("super_admins.super_admin_id"))
    admin_password = Column(String(256), nullable=False)
    admin_phone_number = Column(String(15), nullable=False)
    status = Column(String(10), nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    background_images = relationship("BackgroundImage", back_populates="system")


# 用户表
class User(Base):
    __tablename__ = "users"

    user_id = Column(String(64), primary_key=True)
    phone_number = Column(String(15), nullable=False)
    password = Column(String(256), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

# 空间表
class Area(Base):
    __tablename__ = "areas"

    area_id = Column(String(64), primary_key=True, default=generate_area_id)
    system_id = Column(String(64), ForeignKey("systems.system_id"))
    area_name = Column(String(128), nullable=False)
    area_location = Column(String(256), nullable=False)
    area_value = Column(Float, nullable=False)
    area_height = Column(Float, nullable=False)
    memo = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


# 验证码表
class VerificationCode(Base):
    __tablename__ = "verification_codes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    super_admin_id = Column(String(64), ForeignKey("super_admins.super_admin_id"))
    code = Column(String(6), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    expires_at = Column(TIMESTAMP, nullable=False)

# 设备管理
class Host(Base):
    __tablename__ = "hosts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    system_id = Column(String(255), nullable=False)
    host_no = Column(Integer, unique=True, nullable=False)
    dev_eui = Column(String(255), unique=True, nullable=False)
    host_type = Column(String(50), nullable=False)
    host_name = Column(String(255), nullable=True)
    max_connection = Column(Integer, nullable=True)
    location = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    user_name = Column(String(255), nullable=True)
    phone_num = Column(String(20), nullable=True)
    memo = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class NodeHistory(Base):
    __tablename__ = "node_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    node_id = Column(Integer, ForeignKey('nodes.id'), nullable=False)  # 外键，指向 nodes 表
    date = Column(DateTime, nullable=False, default=func.now())  # 默认是当前时间
    param_value = Column(Float, nullable=False)  # 参数值

    # 定义与 Node 的关系
    node = relationship("Node", back_populates="history")

    def __repr__(self):
        return f"<NodeHistory(node_id={self.node_id}, date={self.date}, param_value={self.param_value})>"


class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    system_id = Column(String(255), nullable=False)
    host_no = Column(Integer, nullable=False)
    dev_eui = Column(String(255), unique=True, nullable=False)
    dev_name = Column(String(255), nullable=False)
    dev_type = Column(String(50), nullable=False)
    dev_port = Column(Integer, nullable=True)
    location = Column(String(255), nullable=True)
    memo = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # 反向引用 NodeHistory
    history = relationship("NodeHistory", back_populates="node")
    
    def __repr__(self):
        return f"<Node(id={self.id}, system_id='{self.system_id}', dev_name='{self.dev_name}', dev_eui='{self.dev_eui}')>"
    
class HostOperationsLog(Base):
    __tablename__ = "host_operations_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    host_no = Column(Integer, nullable=False)
    operation = Column(String(50), nullable=False)
    user = Column(String(255), nullable=True)
    status_code = Column(String(10), nullable=True)
    status_message = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

class NodeOperationsLog(Base):
    __tablename__ = "node_operations_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    node_id = Column(Integer, nullable=False)
    operation = Column(String(50), nullable=False)
    user = Column(String(255), nullable=True)
    status_code = Column(String(10), nullable=True)
    status_message = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

# 任务管理
class Task(Base):
    __tablename__ = "tasks"
    
    task_id = Column(Integer, primary_key=True, index=True)
    system_id = Column(String, index=True)
    task_name = Column(String)
    task_type = Column(String)
    action = Column(String)
    act_time = Column(Integer)
    act_on_time = Column(Integer)
    number1 = Column(Integer)
    setup_day = Column(String)
    repeat_mode = Column(String)
    interval_day = Column(Integer, nullable=True)
    act_day = Column(String, nullable=True)
    cycle_num = Column(Integer, nullable=True)
    concurrent = Column(Integer, nullable=True)
    area_id = Column(String)
    memo = Column(Text, nullable=True)
    

class TaskStartTime(Base):
    __tablename__ = "task_start_times"

    start_id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String(50), ForeignKey("tasks.task_id"))
    begin_time = Column(TIMESTAMP, nullable=False)

class TaskSenseParam(Base):
    __tablename__ = "task_sense_params"

    sense_id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String(50), ForeignKey("tasks.task_id"))
    high_value = Column(Float, nullable=False)
    high_act = Column(String(20), nullable=False)
    low_value = Column(Float, nullable=False)
    low_act = Column(String(20), nullable=False)

class TaskRunMode(Base):
    __tablename__ = "task_run_modes"

    mode_id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String(50), ForeignKey("tasks.task_id"))
    run_mode = Column(String(20), nullable=False)

class TaskHistory(Base):
    __tablename__ = "task_histories"

    history_id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String(50), ForeignKey("tasks.task_id"))
    action = Column(String(20), nullable=False)
    run_mode = Column(String(20), nullable=False)
    executed_at = Column(TIMESTAMP, nullable=False)
    status = Column(String(20), nullable=False)
    memo = Column(Text, nullable=True)

# 报告管理
class Report(Base):
    __tablename__ = "reports"

    report_id = Column(String(50), primary_key=True)
    report_name = Column(String(100), nullable=False)
    created_date = Column(TIMESTAMP, nullable=False)
    user_id = Column(String(50), ForeignKey("users.user_id"))

# 人员管理
class Admin(Base):
    __tablename__ = "admins"

    admin_id = Column(String(50), primary_key=True)
    admin_name = Column(String(100), nullable=False)

class HistoryData(Base):
    __tablename__ = "history_data"
    
    device_id = Column(String, primary_key=True)
    date = Column(DateTime, nullable=False)
    param_value = Column(Float, nullable=False)

class Substation(Base):
    __tablename__ = "substations"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 分站唯一标识
    system_id = Column(String(255), nullable=False, index=True)  # 系统ID，不得修改
    host_no = Column(Integer, nullable=False)  # 主机顺序号
    node_no = Column(Integer, nullable=False)  # 节点顺序号
    station_name = Column(String(255), nullable=False)  # 分站名称
    port_no = Column(Integer, nullable=False)  # 节点端口号
    area_id = Column(String(255), nullable=False)  # 空间编号
    drv_type = Column(String(50), nullable=False)  # 驱动类型
    drv_time = Column(Integer, nullable=False)  # 驱动时间，单位毫秒
    mb_addr = Column(String(255), nullable=False)  # Modbus地址
    mb_param = Column(String(255), nullable=False)  # Modbus通讯参数
    memo = Column(Text, nullable=True)  # 备注说明
    created_at = Column(TIMESTAMP, server_default=func.now())  # 创建时间
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())  # 更新时间

    def __repr__(self):
        return f"<Station(id={self.id}, station_name='{self.station_name}', system_id='{self.system_id}')>"