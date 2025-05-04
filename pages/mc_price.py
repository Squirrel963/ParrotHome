import streamlit as st
import requests
import json
import numpy as np
import pandas as pd

def get_data_from_api(api_url):  
    response = requests.get(api_url, verify=False)  
    data = response.content
    return data

st.title("MineCraft正版价格监控")
st.sidebar.page_link("PWUI.py", label="返回主页", icon=":material/home:",use_container_width=True)

if st.button("获取数据",use_container_width=True):
    with st.status("加载中...",expanded=True):
        st.write("正在从SAR_api获取数据...")
        prices = get_data_from_api("https://www.wycc.dedyn.io/api/MPapi/history").decode('utf-8').split("\r\n")
        Date = []
        Deluxe = []
        Standard = []
        st.write("正在处理数据...")
        for i in prices:
            temp = json.loads(i)
            Date.append(temp['date'])
            Deluxe.append(float(temp['Deluxe']))
            Standard.append(float(temp['Standard']))
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="标准版近期价格（RMB）", value=f"{Standard[-1]}", border=True, delta=f"{Standard[-2]-Standard[-1]}")
    with col2:
        st.metric(label="豪华版近期价格（RMB）", value=f"{Deluxe[-1]}", border=True, delta=f"{Deluxe[-2]-Deluxe[-1]}")
    data = {
        "date": Date,
        "豪华版本": Deluxe,
        "标准版本": Standard
    }

    df = pd.DataFrame(data)

    df['date'] = pd.to_datetime(df['date'], format='%Y/%m-%d')

    df.set_index('date', inplace=True)

    st.line_chart(df)