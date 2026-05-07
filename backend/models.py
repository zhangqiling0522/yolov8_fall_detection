from sqlalchemy import Column, Integer, String, DateTime, Enum, Float, Boolean
from sqlalchemy.sql import func
import enum
from database import Base

# 职务枚举类
class PositionEnum(str, enum.Enum):
    NURSE = "护工"
    SYSTEM_ADMIN = "系统管理员"
    MONITOR_ADMIN = "监控管理员"

# 场景枚举类
class SceneEnum(str, enum.Enum):
    ROOM = "房间"
    HALL = "大厅"
    YARD = "院落"

# 检测结果枚举类
class DetectionResultEnum(str, enum.Enum):
    TRUE_POSITIVE = "真阳性"
    FALSE_POSITIVE = "假阳性"
    FALSE_NEGATIVE = "假阴性"
    TRUE_NEGATIVE = "真阴性"

# 老人表
class OldPerson(Base):
    __tablename__ = "old_person"
    
    id = Column(String(4), primary_key=True, index=True)  # 4位编号
    name = Column(String(50), nullable=False)  # 姓名
    age = Column(Integer, nullable=False)  # 年龄
    gender = Column(String(10), nullable=False)  # 性别
    room_number = Column(String(10), nullable=False, index=True)  # 房间号
    phone = Column(String(20), nullable=False)  # 联系电话

# 管理人员表
class Admin(Base):
    __tablename__ = "admin"
    
    id = Column(String(4), primary_key=True, index=True)  # 4位编号
    name = Column(String(50), nullable=False)  # 姓名
    age = Column(Integer, nullable=False)  # 年龄
    gender = Column(String(10), nullable=False)  # 性别
    position = Column(Enum(PositionEnum), nullable=False)  # 职务
    phone = Column(String(20), nullable=False, unique=True)  # 手机号
    password = Column(String(100), nullable=False)  # 密码
    is_active = Column(Boolean, default=True)  # 是否在职

# 日志表
class Log(Base):
    __tablename__ = "log"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # 自增ID
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # 时间
    room_number = Column(String(10), nullable=False, index=True)  # 房间号
    scene = Column(Enum(SceneEnum), nullable=False, default=SceneEnum.ROOM)  # 场景
    phone = Column(String(20), nullable=False)  # 电话号
    status = Column(String(20), nullable=False, default="摔倒检测")  # 状态描述
    detection_result = Column(Enum(DetectionResultEnum))  # 检测结果（用于统计）
    confidence = Column(Float)  # 检测置信度
    admin_id = Column(String(4))  # 处理的管理员ID

# 测试数据表
class TestData(Base):
    __tablename__ = "test_data"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    test_name = Column(String(100), nullable=False)  # 测试名称
    test_type = Column(String(20), nullable=False)  # 测试类型：共用数据/自测实景数据
    scene = Column(Enum(SceneEnum), nullable=False)  # 场景
    total_samples = Column(Integer, nullable=False, default=0)  # 总样本数
    true_positive = Column(Integer, nullable=False, default=0)  # 真阳性
    false_positive = Column(Integer, nullable=False, default=0)  # 假阳性
    false_negative = Column(Integer, nullable=False, default=0)  # 假阴性
    true_negative = Column(Integer, nullable=False, default=0)  # 真阴性
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)