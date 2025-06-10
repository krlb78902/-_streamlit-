import pandas as pd
import streamlit as st

from utils.codeGenerate import codeGenerate

# 设置页面标题
st.set_page_config(page_title="双色球工具",
                   page_icon="./fucd.png",
                   layout="centered",
                   initial_sidebar_state="collapsed")

# 定义标题显示布局

mainLayout = st.columns([1, 20, 3])
with mainLayout[1]:
    # 设置标题当前布局
    curLayout = st.columns([2, 3, 1])

    with curLayout[1]:
        st.title("出号 🎫")

# 设置一个接收需要生成几个双色球号码的input
# 设置布局
with mainLayout[1]:
    curLayout = st.columns([2, 1])

    # 设置号码生成数量输入框
    with curLayout[0]:
        # 获取输入的需要生成双色球号码的数量
        codeNum = st.number_input(
            label="选择号码生成数量",
            min_value=0,
            max_value= 100,
            step=1,
            value=None,
            placeholder="请输入需要生成的号码"
        )

    # 设置模式选择框
    with curLayout[1]:
        # 定义下拉列表可选择的模式和对应的值
        fruit_dict = {"普通模式": 1, "预测模式": 2, "": None,}

        # 使用变量存储选择的模式
        modelSelect = st.selectbox(
            label="选择模式",
            options=list(fruit_dict.keys()),
            index= len(fruit_dict) - 1
        )

    df = None

    if modelSelect != "" and codeNum is not None:
        model = fruit_dict[modelSelect]
        # st.write(f"您当前要生成的号码数量是：{codeNum}，生成模式为：{modelSelect}")
        codeList = codeGenerate(codeNum, model)

        # 将codeList转换为 DataFrame
        df = pd.DataFrame([
            {
                "红色球1号": list(item["redCodes"])[0],
                "红色球2号": list(item["redCodes"])[1],
                "红色球3号": list(item["redCodes"])[2],
                "红色球4号": list(item["redCodes"])[3],
                "红色球5号": list(item["redCodes"])[4],
                "红色球6号": list(item["redCodes"])[5],
                "蓝色球": item["blueCodes"]
            }
            for item in codeList
        ])

    if codeNum is not None and codeNum > 0 and df is not None:
        st.dataframe(
            df,
            hide_index=True,
            height=300,
            use_container_width=True
        )



with mainLayout[1]:
    # 设置返回按钮当前的布局
    curLayout = st.columns([4, 1])

    with curLayout[1]:
        # 返回按钮
        if st.button('←返回'):
            st.switch_page("☯_主页.py")