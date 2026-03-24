"""
茶文化页面 - 展示庐山云雾茶文化
"""
import streamlit as st
import yaml
from pathlib import Path

st.set_page_config(
    page_title="庐山云雾茶",
    page_icon="🍵",
    layout="wide"
)

# 数据目录
DATA_DIR = Path(__file__).parent.parent / "data"

@st.cache_data
def load_tea_data():
    """加载茶文化数据"""
    file_path = DATA_DIR / "tea.yml"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data
    except Exception as e:
        st.error(f"加载数据失败：{e}")
        return {}

st.title("🍵 庐山云雾茶")
st.markdown("中国十大名茶之一 · 千年茶史 · 云雾滋养")

# 加载数据
tea_data = load_tea_data()

if not tea_data:
    st.warning("暂无茶文化数据")
    st.stop()

info = tea_data.get('tea_info', {})
history = tea_data.get('history', [])
growing_areas = tea_data.get('growing_areas', [])
tea_varieties = tea_data.get('tea_varieties', [])
processing_steps = tea_data.get('processing_steps', [])
brewing_guide = tea_data.get('brewing_guide', {})
health_benefits = tea_data.get('health_benefits', [])
culture_stories = tea_data.get('culture_stories', [])
visiting_tea_gardens = tea_data.get('visiting_tea_gardens', {})
buying_guide = tea_data.get('buying_guide', {})
related_poems = tea_data.get('related_poems', [])

# 顶部信息卡
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("茶叶类型", info.get('type', '未知'))
with col2:
    st.metric("历史年限", f"{info.get('history_years', 0)}年")
with col3:
    st.metric("产地", "江西庐山")
with col4:
    st.metric("荣誉", "中国十大名茶")

st.divider()

# 茶叶简介
st.subheader("📖 茶叶简介")
st.markdown(info.get('description', ''))

# Tabs 页面
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📜 历史沿革", "🌱 种植区域", "🏭 制作工艺", "🫖 冲泡指南", "💊 功效作用", "📚 文化故事"])

# ==================== 历史沿革 ====================
with tab1:
    st.header("📜 庐山云雾茶历史")
    st.markdown("庐山云雾茶有 1800 多年种植历史，历经多个朝代发展")

    # 时间线展示
    for i, item in enumerate(history):
        with st.expander(f"**{item['period']}**（{item.get('year', '')}）- {item['event']}", expanded=(i==0)):
            st.write(item['description'])

    # 历史里程碑
    st.divider()
    st.markdown("### 🏆 重要里程碑")
    milestone_cols = st.columns(3)
    with milestone_cols[0]:
        st.info("**唐代**\n\n被列为贡茶")
    with milestone_cols[1]:
        st.info("**1915 年**\n\n获巴拿马万国博览会金奖")
    with milestone_cols[2]:
        st.info("**1959 年**\n\n被评为全国十大名茶")

# ==================== 种植区域 ====================
with tab2:
    st.header("🌱 种植区域")
    st.markdown("庐山云雾茶产于海拔 700 米以上的山区，云雾缭绕，品质优良")

    # 茶区卡片
    for area in growing_areas:
        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"**📍 {area.get('name', '未知')}**")
                st.caption(f"海拔：{area.get('elevation', '未知')}")
            with col2:
                st.metric("面积", area.get('area', '未知'))
            with col3:
                st.info(f"🌿 {area.get('location_id', 'N/A')}")
            st.write(area.get('characteristic', ''))

    # 茶区统计
    st.divider()
    total_area = sum(int(a.get('area', '0').replace('亩', '')) for a in growing_areas if a.get('area'))
    st.metric("总种植面积", f"{total_area}亩")

# ==================== 制作工艺 ====================
with tab3:
    st.header("🏭 制作工艺")
    st.markdown("庐山云雾茶制作精细，经过六道工艺流程")

    # 步骤展示
    for step in processing_steps:
        with st.container(border=True):
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown(f"### 步骤{step.get('step', '')}")
                st.markdown(f"**{step.get('name', '未知')}**")
            with col2:
                st.write(step.get('description', ''))
                if step.get('time'):
                    st.caption(f"⏱️ 时间：{step.get('time', '')}")

    # 工艺流程图（文字版）
    st.divider()
    st.markdown("### 📊 工艺流程")
    process_flow = " → ".join([s.get('name', '') for s in processing_steps])
    st.info(f"**采摘** → **摊晾** → **杀青** → **揉捻** → **干燥** → **筛选**")

# ==================== 冲泡指南 ====================
with tab4:
    st.header("🫖 冲泡指南")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 水温")
        st.metric("推荐水温", brewing_guide.get('water_temperature', '80-85°C'))

        st.markdown("### 茶量")
        st.metric("推荐茶量", brewing_guide.get('tea_amount', '3-5 克/150ml'))

    with col2:
        st.markdown("### 冲泡时间")
        steeping = brewing_guide.get('steeping_time', {})
        for key, value in steeping.items():
            st.caption(f"{key}: {value}")

    st.divider()
    st.markdown("### 🫙 推荐器具")
    vessels = brewing_guide.get('vessels', [])
    vessel_cols = st.columns(len(vessels))
    for i, vessel in enumerate(vessels):
        with vessel_cols[i]:
            st.info(f"**{vessel}**")

    st.divider()
    st.markdown("### 💡 冲泡技巧")
    tips = brewing_guide.get('tips', [])
    for tip in tips:
        st.markdown(f"- {tip}")

# ==================== 功效作用 ====================
with tab5:
    st.header("💊 功效作用")
    st.markdown("庐山云雾茶富含茶多酚、氨基酸等多种营养成分")

    # 功效卡片
    for benefit in health_benefits:
        with st.container(border=True):
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown("### ✅")
            with col2:
                st.markdown(f"**{benefit.get('benefit', '未知')}**")
                st.write(benefit.get('description', ''))

# ==================== 文化故事 ====================
with tab6:
    st.header("📚 文化故事")

    for story in culture_stories:
        with st.expander(f"📖 {story.get('title', '无题')}", expanded=True):
            st.markdown(story.get('content', ''))

    st.divider()
    st.markdown("### 📜 相关诗词")
    for poem in related_poems:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**📜 {poem.get('title', '无题')}**")
                st.caption(f"{poem.get('dynasty', '')} · {poem.get('author', '')}")
            with col2:
                st.info("🍵 茶")

            content = poem.get('content', '')
            st.markdown(f"""
            <div style="background-color: #f9f9f9; padding: 15px; border-radius: 10px; margin: 10px 0;">
                <pre style="white-space: pre-wrap; font-family: inherit; font-size: 1.1em;">{content}</pre>
            </div>
            """, unsafe_allow_html=True)

# ==================== 品种等级 ====================
st.divider()
st.subheader("🏷️ 茶叶品种与等级")

variety_cols = st.columns(len(tea_varieties))
for i, variety in enumerate(tea_varieties):
    with variety_cols[i]:
        with st.container(border=True):
            st.markdown(f"**{variety.get('name', '未知')}**")
            st.caption(f"等级：{variety.get('grade', '未知')}")
            st.write(f"采摘时间：{variety.get('harvest_time', '未知')}")
            st.write(f"特点：{variety.get('characteristic', '未知')}")
            st.info(f"价格：{variety.get('price_range', '未知')}")

# ==================== 游览茶园 ====================
st.divider()
st.subheader("🌱 游览茶园")

st.markdown(f"**最佳时间**: {visiting_tea_gardens.get('best_time', '未知')}")

st.markdown("### 🎯 体验活动")
activities = visiting_tea_gardens.get('activities', [])
activity_cols = st.columns(len(activities))
for i, activity in enumerate(activities):
    with activity_cols[i]:
        st.info(f"**{activity}**")

st.markdown("### 📍 推荐茶园")
gardens = visiting_tea_gardens.get('recommended_gardens', [])
for garden in gardens:
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**📍 {garden.get('name', '未知')}**")
            st.caption(f"位置：{garden.get('location', '未知')}")
            st.write(garden.get('features', ''))
        with col2:
            location_id = garden.get('location_id')
            if location_id:
                st.success("✅ 可导航")
            else:
                st.info("ℹ️ 详情咨询")

# ==================== 购买指南 ====================
st.divider()
st.subheader("🛒 购买指南")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔍 选购技巧")
    tips = buying_guide.get('tips', [])
    for tip in tips:
        st.markdown(f"- {tip}")

with col2:
    st.markdown("### 💰 价格参考")
    price_ref = buying_guide.get('price_reference', [])
    for ref in price_ref:
        st.info(f"**{ref.get('grade', '未知')}**: {ref.get('price', '未知')}")

st.divider()
st.markdown(f"""
> 🏷️ **地理标志**: {buying_guide.get('authentic_mark', '请认准地理标志保护产品标识')}
""")
