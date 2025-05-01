import streamlit as st

st.set_page_config(page_icon="🦜", layout="wide", page_title="PH - QQ空间跳转器")

st.sidebar.page_link("PWUI.py", label="返回主页", icon=":material/home:",use_container_width=True)

st.title("QQ空间跳转器")
qq = st.text_input("QQ号", help="在此填入要查看的QQ空间的QQ号")

with st.container(border=True):
    option_map = {
        ":material/mode_comment: 主页" : "main",
        ":material/insert_photo: 相册" : "photo",
        ":material/note: 留言板" : "334",
        ":material/forum: 说说" : "311",
        ":material/person: 个人档" : "1",
        ":material/queue_music: 音乐" : "305",
        ":material/star: 收藏" : "favorite",
    }
    selection = st.pills(
        "Tool",label_visibility='collapsed',
        options=option_map.keys(),
        selection_mode="single",
    )

if not selection == None and not qq == "":
    st.link_button(label=":material/call_made: 立即跳转",url=f"https://user.qzone.qq.com/{qq}/{option_map[selection]}",use_container_width=True,type='primary')
elif qq == "":
    st.link_button(label=":material/call_made: 立即跳转",url="",use_container_width=True,type='primary',disabled=True,help="请输入目标QQ号")
elif selection == None:
    st.link_button(label=":material/call_made: 立即跳转",url="",use_container_width=True,type='primary',disabled=True,help="请选择一项板块")
