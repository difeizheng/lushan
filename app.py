"""
庐山文化旅游信息平台 - 主应用
Streamlit Application
"""
import streamlit as st
import yaml
from pathlib import Path
from datetime import datetime
from utils.weather import get_current_weather, get_clothing_advice, get_travel_advice
from utils.seasons import get_current_season, get_season_info, render_season_banner, get_season_recommendations

# 页面配置
st.set_page_config(
    page_title="庐山文旅通",
    page_icon="🏞️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 数据目录
DATA_DIR = Path(__file__).parent / "data"

# 获取当前季节
current_season = get_current_season()
season_info = get_season_info()

# 自定义 CSS 样式（根据季节动态变化）
st.markdown(f"""
<style>
    .main-header {{
        font-size: 2.5rem;
        font-weight: bold;
        color: {season_info['primary_color']};
        text-align: center;
        margin-bottom: 1rem;
    }}
    .sub-header {{
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }}
    .card {{
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    .stButton>button {{
        width: 100%;
        border-radius: 5px;
        height: 3em;
    }}
    .search-box input {{
        font-size: 1.1rem;
        padding: 10px;
        border-radius: 10px;
        border: 2px solid {season_info['primary_color']};
    }}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data(file_name: str):
    """加载 YAML 数据文件"""
    file_path = DATA_DIR / file_name
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        st.error(f"加载数据失败：{e}")
        return None


def get_season_recommendation():
    """根据当前月份获取推荐景点"""
    month = datetime.now().month
    if 3 <= month <= 5:
        return '春季', ['花径', '锦绣谷', '如琴湖'], '🌸 春季是赏花的好时节，推荐游览花径、锦绣谷等地'
    elif 6 <= month <= 8:
        return '夏季', ['三叠泉', '含鄱口', '五老峰'], '🌋 夏季凉爽宜人，是避暑观景的最佳季节'
    elif 9 <= month <= 11:
        return '秋季', ['五老峰', '汉阳峰', '含鄱口'], '🍁 秋高气爽，适合登高观景，观赏日出云海'
    else:
        return '冬季', ['含鄱口', '五老峰', '汉阳峰'], '❄️ 冬季可观赏雾凇雪景，别有一番风味'


def get_today_recommendation(spots: list, weather_data: dict) -> list:
    """根据天气获取今日推荐景点"""
    if not weather_data or not spots:
        return spots[:3] if spots else []

    # 根据天气推荐
    weather_code = weather_data.get('weather_code', 0)
    temp = weather_data.get('temperature', 20)

    recommended = []

    # 晴天推荐观景
    if weather_code <= 2:
        for spot in spots:
            if spot.get('category') == '自然景观' and spot.get('difficulty') in ['简单', '中等']:
                recommended.append(spot)
    # 多云/阴天推荐室内外结合
    elif weather_code <= 48:
        for spot in spots:
            if spot.get('category') in ['人文景观', '宗教建筑']:
                recommended.append(spot)
    # 雨天推荐室内
    else:
        for spot in spots:
            if spot.get('subcategory') in ['历史遗迹', '古刹', '书院', '历史建筑']:
                recommended.append(spot)

    # 温度过高/过低推荐轻松路线
    if temp > 28 or temp < 5:
        recommended = [s for s in recommended if s.get('difficulty') == '简单']

    return recommended[:4] if recommended else spots[:3]


def show_homepage():
    """显示首页"""
    # 季节横幅
    st.markdown(render_season_banner(), unsafe_allow_html=True)

    # 头部
    st.markdown('<p class="main-header">🏞️ 庐山文旅通</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-header">{season_info["description"]} · {season_info["icon"]}</p>', unsafe_allow_html=True)

    # 全局搜索框
    search_query = st.text_input(
        "🔍 搜索景点、诗词、名人",
        placeholder="输入关键词，如'瀑布'、'李白'、'桃花'...",
        key="global_search",
        label_visibility="collapsed"
    )

    if search_query:
        st.switch_page("pages/00_🔍_搜索.py")

    # 分隔线
    st.divider()

    # 今日推荐
    st.subheader("🌤️ 今日推荐")

    weather_data = get_current_weather()
    spots_data = load_data("scenic_spots.yml")
    spots = spots_data.get('scenic_spots', []) if spots_data else []

    if weather_data:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("当前温度", f"{weather_data['temperature']}°C")
        with col2:
            st.metric("湿度", f"{weather_data['humidity']}%")
        with col3:
            st.metric("天气", weather_data['weather_desc'])
        with col4:
            st.metric("风速", f"{weather_data['wind_speed']} km/h")

        # 穿衣和旅游建议
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"👔 {get_clothing_advice(weather_data['temperature'])}")
        with col2:
            st.success(f"🎯 {get_travel_advice(weather_data['weather_code'])}")

        # 今日推荐景点
        today_spots = get_today_recommendation(spots, weather_data)
        if today_spots:
            st.markdown("**推荐游览**：")
            spot_names = [s['name'] for s in today_spots]
            st.write(" → ".join(spot_names))

    else:
        # 季节推荐
        season, rec_spots, tip = get_season_recommendation()
        st.info(f"{tip}")
        st.markdown(f"**{season}推荐**：{'、'.join(rec_spots)}")

    # 本季推荐
    st.divider()
    st.subheader(f"{season_info['icon']} {season_info['name']}推荐")

    rec = get_season_recommendations()
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**📍 推荐景点**")
        for spot in rec['best_spots']:
            st.markdown(f"- {spot}")

    with col2:
        st.markdown("**🎯 推荐活动**")
        for activity in rec['activities']:
            st.markdown(f"- {activity}")

    with col3:
        st.markdown("**👔 穿衣建议**")
        st.info(rec['clothing'])

    st.divider()

    # 简介
    col1, col2 = st.columns([1, 1])

    with col1:
        st.image("https://images.unsplash.com/photo-1508804185872-d7adad5e38ba?w=800",
                 caption="庐山风光", width=600)

    with col2:
        st.subheader("欢迎来到庐山")
        st.write("""
        庐山，位于中国江西省九江市境内，是一座地垒式断块山，
        主峰汉阳峰海拔 1474 米。庐山以雄、奇、险、秀闻名于世，
        素有"匡庐奇秀甲天下"之美誉。

        - 🏔️ **世界文化景观遗产**（1996 年）
        - 🌋 **世界地质公园**（2004 年）
        - ⭐ **国家 5A 级旅游景区**
        - 📜 **中华十大名山之一**
        """)

    st.divider()

    # 快速入口
    st.subheader("🚀 快速入口")
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("🔍 搜索", use_container_width=True):
            st.switch_page("pages/00_🔍_搜索.py")
    with col2:
        if st.button("🏞️ 景点导览", use_container_width=True):
            st.switch_page("pages/01_🏞️_景点导览.py")
    with col3:
        if st.button("📚 文化百科", use_container_width=True):
            st.switch_page("pages/02_📚_文化百科.py")
    with col4:
        if st.button("🗺️ 行程规划", use_container_width=True):
            st.switch_page("pages/03_🗺️_行程规划.py")
    with col5:
        if st.button("🗺️ 地图导览", use_container_width=True):
            st.switch_page("pages/04_🗺️_地图导览.py")

    st.divider()

    # 数据加载
    spots_data = load_data("scenic_spots.yml")
    poems_data = load_data("poems.yml")
    routes_data = load_data("routes.yml")

    # 统计信息
    st.subheader("📊 庐山概览")
    col1, col2, col3, col4, col5 = st.columns(5)

    if spots_data:
        spots = spots_data.get('scenic_spots', [])
        natural = len([s for s in spots if s.get('category') == '自然景观'])
        cultural = len([s for s in spots if s.get('category') == '人文景观'])
        religious = len([s for s in spots if s.get('category') == '宗教建筑'])
        free = len([s for s in spots if s.get('ticket_price', 0) == 0])
        paid = len([s for s in spots if s.get('ticket_price', 0) > 0])

        col1.metric("景点总数", len(spots))
        col2.metric("自然景观", natural)
        col3.metric("人文景观", cultural)
        col4.metric("宗教建筑", religious)
        col5.metric("免费景点", free)

    st.divider()

    # 推荐路线
    st.subheader("🎯 推荐游览路线")

    if routes_data:
        routes = routes_data.get('routes', [])
        for route in routes[:3]:
            with st.expander(f"📍 {route['name']} - {route['duration']}（{route['difficulty']}）"):
                st.write(route['description'])
                if route.get('spots'):
                    spots_names = [s['name'] for s in route['spots'] if s.get('spot_id')]
                    st.write("**途经景点**: " + " → ".join(spots_names[:5]))

    st.divider()

    # 经典诗词
    st.subheader("📜 经典诗词")

    if poems_data:
        poems = poems_data.get('poems', [])
        poem = poems[0] if poems else None
        if poem:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.info(f"**{poem['title']}**\n\n{poem['author']}·{poem['dynasty']}")
            with col2:
                st.markdown(f"> {poem['content']}")

    # 页脚
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>🏞️ 庐山文旅通 - 探索匡庐奇秀，感受千年文化</p>
        <p style="font-size: 0.8rem;">Powered by Streamlit | 数据来源：公开资料整理</p>
    </div>
    """, unsafe_allow_html=True)


# 主函数
def main():
    # 检查是否在首页
    if st.query_params.get("page") is None:
        show_homepage()
    else:
        # 其他页面通过 pages 目录处理
        st.write("请使用侧边栏导航访问其他页面")


if __name__ == "__main__":
    main()
