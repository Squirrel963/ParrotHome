import http
import streamlit as st
from streamlit_elements import elements, mui, html
from streamlit_geolocation import streamlit_geolocation
import streamlit_extras
from streamlit_card import card
import json
import requests
requests.packages.urllib3.disable_warnings()
def get_data_from_api(api_url):  
    # 发送GET请求  
    response = requests.get(api_url)  
    data = response.json()  
    return data

#这个api是免费的，你盗用了也没意义，想用还不如自己注册一个（起码你能光明正大的用），何必提心吊胆地用？--wycc
api_key = "SSLJli7F2PINakHcG"

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

weather_code = {
    0:':sun:',
    1:':crescent_moon:',
    2:':sun:',
    3:':crescent_moon:',
    4:':sun_behind_large_cloud:',
    5:':sun_behind_cloud:',
    6:':sun_behind_cloud:',
    7:':sun_behind_small_cloud:',
    8:':sun_behind_small_cloud:',
    9:':cloud:',
    10:':sun_behind_rain_cloud:',
    11:':cloud_with_lightning_and_rain:',
    31:':fog:'
}

suggestion_tans = {
    'ac':':level_slider: 空调',
    'air_pollution':':dashing_away: 空气污染',
    'airing':':sponge: 晾晒',
    'allergy':':test_tube: 过敏',
    'beer':':beer_mug: 喝啤酒',
    'boating':':canoe: 划船',
    'car_washing':':shower: 洗车',
    'chill':':thermometer: 风寒',
    'comfort':':books: 舒适度',
    'dating':':heart_with_ribbon: 约会',
    'dressing':':t_shirt: 穿衣',
    'fishing':':fish: 钓鱼',
    'flu':':pill: 感冒',
    'kiteflying':':kite: 放风筝',
    'makeup':':lipstick: 化妆',
    'mood':':sunglasses: 心情',
    'morning_sport':':running_shirt: 晨练',
    'road_condition':':taxi: 路况',
    'shopping':':shopping_cart: 购物',
    'sport':':soccer_ball: 运动',
    'sunscreen':':lotion_bottle: 防晒',
    'traffic':':vertical_traffic_light: 交通',
    'travel':':world_map: 旅游',
    'umbrella':':umbrella: 雨伞',
    'uv':':umbrella_on_ground: 紫外线'
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

try:
    with open('friends.json', 'r', encoding='utf-8') as file:
        friends = json.load(file)
except Exception as e:
    friends = {
        '网站错误': {
            'uri': '',
            'des': f'{e}',
            'image': ''
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
    
def wearther_sogs(name ,brief, details):
    with st.expander(f"{name}：{brief}"):
        st.write(details)

with tab2:
    info1, info2 = st.columns(2)
    with info1:
        all_fine = False
        with st.container(border=True):
            loc1, loc2 = st.columns([0.05,0.95])
            with st.spinner("正在获取数据..."):
                with loc1:
                    earth_location = streamlit_geolocation()
                with loc2:
                    st.text("点按左侧按钮以允许PH获取您的位置信息")
                location = f'{earth_location["latitude"]}:{earth_location["longitude"]}'
                #location = get_data_from_api(f"https://api.seniverse.com/v3/location/search.json?key={api_key}&q={earth_location}")["results"][0]['id']
                try:
                    weather = get_data_from_api(f"https://api.seniverse.com/v3/weather/now.json?key={api_key}&location={location}&language=zh-Hans&unit=c")["results"][0]
                    weather_helper = get_data_from_api(f"https://api.seniverse.com/v3/life/suggestion.json?key={api_key}&location={location}&language=zh-Hans&days=1")["results"][0]["suggestion"][0]
                    badguy = ['date','sport','air_pollution','dressing','beer','morning_sport','shopping']
                    for i in badguy:
                        try:
                            weather_helper.pop(i)
                        except:
                            pass
                    all_fine = True
                except:
                    st.write(":material/gps_off: 未获取位置信息")
        if all_fine:
            with st.container(border=True):
                try:
                    st.header(f"{weather_code[int(weather['now']['code'])]} {weather['now']['text']}     {weather['now']['temperature']}℃")
                except:
                    st.header(f"{weather['now']['text']}     {weather['now']['temperature']}℃")
                st.subheader(f":material/room: {weather['location']['path']}")
                st.caption(f'最后更新：{weather["last_update"].replace("T", " ")} （数据来自"心知天气"）')
        if all_fine:
            for sogs in sorted(weather_helper.keys()):
                wearther_sogs(suggestion_tans[sogs], weather_helper[sogs]['brief'], weather_helper[sogs]['details'])

    with info2:
        if all_fine:
            with st.container(border=True):
                st.map(data={'lat': [earth_location["latitude"]], 'lon': [earth_location["longitude"]]}, zoom=10)
            with st.container(border=True):
                st.subheader("您的位置信息")
                st.markdown(f'''维度：{earth_location["latitude"]}  
经度：{earth_location["longitude"]}''')
    #st.write(weather)

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
    li1, li2, li3, li4 = st.columns(4)
    def yqshows(name, description, uri, imag):
        card(
            title=name,
            text=description,
            image=imag,
            url=uri,
        )
    jwidth = (len(friends) // 4) + 1
    j = 1
    for friends_name in friends.keys():
        if j <= jwidth:
            with li1:
                yqshows(friends_name, friends[friends_name]['des'], friends[friends_name]['uri'], friends[friends_name]['image'])
        elif j <= jwidth*2:
            with li2:
                yqshows(friends_name, friends[friends_name]['des'], friends[friends_name]['uri'], friends[friends_name]['image'])
        elif j <= jwidth*3:
            with li3:
                yqshows(friends_name, friends[friends_name]['des'], friends[friends_name]['uri'], friends[friends_name]['image'])
        elif j <= jwidth*4:
            with li4:
                yqshows(friends_name, friends[friends_name]['des'], friends[friends_name]['uri'], friends[friends_name]['image'])
        j += 1

with tab5:
    with st.container(border=True):
        st.caption(":material/move_to_inbox: 网站收录内容")
        uul_url = st.text_input("网址",placeholder='必填')
        uul_des = st.text_input("简介",placeholder='选填')
        st.link_button(":material/how_to_vote: 发送投稿邮件",url=f"mailto:wycc_wycserver@163.com?subject=PH网站收录&body=网址：{uul_url}  简介：{uul_des}", disabled=(uul_url==""))
    with st.container(border=True):
        st.caption(":material/flag: 站点问题反馈")
        report_types = st.selectbox("类型", [
            'Bug(漏洞，使用问题)',
            '功能建议(新增，修改)',
            '内容问题(侵权，不适宜内容)'

        ])
        if report_types == '内容问题(侵权，不适宜内容)':
            report_plate = st.selectbox("板块",['网站收录','友链'])
            report_url = st.text_input("目标地址",placeholder='必填')
        if report_types == '内容问题(侵权，不适宜内容)':
            report_text = st.text_area("详细信息",help='''不知道填什么？ 可填写目标收录网站的违规行为''',placeholder='选填')
            st.link_button(":material/email: 发送邮件",url=f"mailto:wycc_wycserver@163.com?subject=PH建议：{report_types}&body=板块：{report_plate}  地址：{report_url}  详细信息：{report_text}", disabled=(report_url==""))
        else:
            report_text = st.text_area("详细信息",help='''不知道填什么？ 可填写某功能出现的异常现象''',placeholder='必填')
            st.link_button(":material/email: 发送邮件",url=f"mailto:wycc_wycserver@163.com?subject=PH建议：{report_types}&body=详细信息：{report_text}", disabled=(report_text==""))

with tab6:
    st.subheader(" 关于Parrot Home")
    with st.container(border=True):
        st.markdown('''##### 概述
本站是由streamlit编写的导航页面，旨在提供公益导航服务  
包含多搜索引擎跳转、网址合集、资讯卡片等''')
    with st.container(border=True):
        st.markdown('''##### 运营
负责人&站长：wycc  
托管账户提供者：squirrel963（github）  
运行：本站点托管于streamlit社区云  
开源许可证：GPL-3.0''')
    with st.container(border=True):
        st.markdown('''##### 免责声明
本站点仅提供第三方网页跳转服务  
本身不存储任何用户数据及服务用数据  
数据均来自第三方，与本站无关''')
