"""
景点导览页面
"""
import streamlit as st
import yaml
from pathlib import Path
from utils.footprints import render_checkin_button, has_visited

st.set_page_config(
    page_title="景点导览",
    page_icon="🏞️",
    layout="wide"
)

# 数据目录
DATA_DIR = Path(__file__).parent.parent / "data"

@st.cache_data
def load_scenic_spots():
    """加载景点数据"""
    file_path = DATA_DIR / "scenic_spots.yml"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data.get('scenic_spots', [])
    except Exception as e:
        st.error(f"加载数据失败：{e}")
        return []

# 标题
st.title("🏞️ 景点导览")
st.markdown("探索庐山的自然美景和人文景观")

# 显示打卡进度
visited_count = len([s for s in load_scenic_spots() if has_visited(s.get('id', 0))])
total_count = len(load_scenic_spots())
st.sidebar.progress(visited_count / total_count if total_count > 0 else 0)
st.sidebar.markdown(f"**已打卡**: {visited_count}/{total_count}")

# 侧边栏筛选
st.sidebar.header("筛选条件")

# 加载数据
spots = load_scenic_spots()

# 分类筛选
categories = ["全部"] + list(set(s.get('category', '其他') for s in spots))
selected_category = st.sidebar.selectbox("景点分类", categories)

# 难度筛选
difficulties = ["全部"] + list(set(s.get('difficulty', '') for s in spots if s.get('difficulty')))
selected_difficulty = st.sidebar.selectbox("游览难度", difficulties)

# 搜索框
search_keyword = st.sidebar.text_input("搜索景点", placeholder="输入景点名称...")

# 应用筛选
filtered_spots = spots

if selected_category != "全部":
    filtered_spots = [s for s in filtered_spots if s.get('category') == selected_category]

if selected_difficulty != "全部":
    filtered_spots = [s for s in filtered_spots if s.get('difficulty') == selected_difficulty]

if search_keyword:
    keyword = search_keyword.lower()
    filtered_spots = [s for s in filtered_spots
                      if keyword in s.get('name', '').lower()
                      or keyword in s.get('description', '').lower()]

# 显示结果数量
st.sidebar.markdown(f"**找到 {len(filtered_spots)} 个景点**")

# 主内容区
if filtered_spots:
    # 卡片式展示
    cols = st.columns(2)

    for idx, spot in enumerate(filtered_spots):
        col = cols[idx % 2]
        with col:
            # 景点卡片
            with st.container(border=True):
                # 分类图标
                category_icons = {
                    '自然景观': '🏞️',
                    '人文景观': '🏛️',
                    '宗教建筑': '🛕'
                }
                icon = category_icons.get(spot.get('category', ''), '📍')

                st.markdown(f"### {icon} {spot.get('name', '未知景点')}")

                # 基本信息
                col1, col2 = st.columns(2)
                with col1:
                    st.caption(f"📍 {spot.get('subcategory', '')}")
                with col2:
                    difficulty_emoji = {'简单': '🟢', '中等': '🟡', '较难': '🔴'}.get(
                        spot.get('difficulty', ''), '⚪')
                    st.caption(f"{difficulty_emoji} {spot.get('difficulty', '未知')}")

                # 描述（截取前 100 字）
                description = spot.get('description', '')
                if description:
                    st.write(description[:150] + "..." if len(description) > 150 else description)

                # 海拔和游览时间
                col1, col2 = st.columns(2)
                with col1:
                    if spot.get('altitude'):
                        st.metric("海拔", f"{spot['altitude']}米")
                with col2:
                    if spot.get('visiting_time'):
                        st.metric("游览时间", spot['visiting_time'])

                # 标签
                tags = spot.get('tags', [])
                if tags:
                    st.markdown(" ".join([f"`#{tag}`" for tag in tags]))

                # 门票和开放时间
                if spot.get('ticket_price') is not None:
                    price = f"¥{spot['ticket_price']}" if spot['ticket_price'] > 0 else "免费"
                    st.caption(f"🎫 {price}")
                if spot.get('opening_hours'):
                    st.caption(f"🕐 {spot['opening_hours']}")

                # 打卡按钮
                render_checkin_button(spot.get('id', 0), spot.get('name', ''))

                # 详情按钮
                if st.button("查看详情", key=f"spot_{spot.get('id', idx)}"):
                    st.session_state['selected_spot'] = spot
                    st.rerun()

# 详情展示
if st.session_state.get('selected_spot'):
    spot = st.session_state['selected_spot']

    with st.sidebar:
        if st.button("关闭详情", on_click=lambda: st.session_state.pop('selected_spot', None)):
            st.rerun()

    # 详情模态框
    st.divider()
    st.subheader(f"📍 {spot.get('name')} - 详细信息")

    col1, col2 = st.columns([1, 1])

    with col1:
        # 模拟图片
        st.image("https://picsum.photos/seed/lushan1/600/400",
                 caption=spot.get('name', ''), width=500)

    with col2:
        st.markdown(f"""
        ### 基本信息
        - **分类**: {spot.get('category', '')} - {spot.get('subcategory', '')}
        - **海拔**: {spot.get('altitude', '未知')}米
        - **难度**: {spot.get('difficulty', '未知')}
        - **建议游览时间**: {spot.get('visiting_time', '未知')}
        - **标签**: {', '.join(spot.get('tags', []))}
        """)

        # 位置信息
        location = spot.get('location', {})
        if location:
            st.info(f"""
            📍 **地理位置**
            - 纬度：{location.get('lat', 'N/A')}
            - 经度：{location.get('lng', 'N/A')}
            """)

    st.markdown(f"""
    ### 景点介绍
    {spot.get('description', '暂无介绍')}
    """)

    # 门票和开放时间
    col1, col2 = st.columns(2)
    with col1:
        if spot.get('ticket_price') is not None:
            price = f"¥{spot['ticket_price']}" if spot['ticket_price'] > 0 else "免费"
            st.info(f"🎫 **门票**: {price}")
    with col2:
        if spot.get('opening_hours'):
            st.info(f"🕐 **开放时间**: {spot['opening_hours']}")

    # 打卡按钮
    if render_checkin_button(spot.get('id', 0), spot.get('name', '')):
        st.success(f"✅ 成功打卡 {spot.get('name', '')}！")

    # 推荐路线（如果有）
    routes_data = load_scenic_spots()  # 这里可以加载路线数据

else:
    st.info("💡 点击景点卡片可查看详细信息")
