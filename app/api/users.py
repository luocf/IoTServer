from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import UserRegisterRequest, UserLoginRequest, UserTokenLoginRequest, UserCheckRequest, GetVerifyCodeRequest,UserLoginVerifyRequest
from app.services.user_service import UserService
from app.db import get_db

router = APIRouter()

@router.post("/register")
def user_register(request: UserRegisterRequest, db: Session = Depends(get_db)):
    try:
        token = UserService.register_user(db, request.userID, request.userName, request.userPhone, request.password, request.verifyCode)
        return {"what": "SET_REGISTER", "code": "0", "token": token}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"what": "SET_REGISTER", "code": "3", "errNo": "5", "errMsg": "注册失败，请联系客服"})


@router.post("/login")
def user_login(request: UserLoginRequest, db: Session = Depends(get_db)):
    try:
        # Step 1: 验证用户是否存在
        user = UserService.get_user_by_id(db, request.userID)
        if not user:
            return {"what": "SET_LOGINUNAME", "code": "3", "errNo": "6", "errMsg": "用户不存在"}

        # Step 2: 验证验证码 (如果需要)
        if not UserService.verify_code(user, request.verifyCode):
            return {"what": "SET_LOGINUNAME", "code": "3", "errNo": "6", "errMsg": "验证码无效"}

        # Step 3: 验证密码并生成Token
        token = UserService.login_user(user, request.password)
        return {"what": "SET_LOGINUNAME", "code": "0", "token": token}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"what": "SET_LOGINUNAME", "code": "3", "errNo": "6", "errMsg": "登录失败，请联系客服"})

@router.post("/token_login")
def user_token_login(request: UserTokenLoginRequest):
    try:
        token = UserService.token_login_user(request.userToken)
        return {"what": "SET_USERTOKEN", "code": "0", "token": token}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"what": "SET_USERTOKEN", "code": "3", "errNo": "3", "errMsg": str(e)})

@router.post("/token_login")
def user_token_login(request: UserTokenLoginRequest):
    try:
        # 验证用户的Token
        user_id = UserService.token_login_user(request.token)
        
        # 确保传入的 userID 与 token 中的 userID 匹配
        if user_id != request.userID:
            raise Exception("Token与用户ID不匹配")
        
        return {"what": "SET_LOGINTOKEN", "code": "0", "token": request.token}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"what": "SET_LOGINTOKEN", "code": "3", "errNo": "6", "errMsg": "登录失败，请联系客服"})
    
@router.post("/check_user_id")
def check_user_id(request: UserCheckRequest, db: Session = Depends(get_db)):
    user = UserService.get_user_by_id(db, request.userID)
    if user:
        raise HTTPException(status_code=400, detail={
            "what": "QRY_USERID",
            "code": "3",
            "errNo": "4",
            "errMsg": "此注册名已被用"
        })
    return {"what": "QRY_USERID", "code": "OK"}

#注册时的验证码获取
@router.post("/get_verify_code")
def get_verify_code(request: GetVerifyCodeRequest, db: Session = Depends(get_db)):
    try:
        UserService.send_verification_code(db, request.userID, request.userName, request.userPhone, request.password)
        return {"what": "GET_REGVRIFYCODE", "code": "OK"}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"what": "GET_REGVRIFYCODE", "code": "3", "errNo": "4", "errMsg": "获取验证码失败：" + str(e)})
    

#登陆后的验证码获取
@router.post("/get_log_verify_code")
def get_login_verification_code(request: UserLoginVerifyRequest, db: Session = Depends(get_db)):
    try:
        # 获取短信验证码
        verification_code = UserService.get_login_verification_code(db, request.userID, request.password)
        return {"what": "GET_LOGVERIFYCODE", "code": "0"}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"what": "GET_LOGVERIFYCODE", "code": "3", "errNo": "6", "errMsg": "获取验证码失败: " + str(e)})