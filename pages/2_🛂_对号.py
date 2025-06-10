import streamlit as st

# 设置页面标题
st.set_page_config(page_title="双色球工具",
                   page_icon="./fucd.png",
                   layout="centered",
                   initial_sidebar_state="collapsed")

st.title("对号页面🛂")

# 设置主布局
mainLayout = st.columns([1, 3, 1])
with mainLayout[1]:

    # 设置返回按钮布局
    curLayout = st.columns([3, 1])

    with curLayout[1]:
        # 返回按钮
        if st.button('←返回'):
            st.switch_page("☯_主页.py")