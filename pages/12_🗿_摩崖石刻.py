"""
摩崖石刻页面 - 展示庐山千年石刻文化
"""
import streamlit as st
import yaml
from pathlib import Path

st.set_page_config(
    page_title="摩崖石刻",
    page_icon="🗿",
    layout="wide"
)

# 数据目录
DATA_DIR = Path(__file__).parent.parent / "data"

@st.cache_data
def load_carvings():
    """加载摩崖石刻数据"""
    file_path = DATA_DIR / "stone_carvings.yml"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data.get('stone_carvings', [])
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

st.title("🗿 摩崖石刻")
st.markdown("庐山有 1000+ 处摩崖石刻，跨越 1500 多年历史，是珍贵的文化遗产")

# 加载数据
carvings = load_carvings()
spots = load_scenic_spots()

# 创建景点位置映射
spot_locations = {}
for spot in spots:
    spot_locations[spot['name']] = spot.get('location', {})

# 侧边栏筛选
st.sidebar.header("筛选石刻")

# 朝代筛选
dynasties = ["全部"] + list(set(c.get('dynasty', '') for c in carvings))
selected_dynasty = st.sidebar.selectbox("选择朝代", dynasties)

# 地点筛选
locations = ["全部"] + list(set(c.get('location', '') for c in carvings if c.get('location')))
selected_location = st.sidebar.selectbox("选择地点", locations)

# 书体筛选
styles = ["全部"] + list(set(c.get('style', '') for c in carvings if c.get('style')))
selected_style = st.sidebar.selectbox("选择书体", styles)

# 筛选
filtered_carvings = carvings
if selected_dynasty != "全部":
    filtered_carvings = [c for c in filtered_carvings if c.get('dynasty') == selected_dynasty]
if selected_location != "全部":
    filtered_carvings = [c for c in filtered_carvings if c.get('location') == selected_location]
if selected_style != "全部":
    filtered_carvings = [c for c in filtered_carvings if c.get('style') == selected_style]

st.sidebar.markdown(f"**找到 {len(filtered_carvings)} 处石刻**")

# 统计信息
st.subheader("📊 石刻统计")
col1, col2, col3, col4 = st.columns(4)

# 按朝代统计
dynasty_count = {}
for c in carvings:
    dynasty = c.get('dynasty', '未知')
    dynasty_count[dynasty] = dynasty_count.get(dynasty, 0) + 1

# 按书体统计
style_count = {}
for c in carvings:
    style = c.get('style', '未知')
    style_count[style] = style_count.get(style, 0) + 1

# 按地点统计
location_count = {}
for c in carvings:
    location = c.get('location', '未知')
    location_count[location] = location_count.get(location, 0) + 1

with col1:
    st.metric("石刻总数", len(carvings))

with col2:
    st.metric("最早朝代", "唐" if "唐" in dynasty_count else "宋")

with col3:
    st.metric("最多书体", max(style_count, key=style_count.get) if style_count else "未知")

with col4:
    st.metric("分布地点", len(location_count))

st.divider()

# 朝代时间线
st.subheader("📜 历史沿革")
timeline_data = sorted(dynasty_count.items(), key=lambda x: ['东汉', '东晋', '南朝', '唐', '宋', '元', '明', '清', '民国', '现代'].index(x[0]) if x[0] in ['东汉', '东晋', '南朝', '唐', '宋', '元', '明', '清', '民国', '现代'] else 99)

timeline_cols = st.columns(len(timeline_data))
for i, (dynasty, count) in enumerate(timeline_data):
    with timeline_cols[i]:
        st.markdown(f"**{dynasty}**")
        st.caption(f"{count}处")

st.divider()

# 石刻卡片展示
st.subheader(f"🗿 石刻列表 ({len(filtered_carvings)}处)")

# 分组展示
for carving in filtered_carvings:
    with st.container(border=True):
        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            st.markdown(f"### {carving.get('title', '无题')}")
            st.caption(f"{carving.get('dynasty', '')} · {carving.get('author', '佚名')} · {carving.get('year', '')}")
            st.write(carving.get('content', '')[:50] + "..." if len(carving.get('content', '')) > 50 else carving.get('content', ''))

        with col2:
            st.metric("书体", carving.get('style', '未知'))

        with col3:
            st.metric("地点", carving.get('location', '未知')[:4])

        # 石刻内容
        if carving.get('content'):
            st.markdown(f"""
            <div style="background-color: #f9f9f9; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 4px solid #8B4513;">
                <pre style="white-space: pre-wrap; font-family: inherit; font-size: 1.1em; margin: 0;">{carving.get('content', '')}</pre>
            </div>
            """, unsafe_allow_html=True)

        # 详细信息
        with st.expander("📋 详细信息"):
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"**尺寸**: {carving.get('size', '未知')}")
                st.markdown(f"**位置**: {carving.get('location', '未知')}")
            with col_b:
                st.markdown(f"**保存状况**: {carving.get('condition', '未知')}")
                st.markdown(f"**年代**: {carving.get('year', '未知')}")

            st.markdown(f"**描述**: {carving.get('description', '暂无描述')}")

            # 在地图上显示位置
            if carving.get('location_id') and carving.get('location'):
                location_name = carving.get('location')
                if location_name in spot_locations:
                    loc = spot_locations[location_name]
                    st.markdown(f"**坐标**: {loc.get('lat', 'N/A')}, {loc.get('lng', 'N/A')}")

st.divider()

# 书体知识
st.subheader("📖 书体知识")

style_info = {
    "楷书": {
        "description": "楷书又称正书、真书，由隶书演变而来，形体方正，笔画平直，可作楷模。",
        "features": "形体方正、笔画平直、结构严谨",
        "masters": "欧阳询、颜真卿、柳公权、赵孟頫"
    },
    "行书": {
        "description": "行书是介于楷书和草书之间的一种字体，既有楷书的工整，又有草书的流畅。",
        "features": "流畅自然、笔势连贯、易于辨认",
        "masters": "王羲之、王献之、苏轼、米芾"
    },
    "草书": {
        "description": "草书是汉字的一种字体，结构简省、笔画连绵，书写快捷。",
        "features": "结构简省、笔画连绵、气势奔放",
        "masters": "张旭、怀素、黄庭坚、毛泽东"
    },
    "隶书": {
        "description": "隶书由篆书演变而来，字形多呈宽扁，横画长而竖画短。",
        "features": "字形宽扁、蚕头燕尾、一波三折",
        "masters": "蔡邕、钟繇、邓石如、伊秉绶"
    },
    "篆书": {
        "description": "篆书是最古老的汉字书体，包括大篆和小篆，笔画圆润，结构对称。",
        "features": "笔画圆润、结构对称、古朴典雅",
        "masters": "李斯、邓石如、吴昌硕、齐白石"
    }
}

style_cols = st.columns(len(style_info))
for i, (style, info) in enumerate(style_info.items()):
    with style_cols[i]:
        with st.container(border=True):
            st.markdown(f"**{style}**")
            st.caption(info['description'][:30] + "...")
            if st.button("详情", key=f"style_{style}"):
                with st.expander("展开查看", expanded=True):
                    st.markdown(f"**特点**: {info['features']}")
                    st.markdown(f"**名家**: {info['masters']}")

st.divider()

# 保护知识
st.subheader("🛡️ 石刻保护")

st.markdown("""
### 摩崖石刻保护知识

庐山摩崖石刻是珍贵的历史文化遗产，需要我们一起保护：

1. **不要触摸石刻** - 手上的油脂和汗液会腐蚀石刻表面
2. **不要刻画涂鸦** - 保护石刻原貌，不留个人痕迹
3. **不要使用闪光灯** - 强光会加速石刻风化
4. **保持适当距离** - 避免呼吸中的湿气影响石刻
5. **遵守景区规定** - 按照指示牌和工作人员引导参观

### 风化因素

- **自然风化**: 风吹、日晒、雨淋、温差变化
- **生物侵蚀**: 苔藓、地衣、植物根系
- **人为破坏**: 刻画、拓印、不当修复

### 保护措施

- 定期清理表面杂物
- 安装防护栏和监控设备
- 建立数字化档案
- 限制游客接触
- 专业修复和维护
""")

# 景点链接
st.divider()
st.subheader("🗺️ 相关景点")

# 获取有石刻的景点
carving_locations = list(set(c.get('location') for c in carvings if c.get('location')))

location_cols = st.columns(min(6, len(carving_locations)))
for i, location in enumerate(carving_locations[:6]):
    with location_cols[i % 6]:
        count = len([c for c in carvings if c.get('location') == location])
        st.markdown(f"📍 **{location}**")
        st.caption(f"{count}处石刻")
