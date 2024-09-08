import uuid
from sqlalchemy.orm import Session
from typing import Dict

from app.schemas import HostCreate, HostUpdate, HostDelete, HostQuery
from app.schemas import NodeCreate, NodeUpdate, NodeDelete, NodeQuery
from app.schemas import SubstationCreate, SubstationUpdate, SubstationDelete, SubstationQuery
from app.schemas import EquipmentStatusRequest, StationHistoryRequest, StationHistoryResponse, ErrorResponse
from app.schemas import NodeActionRequest, NodeActionResponse, NodeStatusRequest, NodeStatusResponse, NodeHistoryRequest, NodeHistoryResponse
from app import crud

# 模拟生成虚拟主机 EUI 的函数
def generate_virtual_host_eui() -> str:
    return "VIRTUAL_" + str(uuid.uuid4())

def add_host_service(db: Session, data: HostCreate) -> Dict:
    try:
        # 处理虚拟主机逻辑
        if data.hostType == "VIRTUAL":
            data.devEUI = generate_virtual_host_eui()  # 生成虚拟主机的 devEUI
            data.hostName = None
            data.maxConnection = None
            data.location = None
            data.latitude = None
            data.longitude = None
            data.userName = None
            data.phoneNum = None
        
        # 调用 CRUD 操作
        return crud.add_host(db, data)
    
    except Exception as e:
        return {
            "what": "ADD_HOST",
            "code": "3",
            "errNo": "1001",
            "errMsg": str(e)
        }
        
def modify_host_service(db: Session, data: HostUpdate) -> Dict:
    return crud.modify_host(db, data)

def delete_host_service(db: Session, data: HostDelete) -> Dict:
    return crud.delete_host(db, data)

def query_host_service(db: Session, data: HostQuery) -> Dict:
    return crud.query_host(db, data)

def add_node_service(db: Session, data: NodeCreate) -> Dict:
    # 验证节点数量
    if data.number <= 0:
        return {
            "what": "ADD_NODE",
            "code": "3",
            "errNo": "400",
            "errMsg": "Node number must be greater than zero"
        }
    
    # 调用 CRUD 层操作
    return crud.add_node(db, data)

def modify_node_service(db: Session, data: NodeUpdate) -> Dict:
    return crud.modify_node(db, data)

def delete_node_service(db: Session, data: NodeDelete) -> Dict:
    return crud.delete_node(db, data)

def query_node_service(db: Session, data: NodeQuery) -> Dict:
    return crud.query_node(db, data)

def add_substation_service(db: Session, data: SubstationCreate) -> Dict:
    return crud.add_substation(db, data)

def modify_substation_service(db: Session, data: SubstationUpdate) -> Dict:
    return crud.modify_substation(db, data)

def delete_substation_service(db: Session, data: SubstationDelete) -> Dict:
    return crud.delete_substation(db, data)

def query_substation_service(db: Session, data: SubstationQuery) -> Dict:
    return crud.query_substation(db, data)

def set_equipment_status(db: Session, request: EquipmentStatusRequest):
    stations = []
    for station in request.station:
        updated_station = crud.update_equipment_status(db, station.stationID, request.runMode)
        if updated_station:
            stations.append({"stationID": updated_station.stationID, "status": updated_station.status})
        else:
            return {"what": "SET_EQUIP", "code": "3", "errNo": "1", "errMsg": f"设置设备 {station.stationID} 开关状态失败"}
    return {"what": "SET_EQUIP", "code": "0", "number": request.number, "station": stations}

def query_equipment_status(db: Session, request: EquipmentStatusRequest):
    stations = []
    for station in request.station:
        queried_station = crud.get_equipment_status(db, station.stationID)
        if queried_station:
            stations.append({"stationID": queried_station.stationID, "status": queried_station.status})
        else:
            return {"what": "QRY_EQUIP", "code": "3", "errNo": "1", "errMsg": f"查询设备 {station.stationID} 开关状态失败"}
    return {"what": "QRY_EQUIP", "code": "0", "number": request.number, "station": stations}

def query_station_history(db: Session, request: StationHistoryRequest):
    try:
        # 检查设备是否存在
        devices = crud.get_station_devices(db, request.systemID, request.areaID, request.devType, request.stationID)
        if not devices:
            return StationHistoryResponse(
                what="QRY_HISTSTATION",
                code="3",
                errNo="ERR001",
                errMsg="未找到符合条件的设备"
            )
        
        # 根据查询模式获取历史数据
        data = crud.get_station_history_data(db, devices, request.qureyMode, request.beginDay, request.endDay)
        
        if not data:
            return StationHistoryResponse(
                what="QRY_HISTSTATION",
                code="3",
                errNo="ERR002",
                errMsg="未找到历史数据"
            )
        
        # 处理历史数据
        processed_data = [
            {"param": [{"param": param_value} for param_value in params]}
            for params in data
        ]
        
        return StationHistoryResponse(
            what="QRY_HISTSTATION",
            code="0",
            paramNum=len(processed_data[0]['param']) if processed_data else 0,
            quantity=len(processed_data),
            data=processed_data
        )
    except Exception as e:
        return ErrorResponse(
            what="QRY_HISTSTATION",
            code="3",
            errNo="ERR003",
            errMsg=f"查询历史数据失败: {str(e)}"
        )


def activate_node(db: Session, request: NodeActionRequest):
    try:
        # 查找节点
        node = crud.get_node_by_id(db, request.nodeID)
        if not node:
            return NodeActionResponse(
                what="ACTIVATE_NODE",
                code="3",
                errNo="ERR001",
                errMsg="节点未找到"
            )
        
        # 激活或禁止节点
        node.status = "ACTIVE" if request.action == "ACTIVATE" else "DISABLED"
        db.commit()
        db.refresh(node)
        
        return NodeActionResponse(
            what="ACTIVATE_NODE",
            code="0",
            nodeID=node.node_id,
            action=node.status
        )
    except Exception as e:
        return ErrorResponse(
            what="ACTIVATE_NODE",
            code="3",
            errNo="ERR002",
            errMsg=f"激活节点失败: {str(e)}"
        )


def sleep_node(db: Session, request: NodeActionRequest):
    try:
        # 查找节点
        node = crud.get_node_by_id(db, request.nodeID)
        if not node:
            return NodeActionResponse(
                what="SLEEP_NODE",
                code="3",
                errNo="ERR001",
                errMsg="节点未找到"
            )
        
        # 休眠或唤醒节点
        node.status = "SLEEP" if request.action == "SLEEP" else "AWAKE"
        db.commit()
        db.refresh(node)
        
        return NodeActionResponse(
            what="SLEEP_NODE",
            code="0",
            nodeID=node.node_id,
            action=node.status
        )
    except Exception as e:
        return ErrorResponse(
            what="SLEEP_NODE",
            code="3",
            errNo="ERR002",
            errMsg=f"休眠节点失败: {str(e)}"
        )

def query_node_status(db: Session, request: NodeStatusRequest):
    try:
        # 查找节点
        node = crud.get_node_by_id(db, request.nodeID)
        if not node:
            return NodeStatusResponse(
                what="QRY_NODE_STATUS",
                code="3",
                errNo="ERR001",
                errMsg="节点未找到"
            )
        
        # 返回节点状态
        return NodeStatusResponse(
            what="QRY_NODE_STATUS",
            code="0",
            nodeID=node.node_id,
            status=node.status
        )
    except Exception as e:
        return ErrorResponse(
            what="QRY_NODE_STATUS",
            code="3",
            errNo="ERR002",
            errMsg=f"查询节点状态失败: {str(e)}"
        )

def query_node_history(db: Session, request: NodeHistoryRequest):
    try:
        # 查找节点历史数据
        history = crud.get_node_history_data(db, request.nodeID, request.beginDay, request.endDay)
        if not history:
            return NodeHistoryResponse(
                what="QRY_NODE_HISTORY",
                code="3",
                errNo="ERR001",
                errMsg="未找到历史数据"
            )

        # 处理历史数据
        processed_data = [
            {"param": [{"param": param_value} for param_value in params]}
            for params in history
        ]
        
        return NodeHistoryResponse(
            what="QRY_NODE_HISTORY",
            code="0",
            paramNum=len(processed_data[0]['param']) if processed_data else 0,
            quantity=len(processed_data),
            data=processed_data
        )
    except Exception as e:
        return ErrorResponse(
            what="QRY_NODE_HISTORY",
            code="3",
            errNo="ERR002",
            errMsg=f"查询节点历史数据失败: {str(e)}"
        )
