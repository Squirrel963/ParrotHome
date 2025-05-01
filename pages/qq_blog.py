import streamlit as st
import streamlit_antd_components as sac

st.set_page_config(page_icon="🦜", layout="wide", page_title="PH - QQ空间跳转器")

st.sidebar.page_link("PWUI.py", label="返回主页", icon=":material/home:",use_container_width=True)

st.title("QQ空间跳转器")
qq = st.text_input("QQ号", help="在此填入要查看的QQ空间的QQ号")

option_map = {
        "主页" : "main",#:material/mode_comment:
        "相册" : "photo",#:material/insert_photo:
        "留言板" : "334",#:material/note: 
        "说说" : "311",#:material/forum:
        "个人档" : "1",#:material/person:
        "音乐" : "305",#:material/queue_music:
        "收藏" : "favorite"#:material/star:
}
selection = sac.segmented(
        items=[
            sac.SegmentedItem(label='主页', icon='book'),
            sac.SegmentedItem(label='相册', icon='collection'),
            sac.SegmentedItem(label='留言板', icon='journal-text'),
            sac.SegmentedItem(label='说说', icon='stickies-fill'),
            sac.SegmentedItem(label='个人档', icon='file-earmark-person'),
            sac.SegmentedItem(label='音乐', icon='music-note-list'),
            sac.SegmentedItem(label='收藏', icon='clipboard-heart'),
        ], label='', align='center', divider=False, use_container_width=True
    )

if not selection == None and not qq == "":
    st.link_button(label=":material/call_made: 立即跳转",url=f"https://user.qzone.qq.com/{qq}/{option_map[selection]}",use_container_width=True,type='primary')
elif qq == "":
    st.link_button(label=":material/call_made: 立即跳转",url="",use_container_width=True,type='primary',disabled=True,help="请输入目标QQ号")
elif selection == None:
    st.link_button(label=":material/call_made: 立即跳转",url="",use_container_width=True,type='primary',disabled=True,help="请选择一项板块")
