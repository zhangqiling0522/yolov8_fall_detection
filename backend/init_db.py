from database import engine, Base
from models import OldPerson, Admin, Log, PositionEnum
from sqlalchemy.orm import Session

# 创建所有表
Base.metadata.create_all(bind=engine)

# 添加初始数据
def init_data():
    db = Session(bind=engine)
    
    # 检查是否已有数据
    if db.query(OldPerson).count() > 0:
        print("数据库已有数据，跳过初始化")
        return
    
    # 添加老人数据
    old_persons = [
        OldPerson(id="0001", name="张三", age=75, gender="男", room_number="101", phone="13800138001"),
        OldPerson(id="0002", name="李四", age=82, gender="女", room_number="102", phone="13800138002"),
        OldPerson(id="0003", name="王五", age=78, gender="男", room_number="103", phone="13800138003"),
    ]
    db.add_all(old_persons)
    
    # 添加管理人员数据
    admins = [
        Admin(id="0001", name="管理员1", age=30, gender="男", position=PositionEnum.SYSTEM_ADMIN),
        Admin(id="0002", name="护工1", age=45, gender="女", position=PositionEnum.NURSE),
        Admin(id="0003", name="监控员1", age=28, gender="男", position=PositionEnum.MONITOR_ADMIN),
    ]
    db.add_all(admins)
    
    db.commit()
    print("数据库初始化完成")

if __name__ == "__main__":
    init_data()