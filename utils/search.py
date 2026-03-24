"""
全局搜索模块
支持搜索景点、诗词、名人
"""
import streamlit as st
from pathlib import Path
import yaml
from typing import List, Dict, Any

DATA_DIR = Path(__file__).parent.parent / "data"


@st.cache_data
def load_all_data():
    """加载所有数据"""
    data = {}
    files = {
        'spots': 'scenic_spots.yml',
        'poems': 'poems.yml',
        'celebrities': 'celebrities.yml'
    }
    for key, filename in files.items():
        file_path = DATA_DIR / filename
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data[key] = yaml.safe_load(f)
        except Exception as e:
            data[key] = None
    return data


def search_spots(spots: List[Dict], keyword: str) -> List[Dict]:
    """搜索景点"""
    results = []
    keyword_lower = keyword.lower()
    for spot in spots:
        # 搜索名称、描述、标签
        name = spot.get('name', '')
        desc = spot.get('description', '')
        tags = ' '.join(spot.get('tags', []))
        subcategory = spot.get('subcategory', '')

        if (keyword_lower in name.lower() or
            keyword_lower in desc.lower() or
            keyword_lower in tags.lower() or
            keyword_lower in subcategory.lower()):
            results.append(spot)
    return results


def search_poems(poems: List[Dict], keyword: str) -> List[Dict]:
    """搜索诗词"""
    results = []
    keyword_lower = keyword.lower()
    for poem in poems:
        title = poem.get('title', '')
        content = poem.get('content', '')
        author = poem.get('author', '')
        dynasty = poem.get('dynasty', '')

        if (keyword_lower in title.lower() or
            keyword_lower in content.lower() or
            keyword_lower in author.lower() or
            keyword_lower in dynasty.lower()):
            results.append(poem)
    return results


def search_celebrities(celebrities: List[Dict], keyword: str) -> List[Dict]:
    """搜索名人"""
    results = []
    keyword_lower = keyword.lower()
    for celeb in celebrities:
        name = celeb.get('name', '')
        biography = celeb.get('biography', '')
        profession = celeb.get('profession', '')
        dynasty = celeb.get('dynasty', '')

        if (keyword_lower in name.lower() or
            keyword_lower in biography.lower() or
            keyword_lower in profession.lower() or
            keyword_lower in dynasty.lower()):
            results.append(celeb)
    return results


def render_search_results(results: Dict[str, List[Dict]], keyword: str):
    """渲染搜索结果"""
    st.subheader(f"搜索结果：'{keyword}'")

    total = sum(len(v) for v in results.values())
    if total == 0:
        st.info(f"未找到与 '{keyword}' 相关的内容")
        return

    # 景点结果
    if results.get('spots'):
        st.markdown(f"### 🏞️ 景点 ({len(results['spots'])})")
        cols = st.columns(2)
        for idx, spot in enumerate(results['spots'][:6]):
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

    # 诗词结果
    if results.get('poems'):
        st.markdown(f"### 📜 诗词 ({len(results['poems'])})")
        for poem in results['poems'][:5]:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**📖 {poem.get('title')}**")
                    st.caption(f"{poem.get('dynasty', '')} · {poem.get('author', '')}")
                with col2:
                    if poem.get('location'):
                        st.caption(f"📍 {poem.get('location')}")
                content = poem.get('content', '')
                st.markdown(f"> {content[:100]}..." if len(content) > 100 else f"> {content}")

    # 名人结果
    if results.get('celebrities'):
        st.markdown(f"### 👤 名人 ({len(results['celebrities'])})")
        cols = st.columns(2)
        for idx, celeb in enumerate(results['celebrities'][:6]):
            col = cols[idx % 2]
            with col:
                with st.container(border=True):
                    st.markdown(f"**{celeb.get('name')}**")
                    st.caption(f"{celeb.get('dynasty', '')} · {celeb.get('profession', '')}")
                    bio = celeb.get('biography', '')[:80]
                    st.write(f"{bio}...")

    # 提示
    if total > 17:
        st.info("💡 提示：搜索结果较多，请尝试更精确的关键词")


def show_search_modal():
    """显示搜索弹窗"""
    st.title("🔍 全局搜索")
    st.markdown("搜索景点、诗词、名人")

    # 搜索框
    keyword = st.text_input("", placeholder="输入关键词搜索...", label_visibility="collapsed")

    if keyword:
        # 加载数据
        all_data = load_all_data()

        results = {}
        if all_data.get('spots'):
            spots = all_data['spots'].get('scenic_spots', [])
            results['spots'] = search_spots(spots, keyword)

        if all_data.get('poems'):
            poems = all_data['poems'].get('poems', [])
            results['poems'] = search_poems(poems, keyword)

        if all_data.get('celebrities'):
            celebrities = all_data['celebrities'].get('celebrities', [])
            results['celebrities'] = search_celebrities(celebrities, keyword)

        render_search_results(results, keyword)

    # 热门搜索
    st.divider()
    st.subheader("🔥 热门搜索")
    hot_keywords = ["瀑布", "李白", "桃花", "日出", "佛教", "书院"]
    cols = st.columns(6)
    for idx, word in enumerate(hot_keywords):
        with cols[idx]:
            if st.button(f"#{word}", use_container_width=True, key=f"hot_{word}"):
                st.session_state['search_keyword'] = word
                st.rerun()
