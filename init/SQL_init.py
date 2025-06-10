import sqlite3
import os
from datetime import datetime


def initialize_database(db_path="lottery_data.db", sql_path="double_color_ball.sql"):
    """初始化双色球数据库"""
    # 确保数据库和SQL文件的父目录存在
    db_dir = os.path.dirname(db_path)
    sql_dir = os.path.dirname(sql_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
    if sql_dir and not os.path.exists(sql_dir):
        os.makedirs(sql_dir)

    # 检查SQL初始化文件是否存在
    if not os.path.exists(sql_path):
        print(f"SQL初始化文件不存在，将自动创建: {sql_path}")
        create_sql_initialization_file(sql_path)

    # 连接数据库（不存在则创建）
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # 读取SQL初始化脚本
        with open(sql_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        # 执行SQL脚本
        cursor.executescript(sql_script)
        conn.commit()

        print(f"数据库初始化成功，保存至: {db_path}")
        print(f"表结构和索引已创建")
        return True

    except sqlite3.Error as e:
        print(f"初始化数据库时出错: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def create_sql_initialization_file(file_path):
    """创建SQL初始化文件"""
    sql_content = '''
-- 双色球数据库初始化脚本（自动生成）
CREATE TABLE IF NOT EXISTS double_color_ball (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    code TEXT UNIQUE,
    details_link TEXT,
    video_link TEXT,
    draw_date TEXT,
    week TEXT,
    red_balls TEXT,
    blue_ball TEXT,
    blue_ball2 TEXT,
    sales_amount TEXT,
    pool_money TEXT,
    winning_content TEXT,
    add_money TEXT,
    add_money2 TEXT,
    msg TEXT,
    z2add TEXT,
    m2add TEXT,
    create_time TEXT
);

CREATE TABLE IF NOT EXISTS prize_grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lottery_code TEXT,
    prize_type INTEGER,
    prize_type_num TEXT,
    prize_money TEXT,
    FOREIGN KEY (lottery_code) REFERENCES double_color_ball (code)
);
'''
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(sql_content.strip())
    print(f"已自动生成SQL初始化文件: {file_path}")


if __name__ == "__main__":
    # 执行数据库初始化（使用相对路径）
    db_path = "../data/lottery_data.db"
    sql_path = "../data/double_color_ball.sql"

    # 初始化数据库（包含自动创建文件夹）
    initialize_database(db_path, sql_path)