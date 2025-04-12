import http
import streamlit as st
from streamlit_elements import elements, mui, html
import streamlit_extras
from streamlit_card import card
import json

version = "1.41"

st.set_page_config(
    page_title="Parrot导航页",
    page_icon="🦜",
    layout="wide",
    initial_sidebar_state="auto",
)

@st.dialog("发生错误！")
def vote(text:str):
    st.error(f"加载文件时出现问题，请联系网站管理员")
    st.write(f"错误：{text}")

st.title("Parrot 导航页")
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([":material/search: 搜索引擎", ":material/layers: 资讯卡片", ":material/near_me: 网站收录", ":material/local_cafe: 友情链接", ":material/check: 帮助改进", ":material/share: 关于本站"])

engine_links = {
    'Bing':{'text':"https://cn.bing.com/search?q=",
            'image':"https://cn.bing.com/images/search?q=",
            'video':"https://cn.bing.com/videos/search?q=",
            'hold':"%20"},
    '百度':{'text':"https://www.baidu.com/s?wd=",
          'image':"https://image.baidu.com/search/index?tn=baiduimage&word=",
          'video':"https://www.baidu.com/sf/vsearch?pd=video&wd=",
          'hold':"%20"},
    '360搜索':{'text':"https://www.so.com/s?q=",
            'image':"https://image.so.com/ai/s?q=",
            'video':"https://tv.360kan.com/s?q=",
            'hold':"%20"},
    '搜狗':{'text':"https://www.sogou.com/web?query=",
          'image':"https://pic.sogou.com/pics?query=",
          'video':"https://v.sogou.com/v?query=",
          'hold':"%20"},
    'yandex':{'text':"https://yandex.com/search/?text=",
            'hold':"%20"}
}

tans = {
    ":material/explore: 默认":"text",
    ":material/wallpaper: 图片":"image",
    ":material/movie: 视频":"video"
}

try:
    with open('websites.json', 'r', encoding='utf-8') as file:
        websites = json.load(file)
except Exception as e:
    websites = {
        ':material/warning: 网站错误': {
            'url': '',
            'description': f'{e}'
        }
    }

with tab1:
    col1, col2 = st.columns([0.6, 0.4])
    with col2:
        with st.container(border=True):
            engine = st.selectbox(":material/web: 搜索引擎",['Bing','百度','360搜索','搜狗','yandex'])
            mode = st.radio(
                ":material/description: 搜索项目",
                [":material/explore: 默认", ":material/wallpaper: 图片", ":material/movie: 视频"],
            )
    with col1:
        something = st.text_input("搜索内容").replace(" ",f'{engine_links[engine]["hold"]}').replace("+","%2B")
        cantserc = False
        if tans[mode] in engine_links[engine]:
            link = f"{engine_links[engine][tans[mode]]}{something}"
        else:
            link = "None"
            cantserc = True
            col2.warning("当前搜索引擎不支持搜索该项目")
        #st.write(link)
        st.link_button(f":material/launch: 立即搜索：{engine}", f"{link}",disabled=cantserc)
    
with tab2:
    st.write("敬请期待。。。")

with tab3:
    serch = st.text_input("搜索")
    def webshows(name, description, uri):
        with st.container(border=True):
            st.write(f"{name}")
            st.text(description)
            st.link_button(":material/launch: 前往",url=uri)
    webli1, webli2, webli3, webli4 = st.columns(4)
    #with webli1:
    width = (len(websites) // 4) + 1
    i = 1
    with st.spinner("加载中..."):
        for website_name in sorted(websites.keys()):
            if serch.lower() in website_name.lower() or serch == "" or serch.lower() in websites[website_name]['description'].lower():
                if i <= width:
                    with webli1:
                        webshows(website_name,websites[website_name]['description'],websites[website_name]['url'])
                elif i <= width*2:
                    with webli2:
                        webshows(website_name,websites[website_name]['description'],websites[website_name]['url'])
                elif i <= width*3:
                    with webli3:
                        webshows(website_name,websites[website_name]['description'],websites[website_name]['url'])
                elif i <= width*4:
                    with webli4:
                        webshows(website_name,websites[website_name]['description'],websites[website_name]['url'])
            i += 1
with tab4:
    friends = {
        'SAR网盘':{
            'uri':"https://frp-any.top:32998",
            'des':"纯公益不限速云盘"
        },
        'ParrotOCE':{
            'uri':"https://parrotoce.streamlit.app",
            'des':"在线python环境"
        }
    }
    li1, li2, li3, li4 = st.columns(4)
    def yqshows(name, description, uri):
        card(
            title=name,
            text=description,
            image="",
            url=uri,
        )
    with li1:
        for friends_name in sorted(friends.keys()):
            yqshows(friends_name, friends[friends_name]['des'], friends[friends_name]['uri'])

with tab5:
    st.write(f"敬请期待...")

with tab6:
    st.subheader(" 关于Parrot Home")
    with st.container(border=True):
        st.markdown('''##### 概述
本站是由streamlit编写的导航页面，旨在提供公益导航服务  
包含多搜索引擎跳转、网址合集、资讯卡片等''')
    with st.container(border=True):
        st.markdown('''##### 运营
运行：本站点托管于streamlit社区云  
开源许可证：GPL-3.0''')
    with st.container(border=True):
        st.markdown('''##### 免责声明
本站点仅提供第三方网页跳转服务  
本身不存储任何用户数据及服务用数据  
数据均来自第三方，与本站无关''')