import mysql.connector
from environs import Env    # new
env = Env()     # new
env.read_env()

db = mysql.connector.connect(
    host=env('HOST'),
    user=env('USER'),
    password=env('PASSWORD'),
    database=env('DATABASE')
)

# 获取所有表名
def get_table_names(cursor):
    cursor.execute("SHOW TABLES")
    return [table[0] for table in cursor]

# 检查表是否为空
def is_table_empty(cursor, table_name):
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    result = cursor.fetchone()
    return result[0] == 0

# 删除空表
def delete_empty_tables(cursor, table_names):
    for table_name in table_names:
        if is_table_empty(cursor, table_name):
            cursor.execute(f"DROP TABLE {table_name}")
            print(f"已删除空表：{table_name}")

# 批量查阅数据库中的表是否为空并删除空表
def check_and_delete_empty_tables(db):
    cursor = db.cursor()
    table_names = get_table_names(cursor)
    delete_empty_tables(cursor, table_names)
    cursor.close()

# 查阅数据库里有多少表，以及包含关键字的表数量
def search_tables_by_keyword(db, keyword):
    cursor = db.cursor()
    table_names = get_table_names(cursor)
    
    # 查阅数据库里有多少表
    total_tables = len(table_names)
    print(f"数据库中共有 {total_tables} 张表。")

    # 搜索包含关键字的表
    keyword_tables = []
    for table_name in table_names:
        if keyword.lower() in table_name.lower():
            keyword_tables.append(table_name)
    keyword_table_count = len(keyword_tables)
    
    # 输出包含关键字的表的数量和表名
    print(f"关键字 '{keyword}' 出现在 {keyword_table_count} 张表的名字中：")
    """
    for table_name in keyword_tables:
        print(table_name)"""

    cursor.close()

search_tables_by_keyword(db, "shanghai")

check_and_delete_empty_tables(db)

db.close()
