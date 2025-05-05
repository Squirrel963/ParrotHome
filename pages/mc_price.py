import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
import requests
import json
import numpy as np
import pandas as pd

def get_data_from_api(api_url):  
    response = requests.get(api_url, verify=False)  
    data = response.content
    return data

st.title("MineCraft正版价格监测")
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
        st.write("完成！")
    col1, col2 = st.columns(2)
    def card(text:str, value:float, type:str):
        if type == "Deluxe":
            delta = value - np.mean(Deluxe)
        elif type == "Standard":
            delta = value - np.mean(Standard)
        
        if delta != 0:
            delta_color="inverse"
        else:
            delta_color="off"
        st.metric(label=text, value=value, delta=delta,delta_color=delta_color)
        #col3.metric(label="No Change", value=5000, delta=0)
        style_metric_cards(background_color="#12161e",border_color="#6c86b6")
    with col1:
        card(text="标准版近期价格（RMB）", value=Standard[-1], type="Standard")
    with col2:
        card(text="豪华版近期价格（RMB）", value=Deluxe[-1], type="Deluxe")
    data = {
        "date": Date,
        "豪华版本": Deluxe,
        "标准版本": Standard
    }

    df = pd.DataFrame(data)

    df['date'] = pd.to_datetime(df['date'], format='%Y/%m-%d')

    df.set_index('date', inplace=True)

    st.line_chart(df)