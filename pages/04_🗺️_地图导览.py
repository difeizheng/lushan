"""
地图导览页面 - 带交互式地图
"""
import streamlit as st
import yaml
import folium
from folium import Marker, Popup
from streamlit_folium import folium_static
from pathlib import Path

st.set_page_config(
    page_title="地图导览",
    page_icon="🗺️",
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
st.title("🗺️ 地图导览")
st.markdown("查看庐山景点分布，规划游览路线")

# 加载数据
spots = load_scenic_spots()

# 侧边栏 - 筛选
st.sidebar.header("图层控制")

# 分类筛选
categories = ["全部"] + list(set(s.get('category', '其他') for s in spots))
selected_categories = st.sidebar.multiselect("景点分类", categories, default=["全部"])

# 难度筛选
difficulties = st.sidebar.multiselect(
    "游览难度",
    ["简单", "中等", "较难"],
    default=["简单", "中等", "较难"]
)

# 筛选景点
filtered_spots = spots

if "全部" not in selected_categories:
    filtered_spots = [s for s in filtered_spots if s.get('category') in selected_categories]

filtered_spots = [s for s in filtered_spots if s.get('difficulty') in difficulties]

st.sidebar.markdown(f"**显示 {len(filtered_spots)} 个景点**")

# 地图提示
st.info("""
📍 **地图使用说明**：
- 🏞️ 绿色标记：自然景观
- 🏛️ 棕色标记：人文景观
- 🛕 紫色标记：宗教建筑
- 点击标记可查看景点详情
- 使用鼠标滚轮缩放地图
""")

# 创建交互式地图
if filtered_spots:
    # 计算地图中心点（所有景点的平均位置）
    valid_spots = [s for s in filtered_spots if s.get('location', {}).get('lat') and s.get('location', {}).get('lng')]

    if valid_spots:
        center_lat = sum(s['location']['lat'] for s in valid_spots) / len(valid_spots)
        center_lng = sum(s['location']['lng'] for s in valid_spots) / len(valid_spots)
    else:
        center_lat, center_lng = 29.5683, 115.9850  # 默认牯岭镇位置

    # 创建地图
    m = folium.Map(
        location=[center_lat, center_lng],
        zoom_start=12,
        tiles='OpenStreetMap'
    )

    # 分类颜色映射
    category_colors = {
        '自然景观': 'green',
        '人文景观': 'brown',
        '宗教建筑': 'purple'
    }

    # 添加景点标记
    for spot in filtered_spots:
        location = spot.get('location', {})
        if location and location.get('lat') and location.get('lng'):
            lat = location['lat']
            lng = location['lng']
            name = spot.get('name', '未知')
            category = spot.get('category', '')
            difficulty = spot.get('difficulty', '')
            altitude = spot.get('altitude', '')
            description = spot.get('description', '')[:200]
            visiting_time = spot.get('visiting_time', '')

            # 获取颜色
            color = category_colors.get(category, 'blue')

            # 获取图标
            icon_map = {
                '自然景观': 'leaf',
                '人文景观': 'monument',
                '宗教建筑': 'religion'
            }
            icon = icon_map.get(category, 'info-sign')

            # 创建弹窗内容
            popup_html = f"""
            <div style="width: 250px; padding: 10px;">
                <h4 style="margin: 0; color: #2E8B57;">{name}</h4>
                <hr style="margin: 5px 0;">
                <p style="margin: 5px 0;"><strong>分类:</strong> {category}</p>
                <p style="margin: 5px 0;"><strong>难度:</strong> {difficulty}</p>
                {f'<p style="margin: 5px 0;"><strong>海拔:</strong> {altitude}米</p>' if altitude else ''}
                {f'<p style="margin: 5px 0;"><strong>游览时间:</strong> {visiting_time}</p>' if visiting_time else ''}
                <p style="margin: 5px 0; color: #666; font-size: 12px;">{description}...</p>
            </div>
            """

            # 添加标记
            Marker(
                location=[lat, lng],
                popup=Popup(popup_html, max_width=300),
                tooltip=name,
                icon=folium.Icon(color=color, icon=icon, prefix='glyphicon')
            ).add_to(m)

    # 添加牯岭镇标记
    Marker(
        location=[29.5683, 115.9850],
        popup="牯岭镇 - 庐山游客中心",
        tooltip="牯岭镇",
        icon=folium.Icon(color='red', icon='home', prefix='glyphicon')
    ).add_to(m)

    # 显示地图
    st.subheader("📍 庐山景点 interactive 地图")
    folium_static(m, width=900, height=600)

    # 景点坐标列表
    st.divider()
    st.subheader("景点坐标列表")

    # 创建 DataFrame 风格的展示
    for spot in filtered_spots:
        location = spot.get('location', {})
        if location and location.get('lat') and location.get('lng'):
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 1, 1])

                with col1:
                    category_icon = {
                        '自然景观': '🏞️',
                        '人文景观': '🏛️',
                        '宗教建筑': '🛕'
                    }.get(spot.get('category', ''), '📍')

                    st.markdown(f"**{category_icon} {spot.get('name', '未知')}**")
                    st.caption(f"{spot.get('category', '')} | {spot.get('difficulty', '')}")

                with col2:
                    st.metric("纬度", f"{location.get('lat', 0):.4f}°")

                with col3:
                    st.metric("经度", f"{location.get('lng', 0):.4f}°")

                if spot.get('altitude'):
                    st.caption(f"🏔️ 海拔：{spot['altitude']}米")

    # 导出地图数据
    st.divider()
    st.subheader("导出数据")

    # CSV 格式
    csv_data = "名称，分类，难度，纬度，经度，海拔\n"
    for spot in filtered_spots:
        location = spot.get('location', {})
        csv_data += f"{spot.get('name', '')},{spot.get('category', '')},{spot.get('difficulty', '')},{location.get('lat', '')},{location.get('lng', '')},{spot.get('altitude', '')}\n"

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="📥 下载 CSV 数据",
            data=csv_data,
            file_name="庐山景点坐标.csv",
            mime="text/csv"
        )

    with col2:
        # JSON 格式
        import json
        map_data = []
        for spot in filtered_spots:
            location = spot.get('location', {})
            map_data.append({
                'name': spot.get('name', ''),
                'lat': location.get('lat', 0),
                'lng': location.get('lng', 0),
                'category': spot.get('category', ''),
                'difficulty': spot.get('difficulty', ''),
                'altitude': spot.get('altitude', '')
            })
        json_data = json.dumps(map_data, ensure_ascii=False, indent=2)
        st.download_button(
            label="📥 下载 JSON 数据",
            data=json_data,
            file_name="庐山景点坐标.json",
            mime="application/json"
        )

else:
    st.warning("暂无符合条件的景点数据")

# 推荐游览顺序
st.divider()
st.subheader("🎯 推荐游览顺序")

st.markdown("""
**西线一日游**（适合首次游览）：
1. 牯岭镇出发
2. 如琴湖 → 花径 → 锦绣谷 → 仙人洞
3. 返回牯岭镇用餐
4. 下午前往三叠泉

**东线自然风光游**：
1. 含鄱口看日出
2. 五老峰登山
3. 三叠泉瀑布
4. 返回牯岭镇

**文化之旅**：
1. 美庐 → 庐山会议旧址
2. 白鹿洞书院
3. 东林寺
""")

# 外部地图链接
st.divider()
st.subheader("🔗 外部地图资源")

col1, col2, col3 = st.columns(3)

with col1:
    st.link_button(
        "🗺️ 百度地图 - 庐山",
        "https://map.baidu.com/search/庐山"
    )

with col2:
    st.link_button(
        "🗺️ 高德地图 - 庐山",
        "https://www.amap.com/search?query=庐山"
    )

with col3:
    st.link_button(
        "🌍 Google 地图 - 庐山",
        "https://www.google.com/maps/search/庐山"
    )
