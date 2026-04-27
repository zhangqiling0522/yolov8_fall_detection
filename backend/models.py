from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
import enum
from database import Base

# 职务枚举类
class PositionEnum(str, enum.Enum):
    NURSE = "护工"
    SYSTEM_ADMIN = "系统管理员"
    MONITOR_ADMIN = "监控管理员"

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
    phone = Column(String(20), nullable=False)  # 手机号
    password = Column(String(100), nullable=False)  # 密码

# 日志表
class Log(Base):
    __tablename__ = "log"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # 自增ID
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # 时间
    room_number = Column(String(10), nullable=False, index=True)  # 房间号
    phone = Column(String(20), nullable=False)  # 电话号
    status = Column(String(20), nullable=False, default="摔倒检测")  # 状态描述