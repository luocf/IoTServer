from sqlalchemy.orm import Session
from app.models import Area
from typing import List, Dict, Any
from app import crud

class AreaService:
    @staticmethod
    def get_areas(db: Session, system_id: str, first: int, number: int) -> List[Dict[str, Any]]:
        areas = crud.get_areas(db, system_id, first, number)
        return [{
            "areaID": area.area_id,
            "areaName": area.area_name,
            "areaLocation": area.area_location,
            "areaValue": area.area_value,
            "areaHight": area.area_height,
            "memo": area.memo
        } for area in areas]

    @staticmethod
    def get_areas(db: Session, system_id: str, first: int, number: int) -> tuple[List[Dict[str, Any]], int]:
        areas = crud.get_areas(db, system_id, first, number)
        return [{
            "areaID": area.area_id,
            "areaName": area.area_name,
            "areaLocation": area.area_location,
            "areaValue": area.area_value,
            "areaHight": area.area_height,
            "memo": area.memo
        } for area in areas], len(areas)
        
    @staticmethod
    def add_areas(db: Session, system_id: str, area_data: List[Dict[str, Any]]):
        for area in area_data:
            # 创建一个新的 Area 对象
            new_area = Area(
                system_id=system_id,
                area_name=area["areaName"],  # areaID 是新增时为 0，数据库会自动生成
                area_location=area["areaLocation"],
                area_value=area["areaValue"],
                area_height=area["areaHight"],
                memo=area.get("memo", "")  # 备注是可选的
            )
            # 调用 CRUD 操作来添加区域
            crud.add_area(db, new_area)
        
        try:
            # 提交数据库事务
            db.commit()
        except Exception as e:
            # 如果失败，回滚事务
            db.rollback()
            raise Exception("空间添加失败: " + str(e))
        
    @staticmethod
    def update_areas(db: Session, area_data: List[Dict[str, Any]]):
        for area in area_data:
            existing_area = crud.get_area_by_id(db, area["areaID"])
            if existing_area:
                existing_area.area_name = area["areaName"]
                existing_area.area_location = area["areaLocation"]
                existing_area.area_value = area["areaValue"]
                existing_area.area_height = area["areaHight"]
                existing_area.memo = area.get("memo", "")
            else:
                raise Exception(f"空间ID {area['areaID']} 不存在")
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise Exception("空间修改失败: " + str(e))

    @staticmethod
    def delete_areas(db: Session, area_ids: List[str]):
        for area_id in area_ids:
            area = crud.get_area_by_id(db, area_id)
            if area:
                crud.delete_area(db, area)
            else:
                raise Exception(f"空间ID {area_id} 不存在")
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise Exception("空间删除失败: " + str(e))