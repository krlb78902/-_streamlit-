import streamlit as st

# 设置页面标题和其他配置
st.set_page_config(page_title="双色球工具",
                   page_icon="./fucd.png",
                   layout="centered",
                   initial_sidebar_state="collapsed")

# 添加标题
st.title("欢迎来到双色球彩票工具应用 ☯")
# 添加文本
st.write("这里可以随机出号，也可以检查是否中奖！")

# # 添加Markdown文本
# st.markdown("""
# ### 这是一个Markdown标题
# - 列表项1
# - 列表项2
# - 列表项3
# """)

# # 添加侧边栏
# with st.sidebar:
#     st.header("功能选择")
#     st.button("出号")
#     st.button("对号")

# 添加页面跳转按钮
# if st.button("点击我"):
#     st.balloons()  # 显示气球动画
#     st.success("按钮被点击了!")


# 配置主页面导航按钮
if st.button("出号 🎫", use_container_width=True):
    # st.success("开始出号！")
    st.switch_page("pages/1_🎫_出号.py")

if st.button("对号 🛂", use_container_width=True):
    # st.success("对号中！")
    st.switch_page("pages/2_🛂_对号.py")

if st.button("双色球走势分析 💹", use_container_width=True):
    # st.success("对号中！")
    st.switch_page("pages/3_💹_双色球走势分析.py")

st.link_button("进入福彩官网", "https://www.cwl.gov.cn/", use_container_width=True)


# # 添加滑块
# age = st.slider("你的年龄", 0, 100, 25)
# st.write(f"你选择了: {age}岁")

# 添加选择框
# option = st.selectbox(
#     "你最喜欢哪个颜色?",
#     ("红色", "蓝色", "绿色"))
# st.write(f"你选择了: {option}")