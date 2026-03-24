"""
文化百科页面
"""
import streamlit as st
import yaml
from pathlib import Path

st.set_page_config(
    page_title="文化百科",
    page_icon="📚",
    layout="wide"
)

# 数据目录
DATA_DIR = Path(__file__).parent.parent / "data"

@st.cache_data
def load_culture_data():
    """加载文化数据"""
    celebrities_file = DATA_DIR / "celebrities.yml"
    poems_file = DATA_DIR / "poems.yml"

    celebrities = []
    poems = []

    try:
        with open(celebrities_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            celebrities = data.get('celebrities', [])
    except Exception as e:
        st.error(f"加载名人数据失败：{e}")

    try:
        with open(poems_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            poems = data.get('poems', [])
    except Exception as e:
        st.error(f"加载诗词数据失败：{e}")

    return celebrities, poems

# 标题
st.title("📚 文化百科")
st.markdown("探索庐山深厚的历史文化底蕴")

# 顶部标签页
tab1, tab2, tab3 = st.tabs(["📜 历史沿革", "👤 名人堂", "📖 诗词库"])

# ==================== 历史沿革 ====================
with tab1:
    st.header("📜 庐山历史沿革")

    # 时间线展示
    timeline = [
        {
            "period": "先秦时期",
            "year": "公元前",
            "event": "庐山早有记载",
            "description": "《尚书·禹贡》中就有'敷浅原'的记载，指的就是庐山一带。"
        },
        {
            "period": "汉代",
            "year": "公元前 202 年 - 公元 220 年",
            "event": "庐山之名正式出现",
            "description": "因殷周时期有匡俗兄弟七人在山中结庐隐居，故又称'匡山'或'匡庐'。"
        },
        {
            "period": "东晋",
            "year": "386 年",
            "event": "慧远创建东林寺",
            "description": "高僧慧远在庐山创立东林寺，开创佛教净土宗，使庐山成为佛教圣地。"
        },
        {
            "period": "南朝",
            "year": "406-477 年",
            "event": "陆修静修道庐山",
            "description": "著名道士陆修静在庐山简寂观修道，整理道教经典，庐山成为道教圣地之一。"
        },
        {
            "period": "唐代",
            "year": "618-907 年",
            "event": "庐山文化鼎盛",
            "description": "李白、白居易等众多文人墨客到此游览并留下大量诗篇。李白五次游庐山，作《望庐山瀑布》。"
        },
        {
            "period": "宋代",
            "year": "960-1279 年",
            "event": "苏轼题诗西林壁",
            "description": "苏轼游庐山作《题西林壁》，'不识庐山真面目'成为千古名句。朱熹在白鹿洞书院讲学。"
        },
        {
            "period": "近代",
            "year": "1895 年",
            "event": "庐山开辟避暑地",
            "description": "英国传教士李德立获准在庐山牯岭租地建房，开辟避暑地。"
        },
        {
            "period": "民国",
            "year": "1930 年代",
            "event": "庐山成为'夏都'",
            "description": "蒋介石曾多次在庐山召开会议，庐山成为国民政府的夏都。"
        },
        {
            "period": "现代",
            "year": "1959-1970 年",
            "event": "庐山会议",
            "description": "中共中央在庐山召开三次重要会议，在中国现代史上具有重要地位。"
        },
        {
            "period": "当代",
            "year": "1996 年",
            "event": "列入世界遗产",
            "description": "庐山以'庐山国家公园'之名被联合国教科文组织列入《世界遗产名录》。"
        },
        {
            "period": "当代",
            "year": "2004 年",
            "event": "世界地质公园",
            "description": "庐山被评为世界地质公园，地质遗迹丰富。"
        }
    ]

    for i, item in enumerate(timeline):
        with st.expander(f"**{item['period']}**（{item['year']}）- {item['event']}", expanded=(i==0)):
            st.write(item['description'])

    # 历史统计
    st.divider()
    col1, col2, col3 = st.columns(3)
    col1.metric("有记载历史", "约 3000 年")
    col2.metric("收录诗词", "4000 余首")
    col3.metric("世界遗产", "1996 年列入")

# ==================== 名人堂 ====================
with tab2:
    st.header("👤 名人堂")
    st.markdown("与庐山有关的历史名人")

    celebrities, poems = load_culture_data()

    if celebrities:
        # 侧边栏筛选
        st.sidebar.header("筛选名人")

        dynasties = ["全部"] + list(set(c.get('dynasty', '') for c in celebrities))
        selected_dynasty = st.sidebar.selectbox("选择朝代", dynasties)

        professions = ["全部"] + list(set(c.get('profession', '') for c in celebrities))
        selected_profession = st.sidebar.selectbox("选择身份", professions)

        # 筛选
        filtered_celebrities = celebrities
        if selected_dynasty != "全部":
            filtered_celebrities = [c for c in filtered_celebrities if c.get('dynasty') == selected_dynasty]
        if selected_profession != "全部":
            filtered_celebrities = [c for c in filtered_celebrities if c.get('profession') == selected_profession]

        st.sidebar.markdown(f"**找到 {len(filtered_celebrities)} 位名人**")

        # 展示名人卡片
        cols = st.columns(2)

        for idx, celebrity in enumerate(filtered_celebrities):
            col = cols[idx % 2]
            with col:
                with st.container(border=True):
                    # 头像（占位）
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.image("https://picsum.photos/seed/person/80/80",
                                 width=80)
                    with col2:
                        st.subheader(celebrity.get('name', '未知'))
                        st.caption(f"{celebrity.get('dynasty', '')} · {celebrity.get('profession', '')}")

                    st.write(celebrity.get('biography', '')[:100] + "...")

                    # 与庐山的关系
                    st.info(f"📍 **与庐山**: {celebrity.get('relation_to_lushan', '')[:50]}...")

                    # 详情按钮
                    if st.button("查看详情", key=f"celeb_{celebrity.get('id', idx)}"):
                        st.session_state['selected_celebrity'] = celebrity
                        st.rerun()

        # 名人详情
        if st.session_state.get('selected_celebrity'):
            celeb = st.session_state['selected_celebrity']

            st.divider()
            col1, col2 = st.columns([1, 2])

            with col1:
                st.image("https://picsum.photos/seed/person/300/300",
                         caption=celeb.get('name', ''), width=300)

            with col2:
                st.markdown(f"""
                ### {celeb.get('name', '未知')}
                - **朝代**: {celeb.get('dynasty', '未知')}
                - **身份**: {celeb.get('profession', '未知')}
                - **生卒**: {celeb.get('birth_year', '?')}-{celeb.get('death_year', '?')}
                """)

            st.markdown(f"""
            ### 生平简介
            {celeb.get('biography', '暂无简介')}

            ### 与庐山的关系
            {celeb.get('relation_to_lushan', '暂无')}
            """)

            # 相关诗词
            celeb_poems = [p for p in poems if p.get('author') == celeb.get('name')]
            if celeb_poems:
                st.markdown("### 相关诗词")
                for poem in celeb_poems:
                    with st.expander(f"📖 {poem.get('title', '无题')}"):
                        st.markdown(f"**{poem.get('dynasty', '')} · {poem.get('author', '')}**")
                        st.markdown(f"> {poem.get('content', '')}")

            if st.button("关闭详情", key="close_celeb"):
                st.session_state.pop('selected_celebrity', None)
                st.rerun()

    else:
        st.warning("暂无名人数据")

# ==================== 诗词库 ====================
with tab3:
    st.header("📖 诗词库")
    st.markdown("历代文人墨客留下的 4000 余首诗词")

    celebrities, poems = load_culture_data()

    if poems:
        # 侧边栏筛选
        st.sidebar.header("筛选诗词")

        # 作者筛选
        authors = ["全部"] + list(set(p.get('author', '') for p in poems))
        selected_author = st.sidebar.selectbox("选择作者", authors)

        # 朝代筛选
        dynasties = ["全部"] + list(set(p.get('dynasty', '') for p in poems))
        selected_dynasty = st.sidebar.selectbox("选择朝代", dynasties)

        # 搜索
        search_keyword = st.sidebar.text_input("搜索诗词", placeholder="输入诗词标题或内容...")

        # 筛选
        filtered_poems = poems
        if selected_author != "全部":
            filtered_poems = [p for p in filtered_poems if p.get('author') == selected_author]
        if selected_dynasty != "全部":
            filtered_poems = [p for p in filtered_poems if p.get('dynasty') == selected_dynasty]
        if search_keyword:
            keyword = search_keyword.lower()
            filtered_poems = [p for p in filtered_poems
                            if keyword in p.get('title', '').lower()
                            or keyword in p.get('content', '').lower()]

        st.sidebar.markdown(f"**找到 {len(filtered_poems)} 首诗词**")

        # 展示诗词
        for poem in filtered_poems:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"### 📜 {poem.get('title', '无题')}")
                    st.caption(f"{poem.get('dynasty', '')} · {poem.get('author', '')}")

                with col2:
                    if poem.get('location'):
                        st.caption(f"📍 {poem.get('location')}")

                content = poem.get('content', '')
                st.markdown(f"""
                <div style="background-color: #f9f9f9; padding: 15px; border-radius: 10px; margin: 10px 0;">
                    <pre style="white-space: pre-wrap; font-family: inherit; font-size: 1.1em;">{content}</pre>
                </div>
                """, unsafe_allow_html=True)

                # 创作背景
                if poem.get('background'):
                    with st.expander("📖 创作背景"):
                        st.write(poem.get('background'))

                # 类型标签
                if poem.get('type'):
                    st.markdown(f"`{poem.get('type')}`")

    else:
        st.warning("暂无诗词数据")
