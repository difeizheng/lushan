"""
白鹿洞书院页面 - 展示中国四大书院之首
"""
import streamlit as st
import yaml
from pathlib import Path

st.set_page_config(
    page_title="白鹿洞书院",
    page_icon="🏛️",
    layout="wide"
)

# 数据目录
DATA_DIR = Path(__file__).parent.parent / "data"

@st.cache_data
def load_academy_data():
    """加载书院数据"""
    file_path = DATA_DIR / "academy.yml"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data
    except Exception as e:
        st.error(f"加载数据失败：{e}")
        return {}

st.title("🏛️ 白鹿洞书院")
st.markdown("中国四大书院之首 · 朱熹讲学之地 · 世界文化遗产组成部分")

# 加载数据
academy_data = load_academy_data()

if not academy_data:
    st.warning("暂无书院数据")
    st.stop()

info = academy_data.get('academy_info', {})
history = academy_data.get('history', [])
buildings = academy_data.get('buildings', [])
famous_persons = academy_data.get('famous_persons', [])
school_rules = academy_data.get('school_rules', {})
cultural_relics = academy_data.get('cultural_relics', [])
visiting_info = academy_data.get('visiting_info', {})
related_poems = academy_data.get('related_poems', [])

# 顶部信息卡
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("始建时间", info.get('established', '未知'))
with col2:
    st.metric("历史年限", f"{info.get('history_years', 0)}年")
with col3:
    st.metric("创始人", info.get('founder', '未知'))
with col4:
    st.metric("鼎盛时期", info.get('peak_period', '未知'))

st.divider()

# 书院简介
st.subheader("📖 书院简介")
st.markdown(info.get('description', ''))

#  tabs 页面
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📜 历史沿革", "🏛️ 建筑布局", "👥 名人堂", "📚 学规家训", "📍 游览指南"])

# ==================== 历史沿革 ====================
with tab1:
    st.header("📜 历史沿革")
    st.markdown("白鹿洞书院历经千年，见证了中国古代教育的兴衰")

    # 时间线展示
    for i, item in enumerate(history):
        with st.expander(f"**{item['period']}**（{item.get('year', '')}）- {item['event']}", expanded=(i==0)):
            st.write(item['description'])

    # 历史统计
    st.divider()
    col1, col2, col3 = st.columns(3)
    col1.metric("朝代更迭", len(history))
    col2.metric("历史地位", "四大书院之首")
    col3.metric("世界遗产", "1996 年列入")

# ==================== 建筑布局 ====================
with tab2:
    st.header("🏛️ 建筑布局")
    st.markdown("白鹿洞书院建筑群依山而建，布局严谨")

    # 建筑卡片
    for i, building in enumerate(buildings):
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### {building.get('name', '未知')}")
                st.caption(f"类型：{building.get('type', '未知')}")
                st.write(building.get('description', ''))
            with col2:
                st.info(f"🏛️ {building.get('type', '未知')}")

    # 建筑统计
    st.divider()
    building_types = {}
    for b in buildings:
        btype = b.get('type', '未知')
        building_types[btype] = building_types.get(btype, 0) + 1

    st.markdown("**建筑类型统计**")
    cols = st.columns(len(building_types))
    for i, (btype, count) in enumerate(building_types.items()):
        with cols[i]:
            st.metric(btype, f"{count}处")

# ==================== 名人堂 ====================
with tab3:
    st.header("👥 名人堂")
    st.markdown("历代与白鹿洞书院有关的名人")

    # 名人卡片
    for i, person in enumerate(famous_persons):
        with st.container(border=True):
            col1, col2, col3 = st.columns([1, 3, 2])
            with col1:
                # 头像占位
                st.image(f"https://picsum.photos/seed/{person.get('name', 'person')}/80/80", width=80)
            with col2:
                st.subheader(person.get('name', '未知'))
                st.caption(f"{person.get('dynasty', '')} · {person.get('role', '未知')}")
            with col3:
                st.info(f"📜 {person.get('role', '未知')}")

            st.write(person.get('story', ''))

    # 名人统计
    st.divider()
    dynasty_count = {}
    for p in famous_persons:
        dynasty = p.get('dynasty', '未知')
        dynasty_count[dynasty] = dynasty_count.get(dynasty, 0) + 1

    st.markdown("**按朝代统计**")
    cols = st.columns(len(dynasty_count))
    for i, (dynasty, count) in enumerate(dynasty_count.items()):
        with cols[i]:
            st.metric(dynasty, f"{count}人")

# ==================== 学规家训 ====================
with tab4:
    st.header("📚 白鹿洞书院揭示")
    st.markdown(f"**作者**: {school_rules.get('author', '未知')}  **年代**: {school_rules.get('year', '未知')}")
    st.markdown("---")

    # 学规内容
    rules_content = school_rules.get('content', [])
    rule_icons = ["🎯", "📖", "🧘", "⚖️", "🤝"]

    for i, rule in enumerate(rules_content):
        with st.container(border=True):
            st.markdown(f"### {rule_icons[i % len(rule_icons)]} {rule.get('category', '')}")
            st.markdown(f"<div style='font-size: 1.2em; padding: 10px; background-color: #f5f5f5; border-radius: 8px;'>{rule.get('text', '')}</div>", unsafe_allow_html=True)

    # 学规意义
    st.divider()
    st.markdown("### 📖 学规意义")
    st.markdown(school_rules.get('significance', ''))

    # 名句展示
    st.divider()
    st.markdown("### 💡 名句摘录")

    quote_cols = st.columns(5)
    quotes = [
        "博学之，审问之，慎思之，明辨之，笃行之。",
        "言忠信，行笃敬。",
        "己所不欲，勿施于人。",
        "正其义不谋其利，明其道不计其功。",
        "行有不得，反求诸己。"
    ]
    for i, quote in enumerate(quotes):
        with quote_cols[i]:
            st.markdown(f"> {quote}")

# ==================== 游览指南 ====================
with tab5:
    st.header("📍 游览指南")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🕐 开放时间")
        st.info(f"{visiting_info.get('open_time', '未知')}")

        st.markdown("### 🎫 门票价格")
        st.info(f"{visiting_info.get('ticket_price', '未知')}")

        st.markdown("### 🌸 最佳季节")
        st.info(f"{visiting_info.get('best_season', '未知')}")

    with col2:
        st.markdown("### 🚌 交通指南")
        st.write(visiting_info.get('traffic', '暂无信息'))

    st.divider()
    st.markdown("### 💡 游览贴士")
    tips = visiting_info.get('tips', [])
    for tip in tips:
        st.markdown(f"- {tip}")

    # 文物展示
    st.divider()
    st.markdown("### 🏺 珍贵文物")

    for relic in cultural_relics:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{relic.get('name', '未知')}**")
                st.caption(f"类型：{relic.get('type', '未知')}")
                st.write(relic.get('description', ''))
            with col2:
                status = relic.get('status', '未知')
                if status == "保存完好":
                    st.success(f"✅ {status}")
                elif status == "尚存":
                    st.info(f"ℹ️ {status}")
                else:
                    st.warning(f"⚠️ {status}")

# ==================== 相关诗词 ====================
st.divider()
st.subheader("📖 相关诗词")

for poem in related_poems:
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**📜 {poem.get('title', '无题')}**")
            st.caption(f"{poem.get('dynasty', '')} · {poem.get('author', '')}")
        with col2:
            st.info(f"🏛️ 白鹿洞书院")

        content = poem.get('content', '')
        st.markdown(f"""
        <div style="background-color: #f9f9f9; padding: 15px; border-radius: 10px; margin: 10px 0;">
            <pre style="white-space: pre-wrap; font-family: inherit; font-size: 1.1em;">{content}</pre>
        </div>
        """, unsafe_allow_html=True)
