from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import HostCreate, HostUpdate, HostDelete, HostQuery
from app.schemas import NodeCreate, NodeUpdate, NodeDelete, NodeQuery
from app.schemas import SubstationCreate, SubstationUpdate, SubstationDelete, SubstationQuery
from app.schemas import (EquipmentStatusRequest, EquipmentStatusResponse, 
                         SubstationDelete, SubstationQuery, 
                         StationHistoryRequest, StationHistoryResponse,
                         NodeActionResponse, NodeActionRequest, 
                         NodeStatusResponse, NodeStatusRequest,
                         NodeHistoryResponse, NodeHistoryRequest)
from app.services import devices_service
from app.db import get_db


router = APIRouter()

#4.1.1 添加主机
@router.post("/host/add")
async def add_host(data: HostCreate, db: Session = Depends(get_db)):
    result = devices_service.add_host_service(db, data)
    if result["code"] != "0":
        raise HTTPException(status_code=400, detail={
                "what": result.get("what"),
                "code": result.get("code", "3"),
                "errNo": result.get("errNo", "UnknownError"),
                "errMsg": result.get("errMsg", "Unknown error")
            })
    return result

#4.1.2 修改主机
@router.post("/host/modify")
async def modify_host(data: HostUpdate, db: Session = Depends(get_db)):
    result = devices_service.modify_host_service(db, data)
    if result["code"] != "0":
        raise HTTPException(status_code=400, detail={
                "what": result.get("what"),
                "code": result.get("code", "3"),
                "errNo": result.get("errNo", "UnknownError"),
                "errMsg": result.get("errMsg", "Unknown error")
            })
    return result

#4.1.3 删除主机
@router.post("/host/delete")
async def delete_host(data: HostDelete, db: Session = Depends(get_db)):
    result = devices_service.delete_host_service(db, db, data)
    if result["code"] != "0":
        raise HTTPException(
            status_code=400,
            detail={
                "what": result.get("what"),
                "code": result.get("code", "3"),
                "errNo": result.get("errNo", "UnknownError"),
                "errMsg": result.get("errMsg", "Unknown error")
            }
        )

#4.1.4 查询主机
@router.post("/host/query")
async def query_host(data: HostQuery, db: Session = Depends(get_db)):
    result = devices_service.query_host_service(db, data)
    if result["code"] != "0":
        raise HTTPException(status_code=400, detail={
            "what": result.get("what", "QRY_HOST"),
            "code": result.get("code", "3"),
            "errNo": result.get("errNo", "UnknownError"),
            "errMsg": result.get("errMsg", "Unknown error")
        })
    return result

#4.2.1 添加节点
@router.post("/node/add")
async def add_node(data: NodeCreate, db: Session = Depends(get_db)):
    try:
        result = devices_service.add_node_service(db, data)
        if result["code"] != "0":
            raise HTTPException(status_code=400, detail={
                    "what": result.get("what"),
                    "code": result.get("code", "3"),
                    "errNo": result.get("errNo", "UnknownError"),
                    "errMsg": result.get("errMsg", "Unknown error")
                })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
#4.2.2 修改节点
@router.post("/node/modify")
async def modify_node(data: NodeUpdate, db: Session = Depends(get_db)):
    result = devices_service.modify_node_service(db, data)
    if result["code"] != "0":
        raise HTTPException(status_code=400, detail={
                "what": result.get("what"),
                "code": result.get("code", "3"),
                "errNo": result.get("errNo", "UnknownError"),
                "errMsg": result.get("errMsg", "Unknown error")
            })
    return result

#4.2.3 删除节点
@router.post("/node/delete")
async def delete_node(data: NodeDelete, db: Session = Depends(get_db)):
    result = devices_service.delete_node_service(db, data)
    if result["code"] != "0":
        raise HTTPException(status_code=400, detail={
                "what": result.get("what"),
                "code": result.get("code", "3"),
                "errNo": result.get("errNo", "UnknownError"),
                "errMsg": result.get("errMsg", "Unknown error")
            })
    return result

#4.2.4 查询节点
@router.post("/node/query")
async def query_node(data: NodeQuery, db: Session = Depends(get_db)):
    result = devices_service.query_node_service(db, data)
    if result["code"] != "0":
        raise HTTPException(status_code=400, detail={
                "what": result.get("what"),
                "code": result.get("code", "3"),
                "errNo": result.get("errNo", "UnknownError"),
                "errMsg": result.get("errMsg", "Unknown error")
            })
    return result

#4.3.1 添加分站
@router.post("/substation/add")
async def add_substation(data: SubstationCreate, db: Session = Depends(get_db)):
    result = devices_service.add_substation_service(db, data)
    if result["code"] != "0":
        raise HTTPException(status_code=400, detail={
                "what": result.get("what"),
                "code": result.get("code", "3"),
                "errNo": result.get("errNo", "UnknownError"),
                "errMsg": result.get("errMsg", "Unknown error")
            })
    return result

#4.3.2 修改分站
@router.post("/substation/modify")
async def modify_substation(data: SubstationUpdate, db: Session = Depends(get_db)):
    result = devices_service.modify_substation_service(db, data)
    if result["code"] != "0":
        raise HTTPException(status_code=400, detail={
                "what": result.get("what"),
                "code": result.get("code", "3"),
                "errNo": result.get("errNo", "UnknownError"),
                "errMsg": result.get("errMsg", "Unknown error")
            })
    return result

#4.3.3 删除分站
@router.post("/substation/delete")
async def delete_substation(data: SubstationDelete, db: Session = Depends(get_db)):
    result = devices_service.delete_substation_service(db, data)
    if result["code"] != "0":
        raise HTTPException(status_code=400, detail={
                "what": result.get("what"),
                "code": result.get("code", "3"),
                "errNo": result.get("errNo", "UnknownError"),
                "errMsg": result.get("errMsg", "Unknown error")
            })
    return result

#4.3.2 查询分站
@router.post("/substation/query")
async def query_substation(data: SubstationQuery, db: Session = Depends(get_db)):
    result = devices_service.query_substation_service(db, data)
    if result["code"] != "0":
        raise HTTPException(status_code=400, detail={
                "what": result.get("what"),
                "code": result.get("code", "3"),
                "errNo": result.get("errNo", "UnknownError"),
                "errMsg": result.get("errMsg", "Unknown error")
            })
    return result

#6.2.1 设置分站设备开关状态
@router.post("/set_status", response_model=EquipmentStatusResponse)
def set_equipment_status(request: EquipmentStatusRequest, db: Session = Depends(get_db)):
    return devices_service.set_equipment_status(db, request)

#6.2.2 查询分站设备开关状态
@router.post("/query_status", response_model=EquipmentStatusResponse)
def query_equipment_status(request: EquipmentStatusRequest, db: Session = Depends(get_db)):
    return devices_service.query_equipment_status(db, request)

#6.2.3 查询分站设备历史数据
@router.post("/query_station_history", response_model=StationHistoryResponse)
def query_station_history(request: StationHistoryRequest, db: Session = Depends(get_db)):
    return devices_service.query_station_history(db, request)

#6.3.1 节点激活/禁止
@router.post("/activate_node", response_model=NodeActionResponse)
def activate_node(request: NodeActionRequest, db: Session = Depends(get_db)):
    return devices_service.activate_node(db, request)

#6.3.2 节点休眠/唤醒
@router.post("/sleep_node", response_model=NodeActionResponse)
def sleep_node(request: NodeActionRequest, db: Session = Depends(get_db)):
    return devices_service.sleep_node(db, request)

#6.3.3 查询节点状态
@router.post("/query_node_status", response_model=NodeStatusResponse)
def query_node_status(request: NodeStatusRequest, db: Session = Depends(get_db)):
    return devices_service.query_node_status(db, request)

#6.3.4 查询节点历史数据
@router.post("/query_node_history", response_model=NodeHistoryResponse)
def query_node_history(request: NodeHistoryRequest, db: Session = Depends(get_db)):
    return devices_service.query_node_history(db, request)