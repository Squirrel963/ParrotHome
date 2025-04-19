#import http
import streamlit as st
#from streamlit_elements import elements, mui, html
from streamlit_geolocation import streamlit_geolocation
from streamlit_tags import st_tags
#import streamlit_extras
from streamlit_card import card
import json
import requests
# import socket
# import ssl
import pandas as pd
import random
from datetime import datetime
import UPDATECHECK
requests.packages.urllib3.disable_warnings()
def get_data_from_api(api_url):  
    # 发送GET请求  
    response = requests.get(api_url)  
    data = response.json()  
    return data

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(
    smtp_server: str,
    smtp_port: int,
    sender_email: str,
    receiver_email: str,
    subject: str,
    body: str,
    sender_password: str,
    use_tls: bool = True
):
    """
    使用 SMTP 协议发送邮件
    
    参数:
        smtp_server: SMTP 服务器地址
        smtp_port: SMTP 服务器端口
        sender_email: 发件人邮箱地址
        receiver_email: 收件人邮箱地址
        subject: 邮件主题
        body: 邮件正文
        sender_password: 发件人邮箱密码
        use_tls: 是否使用 TLS 加密
    
    返回:
        str: 成功返回 'success'，失败返回错误信息
    """
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))
    
        if use_tls:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
        else:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return 'success'
    except Exception as e:
        return str(e)

ver = '20250419_P0520'

api_key = st.secrets["weather"]["api_key"]

st.set_page_config(
    page_title="Parrot导航页",
    page_icon="🦜",
    layout="wide",
    initial_sidebar_state="auto",
)

caches = ['weatherloaded','weather','weather_helper','location','uplog','randkey','sent']
for i in caches:
    if i not in st.session_state:
        st.session_state[i] = False

if not st.session_state['randkey']:
    st.session_state['randkey'] = random.randint(1000000,9999999)

# def check_ssl_status(shostname:str, port=443):
#     """
#     检查指定主机的SSL证书状态

#     参数：
#     hostname (str): 要检查的主机名
#     port (int): 要检查的端口，默认是443

#     返回：
#     str: 表示SSL证书状态的字符串，可能的值包括：
#          - "SSL证书正常"
#          - "SSL证书已过期"
#          - "SSL证书无效"
#          - "连接超时"
#     """
#     context = ssl.create_default_context()
#     conn = None
#     status = "ssSSL证书无效"
#     hostname = socket.gethostbyname(shostname.replace("/","").replace("https:","").replace("http:",""))
#     st.write(hostname)

#     try:
#         conn = context.wrap_socket(
#             socket.socket(socket.AF_INET),
#             server_hostname=hostname,
#         )
#         conn.settimeout(3.0)
#         conn.connect((hostname, port))
#         cert = conn.getpeercert()

#         # 获取SSL证书到期时间
#         expiry_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')

#         # 检查SSL证书是否过期
#         if expiry_date < datetime.now():
#             status = "SSL证书已过期"
#         else:
#             status = "SSL证书正常"

#     except ssl.SSLError as e:
#         status = "SSL证书无效SSLError"
#     except socket.timeout:
#         status = "站点连接超时"
#     except Exception as e:
#         status = f"SSL证书无效{e}"
#     finally:
#         if conn:
#             conn.close()

#     return status

@st.dialog("发生错误！")
def vote(text:str):
    st.error(f"加载文件时出现问题，请联系网站管理员")
    st.write(f"错误：{text}")

@st.dialog("感谢推荐！")
def share():
    st.balloons()
    st.write("地址：")
    st.code(f"https://parrothome.streamlit.app/")
    st.download_button(
        label="下载地址文本",
        data='''地址：https://parrothome.streamlit.app/
欢迎常来！''',
        file_name="Parrot导航页地址.txt",
        on_click="ignore",
        type="primary",
        icon=":material/download:",
    )

@st.dialog("发送邮件")
def sent_mail(uri:str, infomation:str, sent_type:str):
    if sent_type == "contribute":
        if '.' in uri:
            st.write(f"您准备投稿的地址是{uri}")
            owner = st.toggle("将站点置于友链")
            if owner:
                with st.container(border=True):
                    emails = st.text_input("发送该内容需要您提供您的电子邮件地址",help="您的电子邮箱用于后续审核处理，不会被恶意滥用及泄露")
                    if emails != "" and "@" in emails:
                        if st.button(":material/vpn_key: 发送验证邮件"):
                            with st.spinner("正在发送邮件...请稍等"):
                                asucc = send_email(smtp_server="smtp.163.com",
                                        smtp_port=465,
                                        sender_email=st.secrets["mail"]["email"],
                                        receiver_email=emails,
                                        subject="PH邮箱身份验证",
                                        sender_password=st.secrets["mail"]["imap"],
                                        body=f'''您正在PH上投稿一个友链，如果这不是您本人所为，请忽略本邮件。请填入该验证码以继续操作：{st.session_state['randkey']}''',
                                        use_tls=False)
                                if asucc == "success":
                                    st.session_state['sent'] = emails
                key_code = st.text_input("您收到的数字验证码")
            if st.button(":material/send: 发送"):
                if owner:
                    if key_code == st.session_state['randkey']:
                        with st.spinner("正在发送邮件...请稍等"):
                            asucc = send_email(smtp_server="smtp.163.com",
                                    smtp_port=465,
                                    sender_email=st.secrets["mail"]["email"],
                                    receiver_email=st.secrets["mail"]["target"],
                                    subject="PH网站收录",
                                    sender_password=st.secrets["mail"]["imap"],
                                    body=f"网址：{uri}，简介：{infomation}",
                                    use_tls=False)
                        if asucc == "success":
                            st.success("发送成功！")
                        else:
                            st.warning(f"邮件发送失败！")
                    else:
                        st.error("验证码错误！")
                else:
                    with st.spinner("正在发送邮件...请稍等"):
                        asucc = send_email(smtp_server="smtp.163.com",
                                    smtp_port=465,
                                    sender_email=st.secrets["mail"]["email"],
                                    receiver_email=st.secrets["mail"]["target"],
                                    subject="PH网站收录",
                                    sender_password=st.secrets["mail"]["imap"],
                                    body=f"网址：{uri}，简介：{infomation}",
                                    use_tls=False)
                    if asucc == "success":
                        st.success("发送成功！")
                    else:
                        st.warning(f"邮件发送失败！")
        else:
            st.write("您填写的网址看起来不像一个真正的网址")
    elif sent_type == "report":
        with st.container(border=True):
            emails = st.text_input("发送该内容需要您提供您的电子邮件地址",help="您的电子邮箱用于后续处理状态追踪订阅，不会被恶意滥用及泄露")
            if emails != "" and "@" in emails:
                if st.button(":material/vpn_key: 发送验证邮件"):
                    with st.spinner("正在发送邮件...请稍等"):
                        asucc = send_email(smtp_server="smtp.163.com",
                                smtp_port=465,
                                sender_email=st.secrets["mail"]["email"],
                                receiver_email=emails,
                                subject="PH邮箱身份验证",
                                sender_password=st.secrets["mail"]["imap"],
                                body=f'''您正在PH上汇报一个问题，如果这不是您本人所为，请忽略本邮件。请填入该验证码以继续操作：{st.session_state['randkey']}''',
                                use_tls=False)
                        if asucc == "success":
                            st.session_state['sent'] = emails
        key_code = st.text_input("您收到的数字验证码")
        if st.button(":material/send: 发送"):
            if key_code == f"{st.session_state['randkey']}":
                with st.spinner("正在发送邮件...请稍等"):
                    asucc = send_email(smtp_server="smtp.163.com",
                            smtp_port=465,
                            sender_email=st.secrets["mail"]["email"],
                            receiver_email=st.secrets["mail"]["target"],
                            subject="PH网站问题反馈",
                            sender_password=st.secrets["mail"]["imap"],
                            body=f"{uri}，追踪邮箱：{st.session_state['sent']}，问题：'{infomation}'",
                            use_tls=False)
                if asucc == "success":
                    st.success("发送成功！")
                    st.session_state['randkey'] = random.randint(1000000,9999999)
                else:
                    st.warning(f"邮件发送失败！")
            else:
                st.error("验证码错误！")

# @st.dialog("确认跳转")
# def jump(url:str):
#     with st.spinner("检查目标站点中..."):
#         state = check_ssl_status(url)
#         st.write(state)

st.title("Parrot 导航页")
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    ":material/search: 搜索引擎", 
    ":material/layers: 资讯卡片", 
    ":material/widgets: 实用工具", 
    ":material/near_me: 网站收录", 
    ":material/local_cafe: 友情链接", 
    ":material/check: 帮助改进", 
    ":material/share: 关于本站"])

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

browz_tools = {
    "Edge" :{
        "关于Microsoft Edge": "edge://about",
        "无障碍功能设置": "edge://accessibility",
        "应用服务内部信息": "edge://app-service-internals",
        "应用防护内部信息": "edge://application-guard-internals",
        "应用管理": "edge://apps",
        "归因内部信息": "edge://attribution-internals",
        "自动填充内部信息": "edge://autofill-internals",
        "Blob内部信息": "edge://blob-internals",
        "蓝牙内部信息": "edge://bluetooth-internals",
        "浏览器必备功能": "edge://browser-essentials",
        "浏览器必备功能（顶部Chrome）": "edge://browser-essentials.top-chrome",
        "商业内部信息": "edge://commerce-internals",
        "兼容性信息": "edge://compat",
        "组件更新": "edge://components",
        "冲突检测": "edge://conflicts",
        "连接器内部信息": "edge://connectors-internals",
        "崩溃报告": "edge://crashes",
        "致谢": "edge://credits",
        "数据查看器": "edge://data-viewer",
        "设备日志": "edge://device-log",
        "页面丢弃": "edge://discards",
        "下载内部信息": "edge://download-internals",
        "下载管理": "edge://downloads",
        "数据丢失防护内部信息": "edge://edge-dlp-internals",
        "Edge URL列表": "edge://edge-urls",
        "增强型网络防护": "edge://enp",
        "扩展程序": "edge://extensions",
        "扩展程序内部信息": "edge://extensions-internals",
        "收藏夹": "edge://favorites",
        "实验性功能": "edge://flags",
        "图形处理单元信息": "edge://gpu",
        "帮助": "edge://help",
        "直方图数据": "edge://histograms",
        "历史记录": "edge://history",
        "历史记录聚类内部信息": "edge://history-clusters-internals",
        "索引数据库内部信息": "edge://indexeddb-internals",
        "开发者工具": "edge://inspect",
        "拦截页面": "edge://interstitials",
        "启动来源": "edge://launch-source",
        "本地状态": "edge://local-state",
        "管理应用": "edge://mam-internals",
        "管理控制台": "edge://management",
        "媒体参与度": "edge://media-engagement",
        "媒体内部信息": "edge://media-internals",
        "指标内部信息": "edge://metrics-internals",
        "模块管理": "edge://modules",
        "网络导出": "edge://net-export",
        "网络内部信息": "edge://net-internals",
        "网络错误": "edge://network-errors",
        "新标签页": "edge://newtab",
        "新标签页瓦片内部信息": "edge://ntp-tiles-internals",
        "地址栏": "edge://omnibox",
        "设备内部信息": "edge://on-device-internals",
        "优化指南内部信息": "edge://optimization-guide-internals",
        "密码管理器内部信息": "edge://password-manager-internals",
        "策略设置": "edge://policy",
        "首次运行前置体验": "edge://pre-launch-fre",
        "预测服务": "edge://predictors",
        "偏好设置内部信息": "edge://prefs-internals",
        "打印": "edge://print",
        "私有聚合内部信息": "edge://private-aggregation-internals",
        "进程内部信息": "edge://process-internals",
        "个人资料内部信息": "edge://profile-internals",
        "推送通知内部信息": "edge://push-internals",
        "配额内部信息": "edge://quota-internals",
        "沙盒环境": "edge://sandbox",
        "安全诊断": "edge://security-diagnostics",
        "服务工作线程内部信息": "edge://serviceworker-internals",
        "设置": "edge://settings",
        "登录内部信息": "edge://signin-internals",
        "网站参与度": "edge://site-engagement",
        "同步内部信息": "edge://sync-internals",
        "系统信息": "edge://system",
        "标签页搜索（顶部Chrome）": "edge://tab-search.top-chrome",
        "服务条款": "edge://terms",
        "主题内部信息": "edge://topics-internals",
        "性能追踪": "edge://tracing",
        "翻译内部信息": "edge://translate-internals",
        "使用体验改进计划": "edge://ukm",
        "USB内部信息": "edge://usb-internals",
        "用户操作": "edge://user-actions",
        "版本信息": "edge://version",
        "电子钱包": "edge://wallet",
        "电子钱包密码管理": "edge://wallet/passwords",
        "网络应用内部信息": "edge://web-app-internals",
        "WebRTC内部信息": "edge://webrtc-internals",
        "WebRTC日志": "edge://webrtc-logs",
        "工作区内部信息": "edge://workspaces-internals"
    },
    "chrome(内核)" :{
        "打开新标签页": "chrome://newtab",
        "打开浏览器设置": "chrome://settings",
        "查看实验性功能": "chrome://flags",
        "管理扩展程序": "chrome://extensions",
        "查看历史记录": "chrome://history",
        "查看下载列表": "chrome://downloads",
        "管理书签": "chrome://bookmarks",
        "查看所有打开的标签页": "chrome://tabs",
        "查看隐私设置": "chrome://privacy",
        "查看安全信息": "chrome://certificateviewer",
        "打开任务管理器": "chrome://task-manager",
        "查看内存使用情况": "chrome://memory",
        "调试移动设备上的网页": "chrome://inspect",
        "性能分析工具": "chrome://tracing",
        "查看浏览器使用统计数据": "chrome://stats",
        "查看浏览器版本信息": "chrome://about",
        "查看和更新浏览器组件": "chrome://components",
        "查看网络事件信息": "chrome://net-internals",
        "查看网页翻译设置": "chrome://translate-internals",
        "显示下载的媒体文件": "chrome://media-engagement",
        "查看浏览器的同步状态": "chrome://sync",
        "查看浏览器的痕迹": "chrome://net-export",
        "查看浏览器的权限设置": "chrome://site-settings",
        "查看浏览器的无障碍设置": "chrome://accessibility",
        "查看浏览器的字体设置": "chrome://settings/fonts",
        "查看浏览器的下载位置设置": "chrome://settings/downloads"
    },
    "Firefox" :{
        "打开新标签页": "about:newtab",
        "打开浏览器设置": "about:preferences",
        "查看隐私设置": "about:preferences#privacy",
        "查看网络请求信息": "about:networking",
        "查看浏览器配置": "about:config",
        "查看扩展信息": "about:addons",
        "查看历史记录": "about:history",
        "查看下载列表": "about:downloads",
        "查看内存使用情况": "about:memory",
        "查看性能信息": "about:performance",
        "查看系统信息": "about:system",
        "查看日志": "about:logs",
        "查看证书": "about:certificates"
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
        with st.container(border=True):
            st.caption("搜索结果过滤选项")
            if st.toggle("关注名单",help='搜索引擎将会优先显示包含设置词汇的搜索结果'):
                white_list = st_tags(label='优先词汇',text='按下enter将当前输入转换一个词')
                if len(white_list) != 0:
                    white_list = f" %2B{' %2B'.join(white_list)}"
                else:
                    white_list = ""
            else:
                white_list = ""
            if st.toggle("黑名单",help='搜索引擎将会过滤掉包含设置词汇的搜索结果'):
                black_list = st_tags(label='词汇过滤',text='按下enter将当前输入转换一个词',suggestions=['csdn','京东','淘宝'])
                if len(black_list) != 0:
                    black_list = f" -{' -'.join(black_list)}"
                else:
                    black_list = ""
            else:
                black_list = ""
            #st.write(black_list)
            #st.write(white_list)
    with col1:
        something = st.text_input("搜索内容").replace(" ",f'{engine_links[engine]["hold"]}').replace("+","%2B")
        cantserc = False
        if tans[mode] in engine_links[engine]:
            link = f"{engine_links[engine][tans[mode]]}{something}{engine_links[engine]['hold']}{white_list}{black_list}"
        else:
            link = "None"
            cantserc = True
            col2.error("当前搜索引擎不支持搜索该项目")
        #st.write(link)
        if white_list != "" or black_list != "":
            if engine in ['360搜索','搜狗','百度']:
                col2.warning("当前搜索引擎不支持相关功能，过滤器将不会完全生效")
        if something == "":
            cantserc = True
        sercol1, sercol2 = st.columns([0.35, 0.65])
        with sercol1:
            st.link_button(f":material/launch: 立即搜索：{engine}", f"{link}",disabled=cantserc)
        with sercol2:
            with st.expander(":material/build: 浏览器工具箱"):
                brow_map = {
                    0: "Edge",
                    1: "chrome(内核)",
                    2: "Firefox",
                }
                brow = st.segmented_control(
                    "Tool",label_visibility='collapsed',
                    options=brow_map.keys(),
                    format_func=lambda option: brow_map[option],
                    selection_mode="single",
                )
                if not brow == None:
                    brow_tool = st.selectbox("s",label_visibility='collapsed',options=browz_tools[brow_map[brow]])
                    st.code(browz_tools[brow_map[brow]][brow_tool])
    
def wearther_sogs(name ,brief, details):
    with st.expander(f"{name}：{brief}"):
        st.write(details)

with tab2:
    info1, info2 = st.columns(2)
    with info1:
        with st.container(border=True):
            loc1, loc2 = st.columns([0.1,0.9])
            with st.spinner("正在获取数据..."):
                if not st.session_state['weatherloaded']:
                    with loc1:
                        earth_location = streamlit_geolocation()
                    with loc2:
                        st.text("点按左侧按钮以允许PH获取您的位置信息")
                    location = f'{earth_location["latitude"]}:{earth_location["longitude"]}'
                    st.session_state['location'] = earth_location
                else:
                    st.write(":material/gps_fixed: 已获取您的位置信息")
                #location = get_data_from_api(f"https://api.seniverse.com/v3/location/search.json?key={api_key}&q={earth_location}")["results"][0]['id']
                if not st.session_state['weatherloaded']:
                    try:
                        start_get = datetime.now()
                        weather = get_data_from_api(f"https://api.seniverse.com/v3/weather/now.json?key={api_key}&location={location}&language=zh-Hans&unit=c")["results"][0]
                        weather_helper = get_data_from_api(f"https://api.seniverse.com/v3/life/suggestion.json?key={api_key}&location={location}&language=zh-Hans&days=1")["results"][0]["suggestion"][0]
                        badguy = ['date','sport','air_pollution','dressing','beer','morning_sport','shopping']
                        for i in badguy:
                            try:
                                weather_helper.pop(i)
                            except:
                                pass
                        end_get = datetime.now()
                        times = end_get - start_get
                        st.write(f"本次数据获取耗时：{times.total_seconds()}s")
                        st.session_state['weatherloaded'] = True
                        st.session_state['weather'] = weather
                        st.session_state['weather_helper'] = weather_helper
                    except:
                        st.write(":material/gps_off: 未获取位置信息")
        if st.session_state['weatherloaded']:
            with st.container(border=True):
                try:
                    st.header(f"{weather_code[int(st.session_state['weather']['now']['code'])]} {st.session_state['weather']['now']['text']}     {st.session_state['weather']['now']['temperature']}℃")
                except:
                    st.header(f"{st.session_state['weather']['now']['text']}     {st.session_state['weather']['now']['temperature']}℃")
                st.subheader(f":material/room: {st.session_state['weather']['location']['path']}")
                st.caption(f'最后更新：{st.session_state["weather"]["last_update"].replace("T", " ")} （数据来自"心知天气"）')
        if st.session_state['weatherloaded']:
            with st.container(border=True):
                st.map(data={'lat': [st.session_state['location']["latitude"]], 'lon': [st.session_state['location']["longitude"]]}, zoom=10, height=300)
                st.subheader("您的位置信息")
                st.markdown(f'''纬度：{st.session_state['location']["latitude"]}  
经度：{st.session_state['location']["longitude"]}''')
        if st.session_state['weatherloaded']:
            chart_data = pd.DataFrame(
                {
                    "col1": [1,2,3,4],
                    "col2": [2,3,4,5],
                    "col3": None,
                }
            )

            #st.line_chart(chart_data, x="col1", y="col2", color="col3")
    with info2:
        if st.session_state['weatherloaded']:
            for sogs in sorted(st.session_state['weather_helper'].keys()):
                wearther_sogs(suggestion_tans[sogs], st.session_state['weather_helper'][sogs]['brief'], st.session_state['weather_helper'][sogs]['details'])
                #time.sleep(0.05)
    #st.write(weather)

with tab3:
    st.write("敬请期待")

with tab4:
    with st.spinner("加载中..."):
        didnt_error = False
        try:
            with open('websites.json', 'r', encoding='utf-8') as file:
                websites = json.load(file)
            didnt_error = True
        except Exception as e:
            websites = {
                ':material/warning: 网站错误': {
                    'url': 'error',
                    'description': f'{e}'
                }
            }
    serch = st.text_input(":material/search: 搜索", placeholder='搜索网址名称或简介', label_visibility='collapsed')
    with st.popover("显示设置"):
        beautiful = st.toggle("整齐排版", value=didnt_error,help='通过相关处理来使总体卡片整齐排列；如果开启后无法找到需要内容，可关闭此选项或使用搜索')
        security = st.toggle("http加密显示", value=True,help='显示目标页面所使用的http连接是否加密')
    if beautiful:
        showmode = "top"
    else:
        showmode = "center"
    def webshows(name, description, uri:str, serchmode:bool):
        with st.container(border=True):
            http_mode = uri.split("://")[0]
            if not serchmode:
                st.write(f"{name}")
                if security:
                    if http_mode == "https":
                        st.badge(f":material/verified_user: {http_mode}",color='green')
                    elif uri == "error":
                        st.badge(f":material/block: 内部问题",color='red')
                    else:
                        st.badge(f":material/error: {http_mode}",color='orange')
                if uri != "error":
                    st.text(description)
            else:
                st.write(f"{name} ：{description}")
                if security:
                    if http_mode == "https":
                        st.badge(f":material/verified_user: {http_mode}",color='green')
                    elif uri == "error":
                        st.badge(f":material/block: 内部问题",color='red')
                    else:
                        st.badge(f":material/error: {http_mode}",color='orange')
            if uri != "error":
                st.link_button(":material/launch: 前往",url=uri)
            else:
                if st.button(":material/launch: 前往"):
                    vote(description)
    webli1, webli2, webli3, webli4 = st.columns(4,vertical_alignment=showmode)
    #with webli1:
    if bool(serch):
        more_width = 100
    else:
        more_width = 0
    width = (len(websites) // 4) + int(not beautiful) + more_width
    i = 1
    serch_mode = bool(serch)
    for website_name in sorted(websites.keys()):
        if serch.lower() in website_name.lower() or serch == "" or serch.lower() in websites[website_name]['description'].lower():
            if i <= width:
                with webli1:
                    webshows(website_name,websites[website_name]['description'],websites[website_name]['url'],serch_mode)
            elif i <= width*2:
                with webli2:
                    webshows(website_name,websites[website_name]['description'],websites[website_name]['url'],serch_mode)
            elif i <= width*3:
                with webli3:
                    webshows(website_name,websites[website_name]['description'],websites[website_name]['url'],serch_mode)
            elif i <= width*4:
                with webli4:
                    webshows(website_name,websites[website_name]['description'],websites[website_name]['url'],serch_mode)
        i += 1

with tab5:
    with st.spinner("加载中..."):
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

with tab6:
    with st.container(border=True):
        st.caption(":material/move_to_inbox: 网站收录内容")
        uul_url = st.text_input("网址",placeholder='必填')
        uul_des = st.text_input("简介",placeholder='选填')
        button, rule = st.columns([0.2,0.8], gap="large")
        with button:
            if st.button(":material/how_to_vote: 发送投稿邮件", disabled=(uul_url=="")):
                sent_mail(uri=uul_url, infomation=uul_des, sent_type="contribute")
        with rule:
            with st.popover(label=":material/report: 投稿要求",use_container_width=True):
                with st.expander("《互联网信息服务管理办法》第十五条"):
                    st.markdown('''互联网信息服务提供都不得制作、复制、发布、传播含有下列内容的信息：  
1、 反对宪法所确定的基本原则的  
2、 危害国家安全，泄露国家秘密，颠覆国家政权，破坏国家统一的  
3、 损害国家荣誉和利益的  
4、 煽动民族仇恨、民族歧视，破坏民族团结的  
5、 破坏国家宗教政策，宣扬邪教和封建迷信的  
6、 散布谣言，扰乱社会秩序，破坏社会稳定的  
7、 散布淫秽、色情、赌博、暴力、凶杀、恐怖或者教唆犯罪的  
8、 侮辱或者诽谤他人，侵害他人合法权益的  
9、 含有法律、行政法规禁止的其他内容的''')
                with st.expander("《PH网址投稿规定》"):
                    st.markdown('''1、 站点页面不得包含、插入恶意代码  
2、 站点不得包含大量盈利内容  
3、 站点不采用ip地址直连''')
        #st.link_button(":material/how_to_vote: 发送投稿邮件",url=f"mailto:wycc_wycserver@163.com?subject=PH网站收录&body=网址：{uul_url}  简介：{uul_des}", disabled=(uul_url==""))
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
            if st.button(":material/email: 发送邮件", disabled=(report_url=="")):
                sent_mail(uri={report_types}, infomation=f"板块：{report_plate}，地址：{report_url}", sent_type="report")
            #st.link_button(":material/email: 发送邮件",url=f"mailto:wycc_wycserver@163.com?subject=PH建议：{report_types}&body=板块：{report_plate}  地址：{report_url}  详细信息：{report_text}", disabled=(report_url==""))
        else:
            report_text = st.text_area("详细信息",help='''不知道填什么？ 可填写某功能出现的异常现象或你需要的新功能或对已有的功能提出建议''',placeholder='必填')
            if st.button(":material/email: 发送邮件", disabled=(report_text=="")):
                sent_mail(uri={report_types}, infomation=f"{report_text}", sent_type="report")
            #st.link_button(":material/email: 发送邮件",url=f"mailto:wycc_wycserver@163.com?subject=PH建议：{report_types}&body=详细信息：{report_text}", disabled=(report_text==""))

with tab7:
    start_time = datetime(2025, 4, 11, 13, 20, 5)
    end_time = datetime.now()
    time_diff = end_time - start_time
    diff_days = time_diff.days
    diff_seconds = time_diff.seconds
    diff_hours = diff_seconds // 3600
    diff_minutes = (diff_seconds % 3600) // 60
    st.subheader(" 关于 Parrot Home")
    infocol1, infocol2 = st.columns([0.7, 0.3])
    with infocol1:
        with st.container(border=True):
            st.markdown('''##### 概述
本站是由streamlit编写的导航页面，旨在提供公益导航服务  
包含多搜索引擎跳转、网址合集、资讯卡片等''')
        with st.container(border=True):
            st.markdown(f'''##### 运营
负责人&站长：wycc  
托管账户提供者：squirrel963（github）  
运行：本站点托管于streamlit社区云  
总服务时长：{diff_days}d {diff_hours}h {diff_minutes}min  
内部版本：{ver}  
开源许可证：GPL-3.0''')
        with st.container(border=True):
            st.markdown('''##### 免责声明
本站点仅提供第三方网页跳转服务  
本身不存储任何用户数据及服务用数据  
数据均来自第三方，与本站无关''')
        if st.button(":material/share: 分享该站点！",use_container_width=True):
            share()
    with infocol2:
        with st.container(border=True):
            st.markdown("##### 更新日志")
            if not st.session_state['uplog']:
                if st.button("加载数据"):
                    with st.spinner("获取数据中..."):
                        st.session_state['uplog'] = UPDATECHECK.getlog("https://squirrel963.github.io/parrot_web_database/PH_allinfo/index.md")
                        st.rerun()
            if st.session_state['uplog']:
                log_version = st.selectbox("版本",options=st.session_state['uplog'])
                with st.container(border=True):
                    #st.write(st.session_state['uplog'])
                    for op in st.session_state['uplog'][log_version].split(","):
                        st.write(op)