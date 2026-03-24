"""
行程规划页面
"""
import streamlit as st
import yaml
from pathlib import Path

st.set_page_config(
    page_title="行程规划",
    page_icon="🗺️",
    layout="wide"
)

# 数据目录
DATA_DIR = Path(__file__).parent.parent / "data"

@st.cache_data
def load_routes():
    """加载路线数据"""
    file_path = DATA_DIR / "routes.yml"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data.get('routes', [])
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
st.title("🗺️ 行程规划")
st.markdown("规划您的庐山之旅，定制专属行程")

# 侧边栏 - 路线类型筛选
st.sidebar.header("筛选路线")
routes = load_routes()

if routes:
    # 路线类型
    route_types = ["全部"] + list(set(r.get('type', '') for r in routes))
    selected_type = st.sidebar.selectbox("路线类型", route_types)

    # 难度筛选
    difficulties = ["全部"] + list(set(r.get('difficulty', '') for r in routes))
    selected_difficulty = st.sidebar.selectbox("游览难度", difficulties)

    # 时长筛选
    durations = ["全部"] + list(set(r.get('duration', '') for r in routes))
    selected_duration = st.sidebar.selectbox("游览时长", durations)

    # 筛选
    filtered_routes = routes
    if selected_type != "全部":
        filtered_routes = [r for r in filtered_routes if r.get('type') == selected_type]
    if selected_difficulty != "全部":
        filtered_routes = [r for r in filtered_routes if r.get('difficulty') == selected_difficulty]
    if selected_duration != "全部":
        filtered_routes = [r for r in filtered_routes if r.get('duration') == selected_duration]

    st.sidebar.markdown(f"**找到 {len(filtered_routes)} 条路线**")

    # 主内容区
    if filtered_routes:
        for route in filtered_routes:
            with st.container(border=True):
                # 路线头部
                col1, col2, col3 = st.columns([4, 1, 1])

                with col1:
                    route_icon = "🎯" if route.get('type') == '预设路线' else "🌟"
                    st.markdown(f"### {route_icon} {route.get('name', '未知路线')}")

                with col2:
                    difficulty_badge = {
                        '简单': '🟢',
                        '中等': '🟡',
                        '较难': '🔴'
                    }.get(route.get('difficulty', ''), '⚪')
                    st.markdown(f"{difficulty_badge} {route.get('difficulty', '未知')}")

                with col3:
                    st.markdown(f"⏱️ {route.get('duration', '未知')}")

                # 路线描述
                st.write(route.get('description', ''))

                # 途经景点
                if route.get('spots'):
                    st.markdown("**📍 行程安排:**")

                    # 按天分组显示
                    current_day = None
                    for spot in route['spots']:
                        if '天' in spot.get('name', ''):
                            current_day = spot['name']
                            st.markdown(f"#### {current_day}")
                        else:
                            col1, col2 = st.columns([1, 4])
                            with col1:
                                st.caption(f"⏱️ {spot.get('duration', '')}")
                            with col2:
                                note = f" - {spot.get('note', '')}" if spot.get('note') else ""
                                st.write(f"**{spot.get('name', '未知')}**{note}")

                # 温馨提示
                if route.get('tips'):
                    with st.expander("💡 温馨提示"):
                        st.markdown(route.get('tips', ''))

                # 选择此路线按钮
                if st.button("查看此路线", key=f"route_{route.get('id')}"):
                    st.session_state['selected_route'] = route
                    st.rerun()

    # 路线详情
    if st.session_state.get('selected_route'):
        route = st.session_state['selected_route']

        st.divider()
        st.subheader(f"📍 {route.get('name')} - 详细行程")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"""
            **路线类型**: {route.get('type', '未知')}
            **游览时长**: {route.get('duration', '未知')}
            **难度等级**: {route.get('difficulty', '未知')}
            """)

        with col2:
            st.image("https://picsum.photos/seed/route/400/200",
                     caption=route.get('name', ''), width=400)

        st.markdown(f"""
        ### 路线介绍
        {route.get('description', '')}
        """)

        if st.button("关闭详情", key="close_route"):
            st.session_state.pop('selected_route', None)
            st.rerun()

else:
    st.warning("暂无路线数据")

# 自定义行程工具
st.divider()
st.subheader("🛠️ 自定义行程")

st.markdown("""
如果您想自己规划行程，可以参考以下步骤：
1. 从景点导览页面选择您想游览的景点
2. 根据景点位置规划合理的游览顺序
3. 考虑每个景点的游览时间和交通时间
4. 合理安排住宿和用餐
""")

spots = load_scenic_spots()
if spots:
    # 简易的行程规划器
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**可选景点**")
        available_spots = [s['name'] for s in spots]
        selected_spots = st.multiselect(
            "选择想游览的景点",
            available_spots,
            placeholder="选择景点..."
        )

    with col2:
        if selected_spots:
            st.markdown("**您的行程**")
            for i, spot_name in enumerate(selected_spots, 1):
                spot = next((s for s in spots if s['name'] == spot_name), None)
                if spot:
                    st.write(f"{i}. {spot_name} - {spot.get('visiting_time', '未知时间')}")

            # 导出行程
            if st.button("生成行程单"):
                itinerary = "\n".join([f"{i}. {s}" for i, s in enumerate(selected_spots, 1)])
                st.download_button(
                    label="下载行程单",
                    data=itinerary,
                    file_name="我的庐山行程.txt",
                    mime="text/plain"
                )

# 页脚提示
st.divider()
st.info("💡 提示：以上路线仅供参考，实际游览时请根据天气、体力等情况灵活调整")
