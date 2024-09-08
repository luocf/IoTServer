from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import AreaQueryRequest, AreaAddRequest, AreaUpdateRequest, AreaDeleteRequest
from app.services.area_service import AreaService
from app.db import get_db

router = APIRouter()

@router.post("/query")
def query_areas(request: AreaQueryRequest, db: Session = Depends(get_db)):
    try:
        areas, count = AreaService.get_areas(db, request.systemID, request.first, request.number)
        return {
            "what": "QRY_AREA",
            "code": "0",
            "first": request.first,
            "number": len(areas),  # 返回的记录个数
            "area": areas,
            "count": count  # 总记录个数
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={"what": "QRY_AREA", "code": "3", "errNo": "1001", "errMsg": str(e)})
    
@router.post("/add")
def add_areas(request: AreaAddRequest, db: Session = Depends(get_db)):
    try:
        AreaService.add_areas(db, request.systemID, request.area)
        return {"what": "ADD_AREA", "code": "OK"}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"what": "ADD_AREA", "code": "3", "errNo": "1002", "errMsg": str(e)})

@router.post("/update")
def update_areas(request: AreaUpdateRequest, db: Session = Depends(get_db)):
    try:
        AreaService.update_areas(db, request.area)
        return {"what": "MDF_AREA", "code": "OK"}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"what": "MDF_AREA", "code": "3", "errNo": "1003", "errMsg": str(e)})

@router.post("/delete")
def delete_areas(request: AreaDeleteRequest, db: Session = Depends(get_db)):
    try:
        AreaService.delete_areas(db, [area.areaID for area in request.area])
        return {"what": "DEL_AREA", "code": "OK"}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"what": "DEL_AREA", "code": "3", "errNo": "1004", "errMsg": str(e)})
