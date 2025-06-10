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
