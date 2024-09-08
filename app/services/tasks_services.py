from sqlalchemy.orm import Session
from app.crud import (create_task, update_task, delete_task, get_task, get_tasks, 
                      get_tasks_by_area, get_all_task_run_modes)
from app.schemas import (TaskCreate, TaskUpdate, TaskDelete, TaskQuery, 
                         TaskRunModeRequest, TaskRunModeResponse, 
                         TaskHistoryRequest, TaskHistoryResponse,
                         SystemTaskRunModeRequest, SystemTaskRunModeResponse,
                         ErrorResponse, TaskRunMode)
from app.models import Task,TaskHistory

def add_task(db: Session, task_data: TaskCreate):
    task_dict = task_data.dict()
    return create_task(db, task_dict)

def modify_task(db: Session, task_data: TaskUpdate):
    task_dict = task_data.dict()
    task_id = task_dict.pop('taskID')
    return update_task(db, task_id, task_dict)

def remove_task(db: Session, task_data: TaskDelete):
    return delete_task(db, task_data.taskID)

def query_task(db: Session, task_data: TaskQuery):
    if task_data.taskID:
        return [get_task(db, task_data.taskID)]
    elif task_data.areaID:
        return get_tasks_by_area(db, task_data.systemID, task_data.areaID)
    else:
        return get_tasks(db, task_data.systemID)

def set_task_run_mode(db: Session, request: TaskRunModeRequest):
    try:
        # 1. 验证请求中的 taskID 是否存在
        task = db.query(Task).filter(Task.task_id == request.taskID).first()
        if not task:
            return TaskRunModeResponse(
                what="SET_TASK",
                code="3",
                errNo="ERR001",
                errMsg="任务未找到"
            )

        # 2. 更新任务的运行模式
        task.run_mode = request.runMode
        db.commit()
        db.refresh(task)

        # 3. 返回成功响应
        return TaskRunModeResponse(
            what="SET_TASK",
            code="0",
            taskID=task.task_id,
            runMode=task.run_mode
        )
    except Exception as e:
        # 4. 处理异常并返回错误响应
        return TaskRunModeResponse(
            what="SET_TASK",
            code="3",
            errNo="ERR002",
            errMsg=f"设置任务运行模式失败: {str(e)}"
        )
        
def query_task_run_mode(db: Session, request: TaskRunModeRequest):
    try:
        # 1. 验证请求中的 taskID 是否存在
        task = db.query(Task).filter(Task.task_id == request.taskID).first()
        if not task:
            return TaskRunModeResponse(
                what="QRY_TASK",
                code="3",
                errNo="ERR001",
                errMsg="任务未找到"
            )

        # 2. 返回任务的运行模式
        return TaskRunModeResponse(
            what="QRY_TASK",
            code="0",
            taskID=task.task_id,
            runMode=task.run_mode
        )
    except Exception as e:
        # 3. 处理异常并返回错误响应
        return TaskRunModeResponse(
            what="QRY_TASK",
            code="3",
            errNo="ERR002",
            errMsg=f"查询任务运行模式失败: {str(e)}"
        )
        
def query_task_history(db: Session, request: TaskHistoryRequest):
    try:
        # 1. 查询任务的历史记录
        history = db.query(TaskHistory).filter(
            TaskHistory.task_id == request.taskID,
            TaskHistory.created_at >= request.beginTime,
            TaskHistory.created_at <= request.endTime
        ).all()

        # 2. 返回任务的历史记录
        return TaskHistoryResponse(
            what="QRY_HISTORY",
            code="0",
            taskID=request.taskID,
            history=[h.dict() for h in history]
        )
    except Exception as e:
        # 3. 处理异常并返回错误响应
        return TaskHistoryResponse(
            what="QRY_HISTORY",
            code="3",
            errNo="ERR001",
            errMsg=f"查询任务历史记录失败: {str(e)}"
        )
        
def query_all_task_run_modes(db: Session, request: SystemTaskRunModeRequest):
    try:
        # 从 CRUD 层获取任务列表
        tasks = get_all_task_run_modes(db, request.systemID, request.first, request.number)
        
        if not tasks:
            return SystemTaskRunModeResponse(
                what="QRY_SYSTASK",
                code="0",
                first=request.first,
                number=0,
                tasks=[]
            )
        
        task_list = [TaskRunMode(taskID=task.task_id, runMode=task.run_mode) for task in tasks]
        
        return SystemTaskRunModeResponse(
            what="QRY_SYSTASK",
            code="0",
            first=request.first,
            number=len(task_list),
            tasks=task_list
        )
    except Exception as e:
        return ErrorResponse(
            what="QRY_SYSTASK",
            code="3",
            errNo="ERR001",
            errMsg=f"查询系统任务运行模式失败: {str(e)}"
        )