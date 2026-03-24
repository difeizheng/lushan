"""
诗词地图页面 - 将诗词与地理位置结合
"""
import streamlit as st
import yaml
import folium
from pathlib import Path
from streamlit_folium import folium_static

st.set_page_config(
    page_title="诗词地图",
    page_icon="📜",
    layout="wide"
)

# 数据目录
DATA_DIR = Path(__file__).parent.parent / "data"

@st.cache_data
def load_poems():
    """加载诗词数据"""
    file_path = DATA_DIR / "poems.yml"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data.get('poems', [])
    except Exception as e:
        st.error(f"加载数据失败：{e}")
        return []

@st.cache_data
def load_scenic_spots():
    """加载景点数据"""
    file_path = DATA_DIR / "scenic_spots.yml"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data.get('scenic_spots', [])
    except Exception as e:
        return []

# 标题
st.title("📜 诗词地图")
st.markdown("跟着诗词游庐山，感受千年文化")

# 加载数据
poems = load_poems()
spots = load_scenic_spots()

# 创建景点位置映射
spot_locations = {}
for spot in spots:
    spot_locations[spot['name']] = spot.get('location', {})

# 侧边栏筛选
st.sidebar.header("筛选诗词")

# 作者筛选
authors = ["全部"] + list(set(p.get('author', '') for p in poems))
selected_author = st.sidebar.selectbox("选择作者", authors)

# 朝代筛选
dynasties = ["全部"] + list(set(p.get('dynasty', '') for p in poems))
selected_dynasty = st.sidebar.selectbox("选择朝代", dynasties)

# 类型筛选
types = ["全部"] + list(set(p.get('type', '') for p in poems))
selected_type = st.sidebar.selectbox("诗词类型", types)

# 筛选
filtered_poems = poems
if selected_author != "全部":
    filtered_poems = [p for p in filtered_poems if p.get('author') == selected_author]
if selected_dynasty != "全部":
    filtered_poems = [p for p in filtered_poems if p.get('dynasty') == selected_dynasty]
if selected_type != "全部":
    filtered_poems = [p for p in filtered_poems if p.get('type') == selected_type]

st.sidebar.markdown(f"**找到 {len(filtered_poems)} 首诗词**")

# 创建地图
st.subheader("🗺️ 诗词分布地图")

# 计算地图中心点
m = folium.Map(
    location=[29.55, 116.0],
    zoom_start=11,
    tiles='OpenStreetMap'
)

# 诗词位置映射
location_poems = {}

for poem in filtered_poems:
    location_name = poem.get('location', '')
    location_id = poem.get('location_id')

    # 尝试获取坐标
    lat, lng = None, None

    # 通过 location_id 获取景点坐标
    if location_id:
        for spot in spots:
            if spot.get('id') == location_id:
                loc = spot.get('location', {})
                lat = loc.get('lat')
                lng = loc.get('lng')
                break

    # 通过 location 名称匹配景点
    if not lat and not lng and location_name:
        for spot in spots:
            if location_name in spot.get('name', '') or spot.get('name', '') in location_name:
                loc = spot.get('location', {})
                lat = loc.get('lat')
                lng = loc.get('lng')
                break

    # 使用预设坐标（一些著名地点）
    if not lat and not lng:
        preset_locations = {
            '香炉峰': [29.54, 116.05],
            '花径': [29.569, 115.976],
            '西林寺': [29.57, 115.97],
            '庐山脚下': [29.55, 115.95],
            '五老峰': [29.5417, 116.0533],
            '庐山': [29.55, 116.0],
        }
        if location_name in preset_locations:
            lat, lng = preset_locations[location_name]

    if lat and lng:
        key = f"{lat},{lng}"
        if key not in location_poems:
            location_poems[key] = {
                'lat': lat,
                'lng': lng,
                'location': location_name,
                'poems': []
            }
        location_poems[key]['poems'].append(poem)

# 在地图上标记
for key, data in location_poems.items():
    # 创建弹窗内容
    popup_html = f"""
    <div style="width: 300px; max-height: 400px; overflow-y: auto; padding: 10px;">
        <h4 style="color: #8B4513; margin: 0;">📍 {data['location']}</h4>
        <hr style="margin: 10px 0;">
    """

    for poem in data['poems']:
        popup_html += f"""
        <div style="margin: 10px 0; padding: 10px; background-color: #f5f5f5; border-radius: 5px;">
            <strong>📖 {poem.get('title', '无题')}</strong><br>
            <span style="color: #666; font-size: 12px;">{poem.get('dynasty', '')} · {poem.get('author', '')}</span><br>
            <p style="font-size: 13px; margin: 5px 0; white-space: pre-wrap;">{poem.get('content', '')[:100]}...</p>
        </div>
        """

    popup_html += "</div>"

    # 添加标记
    folium.Marker(
        location=[data['lat'], data['lng']],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=f"📜 {len(data['poems'])}首",
        icon=folium.Icon(color='purple', icon='book', prefix='fa')
    ).add_to(m)

# 显示地图
folium_static(m, width=900, height=500)

# 诗词列表
st.divider()
st.subheader("📖 诗词列表")

for poem in filtered_poems:
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown(f"**📜 {poem.get('title')}**")
            st.caption(f"{poem.get('dynasty', '')} · {poem.get('author', '')}")

        with col2:
            if poem.get('location'):
                st.caption(f"📍 {poem.get('location')}")
            if poem.get('type'):
                st.caption(f"`{poem.get('type')}`")

        # 诗词内容
        content = poem.get('content', '')
        st.markdown(f"""
        <div style="background-color: #f9f9f9; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 4px solid {season_info['primary_color'] if 'season_info' in dir() else '#8B4513'};">
            <pre style="white-space: pre-wrap; font-family: inherit; font-size: 1.1em; margin: 0;">{content}</pre>
        </div>
        """, unsafe_allow_html=True)

        # 创作背景
        if poem.get('background'):
            with st.expander("📖 创作背景"):
                st.write(poem.get('background'))

# 统计信息
st.divider()
st.subheader("📊 诗词统计")

col1, col2, col3 = st.columns(3)

# 按作者统计
author_count = {}
for poem in poems:
    author = poem.get('author', '未知')
    author_count[author] = author_count.get(author, 0) + 1

# 按朝代统计
dynasty_count = {}
for poem in poems:
    dynasty = poem.get('dynasty', '未知')
    dynasty_count[dynasty] = dynasty_count.get(dynasty, 0) + 1

with col1:
    st.markdown("**按作者**")
    for author, count in sorted(author_count.items(), key=lambda x: -x[1])[:5]:
        st.caption(f"{author}: {count}首")

with col2:
    st.markdown("**按朝代**")
    for dynasty, count in dynasty_count.items():
        st.caption(f"{dynasty}: {count}首")

with col3:
    st.markdown("**按类型**")
    type_count = {}
    for poem in poems:
        ptype = poem.get('type', '未知')
        type_count[ptype] = type_count.get(ptype, 0) + 1
    for ptype, count in type_count.items():
        st.caption(f"{ptype}: {count}首")
