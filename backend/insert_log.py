from database import SessionLocal
from models import Log
import datetime

# 创建数据库会话
db = SessionLocal()

try:
    # 创建新的日志记录
    new_log = Log(
        timestamp=datetime.datetime(2026, 2, 26, 12, 0, 0),  # 2026/2/26 12:00:00
        room_number="101",
        phone="13800138001",
        status="摔倒"
    )
    
    # 添加到数据库
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    
    print("日志记录插入成功！")
    print(f"插入的记录ID: {new_log.id}")
    print(f"时间: {new_log.timestamp}")
    print(f"房间号: {new_log.room_number}")
    print(f"电话: {new_log.phone}")
    print(f"状态: {new_log.status}")
    
finally:
    # 关闭数据库会话
    db.close()
