from database import engine
import sqlite3

# 连接到SQLite数据库
conn = sqlite3.connect('fall_detection.db')
cursor = conn.cursor()

try:
    # 检查admin表是否存在phone字段
    cursor.execute("PRAGMA table_info(admin)")
    columns = [column[1] for column in cursor.fetchall()]
    
    # 如果phone字段不存在，添加它
    if 'phone' not in columns:
        cursor.execute("ALTER TABLE admin ADD COLUMN phone VARCHAR(20) NOT NULL DEFAULT '13800138000'")
        print('已添加phone字段')
    else:
        print('phone字段已存在')
    
    # 如果password字段不存在，添加它
    if 'password' not in columns:
        cursor.execute("ALTER TABLE admin ADD COLUMN password VARCHAR(100) NOT NULL DEFAULT '123456'")
        print('已添加password字段')
    else:
        print('password字段已存在')
    
    # 提交更改
    conn.commit()
    print('表结构修改成功！')
    
    # 更新现有数据的phone和password值
    cursor.execute("UPDATE admin SET phone='13800138004', password='123456' WHERE id='0001'")
    cursor.execute("UPDATE admin SET phone='13800138005', password='123456' WHERE id='0002'")
    cursor.execute("UPDATE admin SET phone='13800138006', password='123456' WHERE id='0003'")
    conn.commit()
    print('现有数据已更新！')
    
finally:
    # 关闭数据库连接
    conn.close()
