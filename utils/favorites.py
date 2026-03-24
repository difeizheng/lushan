"""
收藏功能模块
"""
import streamlit as st
from typing import List, Dict, Optional

# 收藏数据存储键
FAVORITES_KEY = "user_favorites"


def init_favorites():
    """初始化收藏数据"""
    if FAVORITES_KEY not in st.session_state:
        st.session_state[FAVORITES_KEY] = {
            'spots': [],  # 收藏的景点 ID
            'poems': [],  # 收藏的诗词 ID
            'celebrities': []  # 收藏的名人 ID
        }


def toggle_favorite_spot(spot_id: int, spot_name: str) -> bool:
    """
    切换景点收藏状态

    Returns:
        True 如果收藏，False 如果取消收藏
    """
    init_favorites()
    favorites = st.session_state[FAVORITES_KEY]

    if spot_id in favorites['spots']:
        favorites['spots'].remove(spot_id)
        return False
    else:
        favorites['spots'].append(spot_id)
        return True


def toggle_favorite_poem(poem_id: int, poem_title: str) -> bool:
    """
    切换诗词收藏状态

    Returns:
        True 如果收藏，False 如果取消收藏
    """
    init_favorites()
    favorites = st.session_state[FAVORITES_KEY]

    if poem_id in favorites['poems']:
        favorites['poems'].remove(poem_id)
        return False
    else:
        favorites['poems'].append(poem_id)
        return True


def is_favorite_spot(spot_id: int) -> bool:
    """检查景点是否已收藏"""
    init_favorites()
    return spot_id in st.session_state[FAVORITES_KEY]['spots']


def is_favorite_poem(poem_id: int) -> bool:
    """检查诗词是否已收藏"""
    init_favorites()
    return poem_id in st.session_state[FAVORITES_KEY]['poems']


def get_favorite_spots() -> List[int]:
    """获取所有收藏的景点 ID"""
    init_favorites()
    return st.session_state[FAVORITES_KEY]['spots'].copy()


def get_favorite_poems() -> List[int]:
    """获取所有收藏的诗词 ID"""
    init_favorites()
    return st.session_state[FAVORITES_KEY]['poems'].copy()


def get_favorites_count() -> Dict[str, int]:
    """获取收藏数量"""
    init_favorites()
    favorites = st.session_state[FAVORITES_KEY]
    return {
        'spots': len(favorites['spots']),
        'poems': len(favorites['poems']),
        'celebrities': len(favorites['celebrities'])
    }


def render_favorite_button_spot(spot_id: int, spot_name: str) -> bool:
    """
    渲染收藏按钮（景点）

    Returns:
        是否切换了状态
    """
    init_favorites()
    is_fav = is_favorite_spot(spot_id)

    if st.button("❤️" if is_fav else "🤍", key=f"fav_spot_{spot_id}"):
        return toggle_favorite_spot(spot_id, spot_name)
    return False


def render_favorite_button_poem(poem_id: int, poem_title: str) -> bool:
    """
    渲染收藏按钮（诗词）

    Returns:
        是否切换了状态
    """
    init_favorites()
    is_fav = is_favorite_poem(poem_id)

    if st.button("❤️" if is_fav else "🤍", key=f"fav_poem_{poem_id}"):
        return toggle_favorite_poem(poem_id, poem_title)
    return False


def clear_all_favorites():
    """清空所有收藏"""
    st.session_state[FAVORITES_KEY] = {
        'spots': [],
        'poems': [],
        'celebrities': []
    }
