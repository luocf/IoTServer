from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.tasks_services import (add_task, modify_task, remove_task, 
                                         query_task,set_task_run_mode, 
                                         query_task_run_mode,
                                         query_task_history, query_all_task_run_modes)
from app.schemas import (TaskCreate, TaskUpdate, TaskDelete, TaskQuery, 
                         TaskResponse, TaskRunModeRequest, TaskRunModeResponse,
                         TaskHistoryRequest, TaskHistoryResponse,SystemTaskRunModeResponse, SystemTaskRunModeRequest)
from app.db import get_db
from .. import schemas, services

router = APIRouter()

#5.1.1 新增任务
@router.post("/task/add", response_model=TaskResponse)
def add_task_endpoint(task: TaskCreate, db: Session = Depends(get_db)):
    try:
        new_task = add_task(db, task)
        return TaskResponse(
            what="ADD_TASK",
            code="0",
            taskID=new_task.task_id,  # 任务顺序号
            taskName=new_task.task_name  # 任务名称
        )
    except Exception as e:
        return TaskResponse(
            what="ADD_TASK",
            code="3",
            errNo="ERR001",  #TODO 根据实际错误情况设置
            errMsg=f"任务创建失败: {str(e)}"
        )
#5.1.2 修改任务
@router.post("/task/update", response_model=TaskResponse)
def update_task_endpoint(task: TaskUpdate, db: Session = Depends(get_db)):
    try:
        updated_task = modify_task(db, task)
        if updated_task:
            return TaskResponse(
                what="MDF_TASK",
                code="0",
                taskID=updated_task.task_id,  # 使用下划线命名
                taskName=updated_task.task_name
            )
        else:
            raise HTTPException(status_code=404, detail="任务未找到")
    except Exception as e:
        return TaskResponse(
            what="MDF_TASK",
            code="3",
            errNo="ERR001",  # 根据实际情况设置错误号
            errMsg=f"任务修改失败: {str(e)}"
        )
#5.1.3 删除任务
@router.post("/task/delete", response_model=TaskResponse)
def delete_task_endpoint(task: TaskDelete, db: Session = Depends(get_db)):
    try:
        deleted_task = remove_task(db, task)
        if deleted_task:
            return TaskResponse(
                what="DEL_TASK",
                code="0",
                taskID=deleted_task.task_id,
                taskName=deleted_task.task_name
            )
        else:
            raise HTTPException(status_code=404, detail="任务未找到")
    except Exception as e:
        return TaskResponse(
            what="DEL_TASK",
            code="3",
            errNo="ERR001",  # 根据实际情况设置错误号
            errMsg=f"任务删除失败: {str(e)}"
        )
        
#5.1.4 查询任务
@router.post("/task/query", response_model=TaskResponse)
def query_task_endpoint(task: TaskQuery, db: Session = Depends(get_db)):
    try:
        tasks = query_task(db, task)
        if tasks:
            return TaskResponse(
                what="SEL_TASK",
                code="0",
                number=len(tasks),
                tasks=tasks
            )
        else:
            return TaskResponse(
                what="SEL_TASK",
                code="3",
                errNo="ERR002",  # 根据实际情况设置错误号
                errMsg="任务未找到"
            )
    except Exception as e:
        return TaskResponse(
            what="SEL_TASK",
            code="3",
            errNo="ERR003",  # 根据实际情况设置错误号
            errMsg=f"任务查询失败: {str(e)}"
        )

#6.1.1 设置任务运行模式
@router.post("/set_mode", response_model=TaskRunModeResponse)
def set_task_run_mode(request: TaskRunModeRequest, db: Session = Depends(get_db)):
    return set_task_run_mode(db, request)

#6.1.2 查询任务运行模式
@router.post("/query_mode", response_model=TaskRunModeResponse)
def query_task_run_mode(request: TaskRunModeRequest, db: Session = Depends(get_db)):
    return query_task_run_mode(db, request)

@router.post("/query_history")
def query_task_history(request: TaskHistoryRequest, db: Session = Depends(get_db)):
    return query_task_history(db, request)

#6.1.3 查询系统下所有任务运行模式
@router.post("/query_systasks", response_model=SystemTaskRunModeResponse)
def query_system_tasks(request: SystemTaskRunModeRequest, db: Session = Depends(get_db)):
    return query_all_task_run_modes(db, request)