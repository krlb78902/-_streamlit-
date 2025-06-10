import streamlit as st
import pandas as pd
import hashlib
import sqlite3
from datetime import datetime, timedelta
import base64

# 页面配置
st.set_page_config(
    page_title="用户认证系统",
    page_icon="🔐",
    layout="wide"
)


# 自定义样式
def add_custom_css():
    custom_css = """
    <style>
        .stApp {
            max-width: 1000px;
            margin: 0 auto;
        }
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            border-radius: 0.5rem;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 2rem;
        }
        .btn-primary {
            background-color: #3b82f6 !important;
            color: white !important;
            border-radius: 0.375rem !important;
            padding: 0.5rem 1rem !important;
            font-weight: 500 !important;
        }
        .btn-secondary {
            background-color: #64748b !important;
            color: white !important;
            border-radius: 0.375rem !important;
            padding: 0.5rem 1rem !important;
            font-weight: 500 !important;
        }
        .form-group {
            margin-bottom: 1rem;
        }
        .form-label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }
        .form-input {
            width: 100%;
            padding: 0.5rem;
            border: 1px solid #d1d5db;
            border-radius: 0.375rem;
        }
        .error-message {
            color: #ef4444;
            margin-top: 0.5rem;
        }
        .success-message {
            color: #10b981;
            margin-top: 0.5rem;
        }
        .footer {
            text-align: center;
            margin-top: 2rem;
            color: #64748b;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


add_custom_css()


# 数据库操作
def create_users_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE NOT NULL,
                 email TEXT UNIQUE NOT NULL,
                 password_hash TEXT NOT NULL,
                 created_at TIMESTAMP NOT NULL,
                 last_login TIMESTAMP)''')
    conn.commit()
    conn.close()


def add_user(username, email, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    created_at = datetime.now()
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
                  (username, email, password_hash, created_at))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_user(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user


def update_password(username, new_password):
    password_hash = hashlib.sha256(new_password.encode()).hexdigest()
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET password_hash = ? WHERE username = ?", (password_hash, username))
    conn.commit()
    conn.close()


def update_last_login(username):
    last_login = datetime.now()
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET last_login = ? WHERE username = ?", (last_login, username))
    conn.commit()
    conn.close()


# 会话状态初始化
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'login'
if 'username' not in st.session_state:
    st.session_state.username = None
if 'error_message' not in st.session_state:
    st.session_state.error_message = None
if 'success_message' not in st.session_state:
    st.session_state.success_message = None

# 创建用户表
create_users_table()


# 登录页面
def login_page():
    st.markdown("""
    <div class="header">
        <h1>用户登录</h1>
        <p>欢迎回来，请登录您的账户</p>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        username = st.text_input("用户名", key="login_username", placeholder="请输入用户名")
        password = st.text_input("密码", type="password", key="login_password", placeholder="请输入密码")

        if st.button("登录", key="login_button", type="primary"):
            user = get_user(username)
            if user and user[3] == hashlib.sha256(password.encode()).hexdigest():
                st.session_state.username = username
                update_last_login(username)
                st.session_state.current_page = 'dashboard'
                st.session_state.success_message = f"欢迎回来，{username}！"
                st.experimental_rerun()
            else:
                st.session_state.error_message = "用户名或密码错误"

        col1, col2 = st.columns(2)
        with col1:
            if st.button("注册新账户", key="register_button"):
                st.session_state.current_page = 'register'
                st.session_state.error_message = None
                st.experimental_rerun()
        with col2:
            if st.button("忘记密码？", key="forgot_password_button"):
                st.session_state.current_page = 'forgot_password'
                st.session_state.error_message = None
                st.experimental_rerun()

        if st.session_state.error_message:
            st.markdown(f'<div class="error-message">{st.session_state.error_message}</div>', unsafe_allow_html=True)

        if st.session_state.success_message:
            st.markdown(f'<div class="success-message">{st.session_state.success_message}</div>',
                        unsafe_allow_html=True)


# 注册页面
def register_page():
    st.markdown("""
    <div class="header">
        <h1>创建新账户</h1>
        <p>填写以下信息注册新账户</p>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        username = st.text_input("用户名", key="register_username", placeholder="请输入用户名")
        email = st.text_input("邮箱", key="register_email", placeholder="请输入邮箱")
        password = st.text_input("密码", type="password", key="register_password", placeholder="请输入密码")
        confirm_password = st.text_input("确认密码", type="password", key="register_confirm_password",
                                         placeholder="请再次输入密码")

        if st.button("注册", key="register_submit_button", type="primary"):
            if not username or not email or not password:
                st.session_state.error_message = "所有字段均为必填项"
            elif password != confirm_password:
                st.session_state.error_message = "两次输入的密码不一致"
            else:
                if add_user(username, email, password):
                    st.session_state.success_message = "注册成功！请登录"
                    st.session_state.current_page = 'login'
                    st.experimental_rerun()
                else:
                    st.session_state.error_message = "用户名或邮箱已存在"

        if st.button("返回登录", key="back_to_login_button"):
            st.session_state.current_page = 'login'
            st.session_state.error_message = None
            st.experimental_rerun()

        if st.session_state.error_message:
            st.markdown(f'<div class="error-message">{st.session_state.error_message}</div>', unsafe_allow_html=True)

        if st.session_state.success_message:
            st.markdown(f'<div class="success-message">{st.session_state.success_message}</div>',
                        unsafe_allow_html=True)


# 忘记密码页面
def forgot_password_page():
    st.markdown("""
    <div class="header">
        <h1>重置密码</h1>
        <p>输入您的用户名，我们将发送密码重置指导</p>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        username = st.text_input("用户名", key="forgot_username", placeholder="请输入用户名")

        if st.button("发送重置邮件", key="send_reset_button", type="primary"):
            user = get_user(username)
            if user:
                # 实际应用中这里应该发送邮件
                st.session_state.success_message = "重置密码的指导已发送至您的邮箱"
                st.session_state.current_page = 'login'
                st.experimental_rerun()
            else:
                st.session_state.error_message = "未找到该用户"

        if st.button("返回登录", key="back_to_login_forgot_button"):
            st.session_state.current_page = 'login'
            st.session_state.error_message = None
            st.experimental_rerun()

        if st.session_state.error_message:
            st.markdown(f'<div class="error-message">{st.session_state.error_message}</div>', unsafe_allow_html=True)

        if st.session_state.success_message:
            st.markdown(f'<div class="success-message">{st.session_state.success_message}</div>',
                        unsafe_allow_html=True)


# 仪表盘页面
def dashboard_page():
    st.markdown(f"""
    <div class="header">
        <h1>欢迎，{st.session_state.username}！</h1>
        <p>这是您的个人仪表盘</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("账户创建日期", get_user(st.session_state.username)[4].split()[0])

    with col2:
        last_login = get_user(st.session_state.username)[5]
        st.metric("上次登录时间", last_login.split()[0] if last_login else "首次登录")

    st.markdown("### 账户操作")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("修改密码", key="change_password_button"):
            st.session_state.current_page = 'change_password'
            st.experimental_rerun()

    with col2:
        if st.button("退出登录", key="logout_button", type="secondary"):
            st.session_state.username = None
            st.session_state.current_page = 'login'
            st.session_state.success_message = "已成功退出登录"
            st.experimental_rerun()

    # 模拟用户数据
    st.markdown("### 用户数据统计")
    user_data = {
        "订单总数": [np.random.randint(10, 100)],
        "平均订单金额": [np.random.randint(100, 1000)],
        "会员等级": ["高级会员" if np.random.random() > 0.5 else "普通会员"]
    }
    st.dataframe(pd.DataFrame(user_data), use_container_width=True)


# 修改密码页面
def change_password_page():
    st.markdown("""
    <div class="header">
        <h1>修改密码</h1>
        <p>设置新的账户密码</p>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        old_password = st.text_input("当前密码", type="password", key="old_password", placeholder="请输入当前密码")
        new_password = st.text_input("新密码", type="password", key="new_password", placeholder="请输入新密码")
        confirm_new_password = st.text_input("确认新密码", type="password", key="confirm_new_password",
                                             placeholder="请再次输入新密码")

        if st.button("修改密码", key="submit_change_password_button", type="primary"):
            user = get_user(st.session_state.username)
            if user[3] != hashlib.sha256(old_password.encode()).hexdigest():
                st.session_state.error_message = "当前密码不正确"
            elif new_password != confirm_new_password:
                st.session_state.error_message = "两次输入的新密码不一致"
            else:
                update_password(st.session_state.username, new_password)
                st.session_state.success_message = "密码修改成功"
                st.session_state.current_page = 'dashboard'
                st.experimental_rerun()

        if st.button("返回", key="back_from_change_password_button"):
            st.session_state.current_page = 'dashboard'
            st.session_state.error_message = None
            st.experimental_rerun()

        if st.session_state.error_message:
            st.markdown(f'<div class="error-message">{st.session_state.error_message}</div>', unsafe_allow_html=True)

        if st.session_state.success_message:
            st.markdown(f'<div class="success-message">{st.session_state.success_message}</div>',
                        unsafe_allow_html=True)


# 页面路由
if st.session_state.current_page == 'login':
    login_page()
elif st.session_state.current_page == 'register':
    register_page()
elif st.session_state.current_page == 'forgot_password':
    forgot_password_page()
elif st.session_state.current_page == 'dashboard':
    dashboard_page()
elif st.session_state.current_page == 'change_password':
    change_password_page()

# 页脚
st.markdown("""
<div class="footer">
    <p>© 2023 用户认证系统 | 保护您的账户安全</p>
</div>
""", unsafe_allow_html=True)