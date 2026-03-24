"""
我的收藏页面
"""
import streamlit as st
from utils.favorites import get_favorite_spots, get_favorite_poems, init_favorites, get_favorites_count
from utils.search import load_all_data

st.set_page_config(
    page_title="我的收藏",
    page_icon="❤️",
    layout="wide"
)

st.title("❤️ 我的收藏")
st.markdown("管理您收藏的景点和诗词")

init_favorites()

# 统计
counts = get_favorites_count()
col1, col2, col3 = st.columns(3)
col1.metric("收藏景点", counts['spots'])
col2.metric("收藏诗词", counts['poems'])
col3.metric("收藏名人", counts['celebrities'])

st.divider()

# 加载数据
all_data = load_all_data()

# 收藏的景点
st.subheader("🏞️ 收藏的景点")
favorite_spot_ids = get_favorite_spots()

if favorite_spot_ids and all_data.get('spots'):
    spots = all_data['spots'].get('scenic_spots', [])
    fav_spots = [s for s in spots if s.get('id') in favorite_spot_ids]

    if fav_spots:
        cols = st.columns(2)
        for idx, spot in enumerate(fav_spots):
            col = cols[idx % 2]
            with col:
                with st.container(border=True):
                    category_icons = {
                        '自然景观': '🏞️',
                        '人文景观': '🏛️',
                        '宗教建筑': '🛕'
                    }
                    icon = category_icons.get(spot.get('category', ''), '📍')
                    st.markdown(f"**{icon} {spot.get('name')}**")
                    st.caption(f"{spot.get('category')} | {spot.get('difficulty', 'N/A')}")
                    desc = spot.get('description', '')[:80]
                    st.write(f"{desc}...")
                    if spot.get('ticket_price') is not None:
                        price = f"¥{spot['ticket_price']}" if spot['ticket_price'] > 0 else "免费"
                        st.caption(f"🎫 {price}")
    else:
        st.info("暂无收藏的景点")
else:
    st.info("暂无收藏的景点")

st.divider()

# 收藏的诗词
st.subheader("📜 收藏的诗词")
favorite_poem_ids = get_favorite_poems()

if favorite_poem_ids and all_data.get('poems'):
    poems = all_data['poems'].get('poems', [])
    fav_poems = [p for p in poems if p.get('id') in favorite_poem_ids]

    if fav_poems:
        for poem in fav_poems:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**📖 {poem.get('title')}**")
                    st.caption(f"{poem.get('dynasty', '')} · {poem.get('author', '')}")
                with col2:
                    if poem.get('location'):
                        st.caption(f"📍 {poem.get('location')}")
                content = poem.get('content', '')
                st.markdown(f"> {content}")
    else:
        st.info("暂无收藏的诗词")
else:
    st.info("暂无收藏的诗词")
