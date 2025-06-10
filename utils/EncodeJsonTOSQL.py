import json
import sqlite3
import os
from datetime import datetime


def create_database(db_path="../data/lottery_data.db"):
    """创建SQLite数据库和表结构"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 创建双色球数据表
    cursor.execute('''
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
    )
    ''')

    # 创建奖级表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS prize_grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lottery_code TEXT,
        prize_type INTEGER,
        prize_type_num TEXT,
        prize_money TEXT,
        FOREIGN KEY (lottery_code) REFERENCES double_color_ball (code)
    )
    ''')

    conn.commit()
    conn.close()
    print(f"数据库和表结构创建成功，保存至: {db_path}")
    return db_path


def parse_lottery_data(json_data):
    """解析JSON数据并返回可插入数据库的格式"""
    data = json.loads(json_data)
    lottery_records = []
    prize_grade_records = []

    for item in data.get("result", []):
        # 处理双色球基本信息
        lottery_record = (
            item.get("name"),
            item.get("code"),
            item.get("detailsLink"),
            item.get("videoLink"),
            item.get("date"),
            item.get("week"),
            item.get("red"),
            item.get("blue"),
            item.get("blue2"),
            item.get("sales"),
            item.get("poolmoney"),
            item.get("content"),
            item.get("addmoney"),
            item.get("addmoney2"),
            item.get("msg"),
            item.get("z2add"),
            item.get("m2add"),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        lottery_records.append(lottery_record)

        # 处理奖级信息
        prize_grades = item.get("prizegrades", [])
        for grade in prize_grades:
            prize_record = (
                item.get("code"),
                grade.get("type"),
                grade.get("typenum"),
                grade.get("typemoney")
            )
            prize_grade_records.append(prize_record)

    return lottery_records, prize_grade_records


def insert_data_to_database(json_data, db_path="../data/lottery_data.db"):
    """将解析后的数据插入数据库"""
    if not os.path.exists(db_path):
        create_database(db_path)

    lottery_records, prize_grade_records = parse_lottery_data(json_data)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # 插入双色球基本信息
        cursor.executemany('''
        INSERT OR IGNORE INTO double_color_ball (
            name, code, details_link, video_link, draw_date, week, 
            red_balls, blue_ball, blue_ball2, sales_amount, pool_money, 
            winning_content, add_money, add_money2, msg, z2add, m2add, create_time
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', lottery_records)

        # 插入奖级信息
        cursor.executemany('''
        INSERT INTO prize_grades (
            lottery_code, prize_type, prize_type_num, prize_money
        ) VALUES (?, ?, ?, ?)
        ''', prize_grade_records)

        conn.commit()
        print(f"成功插入 {len(lottery_records)} 条双色球记录和 {len(prize_grade_records)} 条奖级记录")
    except sqlite3.Error as e:
        print(f"插入数据时出错: {e}")
        conn.rollback()
    finally:
        conn.close()


def process_json_file(file_path, db_path="../data/lottery_data.db"):
    """处理JSON文件并导入数据库"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = f.read()
        insert_data_to_database(json_data, db_path)
    except FileNotFoundError:
        print(f"文件不存在: {file_path}")
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
    except Exception as e:
        print(f"处理文件时出错: {e}")


# 使用示例
if __name__ == "__main__":
    # 直接使用JSON字符串进行测试
    json_data = '''
    {"state":0,"message":"查询成功","total":1870,"pageNum":1,"pageNo":1,"pageSize":100000000,"Tflag":0,"result":[
        {"name":"双色球","code":"2025063","detailsLink":"/c/2025/06/05/617331.shtml","videoLink":"/c/2025/06/05/617335.shtml","date":"2025-06-05(四)","week":"四","red":"02,19,21,22,28,30","blue":"01","blue2":"","sales":"366105242","poolmoney":"2377447244","content":"福建1注，湖北10注，云南1注，共12注。","addmoney":"","addmoney2":"","msg":"","z2add":"","m2add":"","prizegrades":[{"type":1,"typenum":"12","typemoney":"7110664"},{"type":2,"typenum":"77","typemoney":"411168"},{"type":3,"typenum":"617","typemoney":"3000"},{"type":4,"typenum":"45795","typemoney":"200"},{"type":5,"typenum":"1009501","typemoney":"10"},{"type":6,"typenum":"6329337","typemoney":"5"},{"type":7,"typenum":"","typemoney":""}]},
        {"name":"双色球","code":"2025062","detailsLink":"/c/2025/06/03/617117.shtml","videoLink":"/c/2025/06/03/617120.shtml","date":"2025-06-03(二)","week":"二","red":"06,08,09,13,25,31","blue":"14","blue2":"","sales":"353685018","poolmoney":"2367795314","content":"山西1注，辽宁1注，吉林1注，广东2注，云南1注，共6注。","addmoney":"","addmoney2":"","msg":"","z2add":"","m2add":"","prizegrades":[{"type":1,"typenum":"6","typemoney":"8384899"},{"type":2,"typenum":"115","typemoney":"220754"},{"type":3,"typenum":"1524","typemoney":"3000"},{"type":4,"typenum":"68272","typemoney":"200"},{"type":5,"typenum":"1392454","typemoney":"10"},{"type":6,"typenum":"7921545","typemoney":"5"},{"type":7,"typenum":"","typemoney":""}]}
    ]}
    '''

    # 插入数据到数据库
    insert_data_to_database(json_data)