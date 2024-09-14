from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Any, Optional

class SuperAdminLoginRequest(BaseModel):
    superID: str
    superPasswd: str
    verifyCode: str
    needAnswer: str = 'yes'
    
class UserRegisterRequest(BaseModel):
    userID: str
    userName: str
    userPhone: str
    password: str
    verifyCode: str
    needAnswer: str = "yes"

class UserLoginRequest(BaseModel):
    userID: str
    userPasswd: str
    needAnswer: str = "yes"

class UserTokenLoginRequest(BaseModel):
    userToken: str
    needAnswer: str = "yes"

class UserTokenLoginRequest(BaseModel):
    userID: str
    token: str
    needAnswer: str = "yes"
    

class GetVerifyCodeRequest(BaseModel):
    userID: str
    userName: str
    userPhone: str
    password: str
    needAnswer: str = "no"
        
class UserLoginVerifyRequest(BaseModel):
    userID: str
    password: str
    needAnswer: str = "no"
    
class UserCheckRequest(BaseModel):
    userID: str
    needAnswer: str = "yes"

class AreaQueryRequest(BaseModel):
    systemID: str
    first: int
    number: int
    token: str
    needAnswer: str = "yes"
    
class AreaAddRequest(BaseModel):
    token: str
    systemID: str
    number: int
    area: List[Dict[str, Any]]
    needAnswer: str = "yes"

class AreaUpdateRequest(BaseModel):
    token: str
    systemID: str
    number: int
    area: List[Dict[str, Any]]
    needAnswer: str = "yes"

class AreaDeleteRequest(BaseModel):
    token: str
    systemID: str
    number: int
    area: List[Dict[str, Any]]
    needAnswer: str = "yes"


class SystemCreate(BaseModel):
    systemID: str
    newSystem: str
    adminID: str
    adminPasswd: str
    adminPhoneNum: str
    

class SystemUpdate(BaseModel):
    systemID: str
    systemName: str
    adminID: str
    passwd: str
    phoneNum: str
    needAnswer: str = "yes"

class SystemListResponse(BaseModel):
    what: str
    code: str
    number: int
    system: List[SystemCreate]
    

class UploadBackgroundImageRequest(BaseModel):
    systemID: str
    pngFile: str
    needAnswer: str = "yes"

class UploadBackgroundImageResponse(BaseModel):
    what: str
    code: str
    fileToken: str

class CheckSystemAvailabilityRequest(BaseModel):
    newSystem: str
    adminID: str
    needAnswer: str = "yes"
    
class TaskBase(BaseModel):
    systemID: str
    taskName: str
    taskType: str
    action: str
    actTime: int
    actOnTime: int
    number1: int
    setupDay: str
    repeatMode: str
    intervalDay: int
    actDay: str
    cycleNum: int
    concurrent: int
    begin: List[dict]
    sense: List[dict]
    station: List[dict]
    areaID: str
    memo: Optional[str]
    needAnswer: Optional[str] = "yes"

# 新增任务请求体
class TaskCreate(BaseModel):
    todo: str = "ADD_TASK"
    token: str
    systemID: str
    taskName: str
    taskType: str  # TIMING/CYCLING/SENSOR/SCENERY
    action: str  # TURN-ON/TURN_OFF/TURN_ADJ/COLLECT/ORDER
    actTime: int  # 动作执行时间（毫秒）
    actOnTime: int  # 动作保持时间
    number1: int  # 一天内动作次数
    setupDay: str  # 设置日
    repeatMode: str  # ODD_DAY/EVEN_DAY/WORKDAY/INT_DAY
    intervalDay: Optional[int] = None  # 间隔天数（可选）
    actDay: Optional[str] = None  # 动作日期
    cycleNum: Optional[int] = None  # 循环次数
    concurrent: Optional[int] = None  # 同时动作设备数量
    begin: List[dict]  # 动作时间列表
    number2: int  # 相关传感参数数量
    sense: List[dict]  # 传感器相关参数
    number3: int  # 被选分站数量
    station: List[dict]  # 分站设备列表
    areaID: str
    memo: Optional[str] = None
    needAnswer: str = "yes"

# 新增任务响应体
class TaskResponse(BaseModel):
    what: str
    code: str
    taskID: Optional[str] = None
    taskName: Optional[str] = None
    errNo: Optional[str] = None
    errMsg: Optional[str] = None
    tasks: Optional[List[TaskBase]] = None


class TaskUpdate(BaseModel):
    taskID: str
    taskName: Optional[str] = None
    taskType: Optional[str] = None
    action: Optional[str] = None
    actTime: Optional[int] = None
    actOnTime: Optional[int] = None
    number1: Optional[int] = None
    setupDay: Optional[str] = None
    repeatMode: Optional[str] = None
    intervalDay: Optional[int] = None
    actDay: Optional[str] = None
    cycleNum: Optional[int] = None
    concurrent: Optional[int] = None
    beginTime: Optional[str] = None
    highValue: Optional[float] = None
    highAct: Optional[str] = None
    lowValue: Optional[float] = None
    lowAct: Optional[str] = None
    stationID: Optional[str] = None
    areaID: Optional[str] = None
    memo: Optional[str] = None

class TaskDelete(BaseModel):
    systemID: str
    taskID: str

class TaskQuery(BaseModel):
    systemID: str
    taskID: Optional[str]

class TaskItem(BaseModel):
    taskID: str
    taskName: str
    taskType: str
    action: str
    actTime: int
    actOnTime: int
    number1: int
    setupDay: str
    repeatMode: str
    intervalDay: Optional[int] = None
    actDay: Optional[str] = None
    cycleNum: Optional[int] = None
    concurrent: Optional[int] = None
    begin: Optional[List[dict]] = None
    sense: Optional[List[dict]] = None
    station: Optional[List[dict]] = None
    areaID: str
    memo: Optional[str] = None

# 公共部分
class Station(BaseModel):
    stationID: str

class SenseParam(BaseModel):
    highValue: float
    highAct: str
    lowValue: float
    lowAct: str


class TaskRunModeRequest(BaseModel):
    token: str
    systemID: str
    taskID: str
    runMode: str
    needAnswer: Optional[str] = "yes"

class TaskRunModeResponse(BaseModel):
    what: str
    code: str
    taskID: str
    runMode: Optional[str] = None
    errNo: Optional[str] = None
    errMsg: Optional[str] = None

class TaskHistoryRequest(BaseModel):
    todo: str
    token: str
    systemID: str
    taskID: str
    beginTime: str
    endTime: str
    needAnswer: Optional[str] = "yes"

class TaskHistoryResponse(BaseModel):
    what: str
    code: str
    taskID: str
    history: Optional[List[dict]] = None
    errNo: Optional[str] = None
    errMsg: Optional[str] = None


class TaskRunMode(BaseModel):
    taskID: str
    runMode: str

class SystemTaskRunModeRequest(BaseModel):
    systemID: str
    first: int
    number: int

class SystemTaskRunModeResponse(BaseModel):
    what: str = "QRY_SYSTASK"
    code: str
    first: int
    number: int
    tasks: Optional[List[TaskRunMode]] = []

class ErrorResponse(BaseModel):
    what: str
    code: str
    errNo: str
    errMsg: str
    
class EquipmentStatusRequest(BaseModel):
    todo: str
    token: str
    systemID: str
    number: int
    station: List[Station]
    runMode: Optional[str] = None
    needAnswer: Optional[str] = "yes"

class EquipmentStatusResponse(BaseModel):
    what: str
    code: str
    number: int
    station: Optional[List[dict]] = None
    errNo: Optional[str] = None
    errMsg: Optional[str] = None
    
    
    
class Report(BaseModel):
    reportID: str
    reportName: str
    createdDate: datetime

class ReportListRequest(BaseModel):
    token: str
    userID: str
    startDate: Optional[str]
    endDate: Optional[str]
    needAnswer: Optional[str] = 'yes'

class ReportListResponse(BaseModel):
    what: str
    code: str
    reports: Optional[List[Report]]
    errNo: Optional[str]
    errMsg: Optional[str]


class System(BaseModel):
    systemID: str
    systemName: str
    adminID: str
    setupDate: datetime

class Staff(BaseModel):
    userID: str

class SystemListRequest(BaseModel):
    token: str
    adminID: str
    first: Optional[int] = 0
    number: Optional[int] = 0
    needAnswer: Optional[str] = 'yes'

class SystemListResponse(BaseModel):
    what: str
    code: str
    number: Optional[int]
    system: Optional[List[System]]
    errNo: Optional[str]
    errMsg: Optional[str]

class AddStaffRequest(BaseModel):
    token: str
    systemID: str
    staff: List[Staff]
    needAnswer: Optional[str] = 'yes'

class AddStaffResponse(BaseModel):
    what: str
    code: str
    errNo: Optional[str]
    errMsg: Optional[str]

class StaffListRequest(BaseModel):
    token: str
    systemID: str
    first: Optional[int] = 0
    number: Optional[int] = 0
    needAnswer: Optional[str] = 'yes'

class StaffListResponse(BaseModel):
    what: str
    code: str
    number: Optional[int]
    staff: Optional[List[Staff]]
    errNo: Optional[str]
    errMsg: Optional[str]
    
# 分站相关的Schema

class SubstationCreate(BaseModel):
    systemID: str
    substationNo: int
    devEUI: str
    substationName: str
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    memo: Optional[str] = None

class SubstationUpdate(BaseModel):
    systemID: str
    substationNo: int
    devEUI: Optional[str] = None
    substationName: Optional[str] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    memo: Optional[str] = None

class SubstationDelete(BaseModel):
    systemID: str
    substationNo: int

class SubstationQuery(BaseModel):
    systemID: str
    hostNo: Optional[int] = None
    nodeNo: Optional[int] = None
    areaID: Optional[int] = None
    first: int
    number: int


# 主机相关的Schema
class HostCreate(BaseModel):
    systemID: str
    hostNo: int
    hostName: str
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    memo: Optional[str] = None

class HostUpdate(BaseModel):
    systemID: str
    hostNo: int
    hostName: Optional[str] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    memo: Optional[str] = None

class HostDelete(BaseModel):
    systemID: str
    hostNo: int

class HostQuery(BaseModel):
    systemID: str
    first: int
    number: int


# 节点相关的Schema

class NodeCreate(BaseModel):
    systemID: str
    hostNo: int
    nodeNo: int
    nodeName: str
    location: Optional[str] = None
    memo: Optional[str] = None

class NodeUpdate(BaseModel):
    systemID: str
    hostNo: int
    nodeNo: int
    nodeName: Optional[str] = None
    location: Optional[str] = None
    memo: Optional[str] = None

class NodeDelete(BaseModel):
    systemID: str
    hostNo: int
    nodeNo: int

class NodeQuery(BaseModel):
    systemID: str
    hostNo: Optional[int] = None
    nodeNo: Optional[int] = None
    first: int
    number: int
    
    
class StationHistoryRequest(BaseModel):
    todo: str
    token: str
    systemID: str
    areaID: str
    devType: str
    number: int
    station: List[Dict[str, str]]
    stationID: str
    qureyMode: str
    beginDay: str
    endDay: str
    needAnswer: str

class StationHistoryResponse(BaseModel):
    what: str
    code: str
    paramNum: int
    quantity: int
    data: List[Dict[str, List[Dict[str, str]]]]


class NodeActionRequest(BaseModel):
    todo: str
    token: str
    nodeID: str
    action: str   # ACTIVATE/DISABLE 或 SLEEP/WAKE

class NodeActionResponse(BaseModel):
    what: str
    code: str
    nodeID: str
    action: str

class NodeStatusRequest(BaseModel):
    todo: str
    token: str
    nodeID: str

class NodeStatusResponse(BaseModel):
    what: str
    code: str
    nodeID: str
    status: str

class NodeHistoryRequest(BaseModel):
    todo: str
    token: str
    nodeID: str
    beginDay: str
    endDay: str

class NodeHistoryResponse(BaseModel):
    what: str
    code: str
    paramNum: int
    quantity: int
    data: List[Dict[str, List[Dict[str, str]]]]
