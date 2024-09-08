from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import ReportListRequest, ReportListResponse
from services.reports_services import query_report_list

router = APIRouter()

@router.get("/report/list", response_model=ReportListResponse)
def get_report_list(request: ReportListRequest):
    response = query_report_list(request)
    
    if response.code != "0":
        raise HTTPException(status_code=400, detail=response.errMsg)
    
    return response
