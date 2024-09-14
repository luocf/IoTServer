from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime

from app.schemas import SystemCreate, SystemUpdate, SystemListResponse, SuperAdminLoginRequest, UploadBackgroundImageResponse, CheckSystemAvailabilityRequest

from app.services.superadmin_service import (
    verify_superadmin_credentials,
    handle_sms_verification,
    handle_superadmin_login,
    get_system_by_name,
    create_new_system_service,
    modify_existing_system,
    change_system_status_service,
    list_managed_systems_service,
    handle_background_image_upload,
    validate_superadmin
)

from app.utils import generate_admin_token, SECRET_KEY
from app.db import get_db


router = APIRouter()
#1.1.1 获取短信验证码
@router.get("/superadmin/get_sms_verification")
async def get_sms_verification(superID: str, superPasswd: str, needAnswer: str = 'no', db: Session = Depends(get_db)):
    # 验证超级管理员ID和密码
    admin = verify_superadmin_credentials(db, superID, superPasswd)
    if not admin:
        return JSONResponse(status_code=400, content={"what": "GET_SUPERVERIFY", "code": "3", "errNo": "1", "errMsg": "获取验证码失败"})
    
    # 发送短信验证码(TODO 对接短信服务)
    success = handle_sms_verification(superID)
    if not success:
        return {"what": "GET_SUPERVERIFY", "code": "3", "errNo": "1", "errMsg": "获取验证码失败"}
    
    response = {"what": "GET_SUPERVERIFY", "code": "0", "message": "验证码已发送成功"}
    
    if needAnswer.lower() != 'yes':
        response.pop("message")
    
    return response

#1.1.2 超级管理员登录
@router.post("/superadmin/login")
async def superadmin_login(request: SuperAdminLoginRequest, db: Session = Depends(get_db)):
    superID = request.superID
    superPasswd = request.superPasswd
    verifyCode = request.verifyCode
    needAnswer = request.needAnswer
    
    # 验证超级管理员凭据
    admin = verify_superadmin_credentials(db, superID, superPasswd)
    if not admin:
        # return {"what": "SET_SUPERLOGIN", "code": "3", "errNo": "3", "errMsg": "账号密码错误"}
        raise HTTPException(status_code=400, detail={"what": "SET_SUPERLOGIN", "code": "3", "errNo": "3", "errMsg": "账号密码错误"})

    # 验证短信验证码 TODO
    if not handle_superadmin_login(superID, verifyCode):
        # return {"what": "SET_SUPERLOGIN", "code": "3", "errNo": "3", "errMsg": "验证码错误"}
        raise HTTPException(status_code=400, detail={"what": "SET_SUPERLOGIN", "code": "3", "errNo": "3", "errMsg": "验证码错误"})

    return {"what": "SET_SUPERLOGIN", "code": "OK"}



#1.2.1 系统和管理管账号查重
@router.post("/superadmin/check_system_availability")
def check_system_availability(request: CheckSystemAvailabilityRequest, db: Session = Depends(get_db)):
    newSystem = request.newSystem
    adminID = request.adminID
    
    existing_system = get_system_by_name(db, newSystem)
    
    if existing_system:
        if existing_system.admin_id == adminID:
            return {"what": "QRY_SUPERSYSTEM", "code": "3", "errNo": "4", "errMsg": "此注册名已被用"}
        else:
            return {"what": "QRY_SUPERSYSTEM", "code": "3", "errNo": "2", "errMsg": "此系统名已被用"}
    
    return {"what": "QRY_SUPERSYSTEM", "code": "0", "systemID": "available"}

#1.2.2 新建系统
@router.post("/superadmin/create_system")
def create_new_system(system: SystemCreate, db: Session = Depends(get_db)):
    db_system = create_new_system_service(db, system)
    if not db_system:
        return {"what": "SET_SUPERNEW", "code": "3", "errNo": "5", "errMsg": "操作失败"}
    print(f"create_system systemID: {system.systemID}")

    # 假设有一个函数生成 token
    admin_token = generate_admin_token(db_system.admin_id)
    
    print(f"create_system admin_token: {admin_token}")

    return {
        "what": "SET_SUPERNEW",
        "code": "0",
        # "token": admin_token
        "token": "adminToken" #TODO mock token
    }
    
#1.2.3 修改系统
@router.post("/superadmin/modify_system")
def modify_system(system: SystemUpdate, db: Session = Depends(get_db)):
    # 调用修改系统的服务函数
    db_system = modify_existing_system(db, system)
    if not db_system:
        return {"what": "SET_SUPERMODIFY", "code": "3", "errNo": "5", "errMsg": "操作失败"}

    # 生成并返回实际的 token
    token = generate_admin_token(system.adminID)
    return {"what": "SET_SUPERMODIFY", "code": "0", "token": token}

#1.2.4 上传背景图片
@router.post("/superadmin/upload_background_image/", response_model=UploadBackgroundImageResponse)
async def upload_background_image(systemID: str, pngFile: UploadFile = File(...), db: Session = Depends(get_db)):
    file_content = await pngFile.read()
    print(f"Received systemID: {systemID}, pngFile name: {pngFile.filename}")

    file_token, error_msg = handle_background_image_upload(db, systemID, file_content, pngFile.filename)
    
    # 打印调试信息
    print(f"file_token: {file_token}, error_msg: {error_msg}")

    if error_msg:
        return {"what": "SET_SUPERPNGFILE", "code": "3", "errNo": "6", "errMsg": error_msg}

    return {"what": "SET_SUPERPNGFILE", "code": "0", "fileToken": file_token}

#1.2.5 管理系统
@router.post("/superadmin/manage_system")
def manage_system(systemID: str, manage: str, db: Session = Depends(get_db)):
    # 检查 manage 参数是否有效
    if manage not in ["disable", "enable"]:
        return {"what": "SET_SUPERMANAGE", "code": "3", "errNo": "5", "errMsg": "无效的操作类型"}

    # 将 manage 参数转换为布尔值
    status = True if manage == "enable" else False
    
    # 调用服务层函数更改系统状态
    try:
        db_system = change_system_status_service(db, systemID, status)
        if not db_system:
            return {"what": "SET_SUPERMANAGE", "code": "3", "errNo": "5", "errMsg": "操作失败"}
    except Exception as e:
        return {"what": "SET_SUPERMANAGE", "code": "3", "errNo": "5", "errMsg": str(e)}

    # 返回成功响应
    return {"what": "SET_SUPERMANAGE", "code": "OK"}

#1.2.6 管理系统列表
@router.get("/superadmin/list_systems", response_model=SystemListResponse)
def list_managed_systems(superID: str, first: int = 0, number: int = 10, db: Session = Depends(get_db)):
    print(f"superID: {superID}")  # 添加调试信息
    if not validate_superadmin(db, superID):
        print("Invalid superID")  # 打印无效superID的日志
        return {
            "what": "GET_SUPERLIST",
            "code": "3",
            "errNo": "5",
            "errMsg": "无效的 superID",
            "number": 0,
            "system": []
        }

    try:
        systems = list_managed_systems_service(db, first, number)
        system_list = [
            {
                "systemID": system.system_id,
                "systemName": system.system_name,
                "adminID": system.admin_id,
                "setupDate": system.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
            for system in systems
        ]

        return {"what": "GET_SUPERLIST", "code": "0", 
                "errNo": "0",  # 添加 errNo，设置为默认值
                "errMsg": "",  # 添加 errMsg，设置为空字符串
                "number": len(system_list), 
                "system": system_list}

    except Exception as e:
        print(f"Exception: {e}")  # 打印异常信息
        return {
            "what": "GET_SUPERLIST",
            "code": "3",
            "errNo": "5",
            "errMsg": "操作失败",
            "number": 0,
            "system": []
        }
