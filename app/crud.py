from sqlalchemy.orm import Session
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

from app.models import Report as ReportModel
from app.models import (SuperAdmin, System, Host, Node, HostOperationsLog, NodeOperationsLog, 
                    Area, System, User, BackgroundImage, Substation, Task,
                    HistoryData, NodeHistory)

from app.schemas import (SystemCreate, SystemUpdate, Station,
                     HostCreate, HostUpdate, HostDelete, HostQuery, NodeCreate, NodeUpdate, 
                     NodeDelete, NodeQuery, SubstationCreate, 
                     SubstationUpdate, SubstationDelete, SubstationQuery)
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_admin_by_credentials(db: Session, superID: str, superPasswd: str):
    return db.query(SuperAdmin).filter_by(super_admin_id=superID, password=superPasswd).first()

def create_new_system(db: Session, system_data: SystemCreate):
    new_system = System(
        system_id=system_data.systemID,
        system_name=system_data.newSystem,
        admin_id=system_data.adminID,
        admin_password=system_data.adminPasswd,  # 修正字段名
        admin_phone_number=system_data.adminPhoneNum,  # 修正字段名
        status="active"
    )
    
    db.add(new_system)
    try:
        db.commit()
        db.refresh(new_system)
        return new_system
    except Exception as e:
        db.rollback()
        print(f"Error committing system creation: {e}")
        return None

def update_system(db: Session, system_data: SystemUpdate):
    system = db.query(System).filter_by(system_id=system_data.systemID).first()  # 使用 system_id 而非 id
    if system:
        # 手动映射请求体的字段到数据库字段
        system.system_name = system_data.systemName
        system.admin_id = system_data.adminID
        system.admin_password = system_data.passwd
        system.admin_phone_number = system_data.phoneNum
        
        # 提交更改
        db.commit()
        db.refresh(system)
    return system


def list_systems(db: Session, first: int = 0, number: int = 10):
    query = db.query(System).offset(first)
    if number > 0:
        query = query.limit(number)
    return query.all()

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_system_by_name(db: Session, system_name: str) -> System:
    return db.query(System).filter(System.system_name == system_name).first()

def change_system_status(db: Session, system_id: str, status: bool) -> System:
    db_system = db.query(System).filter(System.system_id == system_id).first()
    if db_system:
        db_system.status = status
        db.commit()
        db.refresh(db_system)
    return db_system

def get_system_by_id(db: Session, system_id: str) -> System:
    return db.query(System).filter(System.system_id == system_id).first()

def get_superadmin_by_id(db: Session, super_id: str) -> SuperAdmin:
    return db.query(SuperAdmin).filter(SuperAdmin.super_admin_id == super_id).first()

def save_background_image(db: Session, system_id: str, file_token: str, file_path: str, file_name:str) -> BackgroundImage:
    new_image = BackgroundImage(
        id=file_token,  # 这里使用 `file_token` 作为 ID，确保唯一性
        system_id=system_id,
        file_token=file_token,
        file_path=file_path,
        original_name=file_name
    )
    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    return new_image


def add_host(db: Session, data: HostCreate) -> Dict:
    host = Host(
        system_id=data.systemID,
        host_no=data.hostNo,
        dev_eui=data.devEUI,
        host_type=data.hostType,
        host_name=data.hostName,
        max_connection=data.maxConnection,
        location=data.location,
        latitude=data.latitude,
        longitude=data.longitude,
        user_name=data.userName,
        phone_num=data.phoneNum,
        memo=data.memo
    )
    db.add(host)
    db.commit()
    db.refresh(host)
    
    # 记录操作日志
    log = HostOperationsLog(
        host_no=data.hostNo,
        operation="ADD",
        status_code="0"
    )
    db.add(log)
    db.commit()
    
    return {"what": "ADD_HOST", "code": "0", "hostNo": host.host_no, "devEUI": host.dev_eui}

def modify_host(db: Session, data: HostUpdate) -> Dict:
    host = db.query(Host).filter(Host.host_no == data.hostNo).one_or_none()
    if not host:
        return {"what": "MDF_HOST", "code": "3", "errNo": "404", "errMsg": "Host not found"}
    
    host.dev_eui = data.devEUI
    host.host_type = data.hostType
    host.host_name = data.hostName
    host.max_connection = data.maxConnection
    host.location = data.location
    host.latitude = data.latitude
    host.longitude = data.longitude
    host.user_name = data.userName
    host.phone_num = data.phoneNum
    host.memo = data.memo
    
    db.commit()
    
    # 记录操作日志
    log = HostOperationsLog(
        host_no=data.hostNo,
        operation="MODIFY",
        status_code="0"
    )
    db.add(log)
    db.commit()
    
    return {"what": "MDF_HOST", "code": "0", "hostNo": host.host_no, "devEUI": host.dev_eui}

def delete_host(db: Session, data: HostDelete) -> Dict:
    host = db.query(Host).filter(Host.host_no == data.hostNo).one_or_none()
    if not host:
        return {"what": "DEL_HOST", "code": "3", "errNo": "404", "errMsg": "Host not found"}
    
    db.delete(host)
    db.commit()
    
    # 记录操作日志
    log = HostOperationsLog(
        host_no=data.hostNo,
        operation="DELETE",
        status_code="0"
    )
    db.add(log)
    db.commit()
    
    return {"what": "DEL_HOST", "code": "0", "hostNo": host.host_no, "devEUI": host.dev_eui}

def query_host(db: Session, data: HostQuery) -> Dict:
    # 查询主机信息，使用分页
    hosts = db.query(Host).filter(Host.system_id == data.systemID).offset(data.first).limit(data.number).all()

    if not hosts:
        return {
            "what": "QRY_HOST",
            "code": "3",
            "errNo": "404",
            "errMsg": "No hosts found for the given systemID"
        }

    # 构建返回的主机信息列表
    host_list = [
        {
            "hostNo": host.host_no,
            "devEUI": host.dev_eui,
            "hostType": host.host_type,
            "hostName": host.host_name,
            "maxConnection": host.max_connection,
            "location": host.location,
            "latitude": host.latitude,
            "longitude": host.longitude,
            "userName": host.user_name,
            "phoneNum": host.phone_num,
            "memo": host.memo
        } for host in hosts
    ]

    # 返回符合接口定义的结果
    return {
        "what": "QRY_HOST",
        "code": "0",
        "number": len(host_list),  # 返回主机的数量
        "host": host_list
    }


def add_node(db: Session, data: NodeCreate) -> Dict:
    try:
        # 创建新节点
        nodes = [Node(
            system_id=data.systemID,
            host_no=data.hostNo,
            dev_eui=d["devEUI"],
            dev_name=d["devName"],
            dev_type=d["devType"],
            dev_port=d.get("devPort", 1),  # 默认端口为1
            uplink_addr=d.get("uplinkAddr"),
            uplink_param=d.get("uplinkParam"),
            downlink_addr=d.get("downlinkAddr"),
            downlink_param=d.get("downlinkParam"),
            memo=d.get("memo")
        ) for d in data.controller]
        
        db.add_all(nodes)
        db.commit()
        
        # 记录日志
        for node in nodes:
            log = NodeOperationsLog(
                node_id=node.id,
                operation="ADD",
                status_code="0"
            )
            db.add(log)
        
        db.commit()

        # 返回成功信息，包括 nodeNo 和 devEUI
        return {
            "what": "ADD_NODE",
            "code": "0",
            "number": len(nodes),
            "node": [{"nodeNo": node.id, "devEUI": node.dev_eui} for node in nodes]
        }
    
    except Exception as e:
        db.rollback()  # 出现错误时回滚
        return {
            "what": "ADD_NODE",
            "code": "3",
            "errNo": "500",
            "errMsg": "Failed to add nodes"
        }
        
def modify_node(db: Session, data: NodeUpdate) -> Dict:
    try:
        # 查找对应的节点，通过 nodeNo 来匹配
        nodes = db.query(Node).filter(Node.id.in_([d["nodeNo"] for d in data.controller])).all()
        
        if not nodes:
            return {"what": "MDF_NODE", "code": "3", "errNo": "404", "errMsg": "Nodes not found"}
        
        # 更新节点信息
        for node in nodes:
            update_data = next((item for item in data.controller if item["nodeNo"] == node.id), {})
            node.dev_name = update_data.get("devName", node.dev_name)
            node.dev_type = update_data.get("devType", node.dev_type)
            node.dev_port = update_data.get("devPort", node.dev_port)
            node.uplink_addr = update_data.get("uplinkAddr", node.uplink_addr)
            node.uplink_param = update_data.get("uplinkParam", node.uplink_param)
            node.downlink_addr = update_data.get("downlinkAddr", node.downlink_addr)
            node.downlink_param = update_data.get("downlinkParam", node.downlink_param)
            node.memo = update_data.get("memo", node.memo)
        
        # 提交更新
        db.commit()
        
        # 记录修改日志
        for node in nodes:
            log = NodeOperationsLog(
                node_id=node.id,
                operation="MODIFY",
                status_code="0"
            )
            db.add(log)
        
        db.commit()
        
        # 返回修改成功的信息，包括 nodeNo 和 devEUI
        return {
            "what": "MDF_NODE",
            "code": "0",
            "number": len(nodes),
            "node": [{"nodeNo": node.id, "devEUI": node.dev_eui} for node in nodes]
        }
    
    except Exception as e:
        db.rollback()  # 出现错误时回滚事务
        return {
            "what": "MDF_NODE",
            "code": "3",
            "errNo": "500",
            "errMsg": "Failed to modify nodes"
        }
        
def delete_node(db: Session, data: NodeDelete) -> Dict:
    try:
        # 使用 nodeNo 而不是 devEUI 来查询节点
        node_nos = [d["nodeNo"] for d in data.controller]
        nodes = db.query(Node).filter(Node.id.in_(node_nos)).all()
        
        if not nodes:
            return {"what": "DEL_NODE", "code": "3", "errNo": "404", "errMsg": "Nodes not found"}
        
        # 删除节点
        for node in nodes:
            db.delete(node)
        
        # 提交事务
        db.commit()
        
        # 记录删除操作日志
        for node in nodes:
            log = NodeOperationsLog(
                node_id=node.id,
                operation="DELETE",
                status_code="0"
            )
            db.add(log)
        
        db.commit()
        
        # 返回删除成功的信息，包括 nodeNo 和 devEUI
        return {
            "what": "DEL_NODE",
            "code": "0",
            "number": len(nodes),
            "node": [{"nodeNo": node.id, "devEUI": node.dev_eui} for node in nodes]
        }
    
    except Exception as e:
        db.rollback()  # 出现错误时回滚事务
        return {
            "what": "DEL_NODE",
            "code": "3",
            "errNo": "500",
            "errMsg": "Failed to delete nodes"
        }
        
def query_node(db: Session, data: NodeQuery) -> Dict:
    # 查询条件：根据 systemID 和 hostNo 筛选节点
    query = db.query(Node).filter(Node.system_id == data.systemID, Node.host_no == data.hostNo)

    # 如果 `number` 为 0，返回所有节点，否则分页返回
    if data.number > 0:
        query = query.offset(data.first).limit(data.number)
    
    nodes = query.all()

    # 如果没有查询到节点，返回错误信息
    if not nodes:
        return {
            "what": "QRY_NODE",
            "code": "3",
            "errNo": "404",
            "errMsg": "No nodes found"
        }

    # 返回成功信息和节点详情
    return {
        "what": "QRY_NODE",
        "code": "0",
        "number": len(nodes),
        "controller": [
            {
                "devEUI": node.dev_eui,
                "devName": node.dev_name,
                "devType": node.dev_type,
                "devPort": node.dev_port,
                "uplinkAddr": node.uplink_addr,
                "uplinkParam": node.uplink_param,
                "downlinkAddr": node.downlink_addr,
                "downlinkParam": node.downlink_param,
                "memo": node.memo
            } for node in nodes
        ]
    }

def add_substation(db: Session, data: SubstationCreate) -> Dict:
    #检查分站数量是否为正数
    if data.number <= 0:
        return {
            "what": "ADD_STATION",
            "code": "3",
            "errNo": "400",
            "errMsg": "Number of substations must be greater than 0"
        }

    stations = []
    for i in range(data.number):
        # 从 controller 中获取对应的分站数据
        controller_data = data.controller[i]
        
        substation = Substation(
            system_id=data.systemID,
            host_no=data.hostNo,
            node_no=data.nodeNo,
            substation_name=controller_data["stationName"],
            port_no=controller_data["portNo"],
            area_id=controller_data["areaID"],
            drv_type=controller_data["drvType"],
            drv_time=controller_data["drvTime"],
            mb_addr=controller_data["mbAddr"],
            mb_param=controller_data["mbParam"],
            memo=controller_data.get("memo", "")
        )
        db.add(substation)
        stations.append(substation)

    db.commit()
    
    # 将所有添加的分站刷新并返回
    return {
        "what": "ADD_STATION",
        "code": "0",
        "number": len(stations),
        "node": [
            {
                "stationID": station.id,   # 假设 stationID 对应分站的主键
                "portNo": station.port_no
            } for station in stations
        ]
    }
    
def modify_substation(db: Session, data: SubstationUpdate) -> Dict:
    if data.number <= 0:
        return {
            "what": "MDF_STATION",
            "code": "3",
            "errNo": "400",
            "errMsg": "Number of substations to modify must be greater than 0"
        }
    
    updated_stations = []
    for i in range(data.number):
        # 获取 controller 中的分站数据
        controller_data = data.controller[i]

        substation = db.query(Substation).filter(Substation.id == controller_data["stationID"]).one_or_none()
        if not substation:
            return {"what": "MDF_STATION", "code": "3", "errNo": "404", "errMsg": f"Substation {controller_data['stationID']} not found"}

        # 更新分站信息
        substation.substation_name = controller_data["stationName"]
        substation.port_no = controller_data["portNo"]
        substation.area_id = controller_data["areaID"]
        substation.drv_type = controller_data["drvType"]
        substation.drv_time = controller_data["drvTime"]
        substation.mb_addr = controller_data["mbAddr"]
        substation.mb_param = controller_data["mbParam"]
        substation.memo = controller_data.get("memo", "")
        
        updated_stations.append(substation)

    db.commit()
    
    return {
        "what": "MDF_STATION",
        "code": "0",
        "number": len(updated_stations),
        "node": [
            {
                "stationID": station.id,    # 假设 stationID 对应分站的主键
                "portNo": station.port_no
            } for station in updated_stations
        ]
    }
    
def delete_substation(db: Session, data: SubstationDelete) -> Dict:
    # 批量查询所有要删除的分站
    substations = db.query(Substation).filter(Substation.substation_no.in_([controller.stationID for controller in data.controller])).all()

    if not substations:
        return {"what": "DEL_STATION", "code": "3", "errNo": "404", "errMsg": "Substations not found"}
    
    # 删除分站
    deleted_stations = []
    try:
        for substation in substations:
            db.delete(substation)
            deleted_stations.append({
                "stationID": substation.substation_no,
                "portNo": substation.port_no,
            })
        db.commit()
    except Exception as e:
        db.rollback()  # 回滚事务
        return {"what": "DEL_STATION", "code": "3", "errNo": "500", "errMsg": str(e)}

    return {
        "what": "DEL_STATION",
        "code": "0",
        "number": len(deleted_stations),
        "node": deleted_stations
    }

def query_substation(db: Session, data: SubstationQuery) -> Dict:
    # 构建查询条件
    query = db.query(Substation).filter(Substation.system_id == data.systemID)

    # 根据 hostNo, nodeNo, areaID 进一步过滤
    if data.hostNo is not None:
        query = query.filter(Substation.host_no == data.hostNo)
    if data.nodeNo is not None:
        query = query.filter(Substation.node_no == data.nodeNo)
    if data.areaID is not None:
        query = query.filter(Substation.area_id == data.areaID)

    # 分页
    substations = query.offset(data.first).limit(data.number).all()

    # 如果没有查询到分站，返回错误信息
    if not substations:
        return {"what": "QRY_STATION", "code": "3", "errNo": "404", "errMsg": "No substation found"}

    # 构造返回结果
    return {
        "what": "QRY_STATION",
        "code": "0",
        "number": len(substations),
        "node": [
            {
                "stationID": substation.substation_no,
                "portNo": substation.port_no,
            } for substation in substations
        ]
    }

def get_areas(db: Session, system_id: str, first: int, number: int) -> List[Area]:
    query = db.query(Area).filter(Area.system_id == system_id)
    if number > 0:
        query = query.offset(first).limit(number)
    return query.all()

def add_area(db: Session, area: Area):
    db.add(area)

def get_area_by_id(db: Session, area_id: str) -> Area:
    return db.query(Area).filter(Area.area_id == area_id).first()

def delete_area(db: Session, area: Area):
    db.delete(area)
    

def create_task(db: Session, task_data: dict) -> Task:
    # 创建一个符合 Task 模型字段名称的字典
    task_data_normalized = {
        "task_id": task_data.get("taskID"),
        "system_id": task_data.get("systemID"),
        "task_name": task_data.get("taskName"),
        "task_type": task_data.get("taskType"),
        "action": task_data.get("action"),
        "act_time": task_data.get("actTime"),
        "act_on_time": task_data.get("actOnTime"),
        "number1": task_data.get("number1"),
        "setup_day": task_data.get("setupDay"),
        "repeat_mode": task_data.get("repeatMode"),
        "interval_day": task_data.get("intervalDay"),
        "act_day": task_data.get("actDay"),
        "cycle_num": task_data.get("cycleNum"),
        "concurrent": task_data.get("concurrent"),
        "area_id": task_data.get("areaID"),
        "memo": task_data.get("memo"),
    }
    db_task = Task(**task_data_normalized)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: str, task_data: dict) -> Task:
    db_task = db.query(Task).filter(Task.task_id == task_id).first()  # 使用下划线命名
    if db_task:
        for key, value in task_data.items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
        return db_task
    return None

def delete_task(db: Session, task_id: str) -> Task:
    db_task = db.query(Task).filter(Task.task_id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
        return db_task
    return None

def get_task(db: Session, task_id: str) -> Task:
    return db.query(Task).filter(Task.task_id == task_id).first()

def get_tasks(db: Session, system_id: str) -> List[Task]:
    return db.query(Task).filter(Task.system_id == system_id).all()

def get_tasks_by_area(db: Session, system_id: str, area_id: str) -> List[Task]:
    return db.query(Task).filter(Task.system_id == system_id, Task.area_id == area_id).all()

def update_task_run_mode(db: Session, taskID: str, runMode: str):
    db_task = db.query(Task).filter(Task.task_id == taskID).first()
    if db_task:
        db_task.runMode = runMode
        db.commit()
        db.refresh(db_task)
        return db_task
    return None

def get_task_run_mode(db: Session, taskID: str):
    return db.query(Task).filter(Task.task_id == taskID).first()

def get_all_tasks_run_mode(db: Session, systemID: str, first: int, number: int):
    query = db.query(Task).filter(Task.system_id == systemID)
    if number > 0:
        query = query.offset(first).limit(number)
    return query.all()

def get_task_history(db: Session, taskID: str, beginTime: str, endTime: str):
    return db.query(TaskHistory).filter(
        TaskHistory.taskID == taskID,
        TaskHistory.runTime >= beginTime,
        TaskHistory.runTime <= endTime
    ).all()


def update_equipment_status(db: Session, stationID: str, runMode: str):
    db_station = db.query(Station).filter(Station.stationID == stationID).first()
    if db_station:
        db_station.status = runMode
        db.commit()
        db.refresh(db_station)
        return db_station
    return None

def get_equipment_status(db: Session, stationID: str):
    return db.query(Station).filter(Station.stationID == stationID).first()

def get_all_equipment_status(db: Session, systemID: str, first: int, number: int):
    query = db.query(Station).filter(Station.systemID == systemID)
    if number > 0:
        query = query.offset(first).limit(number)
    return query.all()

def get_reports(db: Session, user_id: str, start_date: Optional[str] = None, end_date: Optional[str] = None):
    query = db.query(ReportModel).filter(ReportModel.user_id == user_id)
    
    if start_date:
        query = query.filter(ReportModel.created_date >= start_date)
    if end_date:
        query = query.filter(ReportModel.created_date <= end_date)
    
    return query.all()

#用户管理
def create_user(db: Session, user_id: str, phone_num: str, hashed_password: str) -> User:
    new_user = User(user_id=user_id, phone_number=phone_num, password=hashed_password)
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        raise Exception("用户注册失败: " + str(e))
    

def get_user_by_id(db: Session, user_id: str):
    return db.query(User).filter(User.user_id == user_id).first()

def get_all_task_run_modes(db: Session, system_id: str, first: int, number: int) -> List[Task]:
    query = db.query(Task).filter(Task.system_id == system_id)
    
    if number > 0:
        query = query.offset(first).limit(number)
        
    return query.all()


def get_station_devices(db: Session, systemID: str, areaID: str, devType: str, stationID: str):
    return db.query(Substation).filter(
        Substation.system_id == systemID,
        Substation.area_id == areaID,
        Substation.drv_type == devType,
        Substation.id == stationID
    ).all()


def get_week_range(start_date):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    start_of_week = start_date - timedelta(days=start_date.weekday())  # 星期一
    end_of_week = start_of_week + timedelta(days=6)  # 星期天
    return start_of_week, end_of_week

def get_month_range(start_date):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    start_of_month = start_date.replace(day=1)
    next_month = start_of_month.replace(day=28) + timedelta(days=4)  # 解决跨月问题
    end_of_month = next_month - timedelta(days=next_month.day)
    return start_of_month, end_of_month

def get_quarter_range(start_date):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    month = start_date.month
    quarter = (month - 1) // 3 + 1
    start_of_quarter = datetime(start_date.year, 3 * quarter - 2, 1)
    end_of_quarter = datetime(start_date.year, 3 * (quarter + 1) - 2, 1) - timedelta(days=1)
    return start_of_quarter, end_of_quarter

def get_year_range(start_date):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    start_of_year = datetime(start_date.year, 1, 1)
    end_of_year = datetime(start_date.year, 12, 31)
    return start_of_year, end_of_year

def get_station_history_data(db: Session, devices: List[Substation], qureyMode: str, beginDay: str, endDay: str):
    # 根据查询模式处理时间范围
    if qureyMode == "WEEK":
        begin_date, end_date = get_week_range(beginDay)
    elif qureyMode == "MONTH":
        begin_date, end_date = get_month_range(beginDay)
    elif qureyMode == "QUATER":
        begin_date, end_date = get_quarter_range(beginDay)
    elif qureyMode == "YEAR":
        begin_date, end_date = get_year_range(beginDay)
    elif qureyMode == "DAYS":
        begin_date, end_date = beginDay, endDay
    else:
        return []

    # 获取历史数据
    device_ids = [device.id for device in devices]
    return db.query(HistoryData).filter(
        HistoryData.device_id.in_(device_ids),
        HistoryData.date >= begin_date,
        HistoryData.date <= end_date
    ).all()


def get_node_by_id(db: Session, nodeID: str):
    return db.query(Node).filter(Node.node_id == nodeID).first()

def get_node_history_data(db: Session, nodeID: str, beginDay: str, endDay: str):
    return db.query(NodeHistory).filter(
        NodeHistory.node_id == nodeID,
        NodeHistory.date >= beginDay,
        NodeHistory.date <= endDay
    ).all()
