from database import SessionLocal
from models import Admin

# 创建数据库会话
db = SessionLocal()

try:
    # 更新管理员名字
    db.query(Admin).filter(Admin.id == '0001').update({'name': '小张'})
    db.query(Admin).filter(Admin.id == '0002').update({'name': '小丽'})
    db.query(Admin).filter(Admin.id == '0003').update({'name': '小王'})
    
    # 提交更改
    db.commit()
    print('工作人员名字已更新成功！')
    
    # 验证更新结果
    admins = db.query(Admin).all()
    print('更新后的工作人员列表：')
    for admin in admins:
        print(f'ID: {admin.id}, 名字: {admin.name}, 职位: {admin.position}')
finally:
    # 关闭数据库会话
    db.close()
