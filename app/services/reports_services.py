from sqlalchemy.orm import Session
from app.crud import get_reports
from app.schemas import ReportListRequest, ReportListResponse, Report

def query_report_list(db: Session, request: ReportListRequest) -> ReportListResponse:
    reports = get_reports(
        db, 
        user_id=request.userID, 
        start_date=request.startDate, 
        end_date=request.endDate
    )
    
    if reports:
        report_list = [
            Report(
                reportID=report.id,
                reportName=report.name,
                createdDate=report.created_date
            ) for report in reports
        ]
        return ReportListResponse(what="GET_REPORTLIST", code="0", reports=report_list)
    else:
        return ReportListResponse(what="GET_REPORTLIST", code="3", errNo="2", errMsg="查询失败")
