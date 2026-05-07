from database import engine, Base
from models import OldPerson, Admin, Log, PositionEnum, TestData, SceneEnum
from sqlalchemy.orm import Session
import os

# 备份旧数据库（如果存在）
if os.path.exists("fall_detection.db"):
    os.rename("fall_detection.db", "fall_detection_backup.db")
    print("已备份旧数据库")

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
    
    # 添加多个值班人员数据（支持不同班次）
    admins = [
        Admin(id="0001", name="小张", age=30, gender="女", position=PositionEnum.MONITOR_ADMIN, phone="13800138004", password="123456", is_active=True),
        Admin(id="0002", name="小丽", age=28, gender="女", position=PositionEnum.MONITOR_ADMIN, phone="13800138005", password="123456", is_active=True),
        Admin(id="0003", name="小王", age=32, gender="男", position=PositionEnum.MONITOR_ADMIN, phone="13800138006", password="123456", is_active=True),
        Admin(id="0004", name="老赵", age=45, gender="男", position=PositionEnum.NURSE, phone="13800138007", password="123456", is_active=True),
        Admin(id="0005", name="系统管理员", age=35, gender="男", position=PositionEnum.SYSTEM_ADMIN, phone="13800138008", password="admin", is_active=True),
    ]
    db.add_all(admins)
    
    # 添加测试数据（共用数据）
    test_data_shared = [
        TestData(test_name="共用数据-房间测试", test_type="共用数据", scene=SceneEnum.ROOM, total_samples=500, true_positive=220, false_positive=15, false_negative=20, true_negative=245),
        TestData(test_name="共用数据-大厅测试", test_type="共用数据", scene=SceneEnum.HALL, total_samples=400, true_positive=175, false_positive=20, false_negative=18, true_negative=187),
        TestData(test_name="共用数据-院落测试", test_type="共用数据", scene=SceneEnum.YARD, total_samples=350, true_positive=150, false_positive=25, false_negative=22, true_negative=153),
    ]
    db.add_all(test_data_shared)
    
    # 添加测试数据（自测实景数据）
    test_data_self = [
        TestData(test_name="自测数据-房间测试", test_type="自测实景数据", scene=SceneEnum.ROOM, total_samples=300, true_positive=135, false_positive=10, false_negative=12, true_negative=143),
        TestData(test_name="自测数据-大厅测试", test_type="自测实景数据", scene=SceneEnum.HALL, total_samples=250, true_positive=110, false_positive=12, false_negative=9, true_negative=119),
        TestData(test_name="自测数据-院落测试", test_type="自测实景数据", scene=SceneEnum.YARD, total_samples=200, true_positive=85, false_positive=15, false_negative=10, true_negative=90),
    ]
    db.add_all(test_data_self)
    
    db.commit()
    print("数据库初始化完成，包含：")
    print("- 3个老人数据")
    print("- 5个管理员账号（支持不同班次）")
    print("- 6条测试数据（共用数据和自测实景数据）")

if __name__ == "__main__":
    init_data()