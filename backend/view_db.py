import sqlite3
import os

# 数据库文件路径
db_path = os.path.join(os.path.dirname(__file__), 'fall_detection.db')

# 连接数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== 数据库表结构和数据 ===")
print(f"数据库文件: {db_path}")
print("\n")

# 获取所有表名
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# 遍历每个表
for table in tables:
    table_name = table[0]
    print(f"=== 表: {table_name} ===")
    
    # 获取表结构
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    print("表结构:")
    print("字段名\t\t类型\t\t是否主键")
    print("-" * 50)
    for column in columns:
        col_id, col_name, col_type, not_null, default, pk = column
        pk_flag = "是" if pk else "否"
        print(f"{col_name}\t\t{col_type}\t\t{pk_flag}")
    
    # 获取表数据
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    print("\n表数据:")
    if rows:
        # 打印表头
        headers = [column[1] for column in columns]
        print("\t".join(headers))
        print("-" * 80)
        # 打印数据行
        for row in rows:
            print("\t".join(str(item) for item in row))
    else:
        print("无数据")
    print("\n" + "=" * 60 + "\n")

# 关闭连接
conn.close()

print("数据库查询完成！")