"""
游览足迹打卡模块
"""
import streamlit as st
from datetime import datetime
from typing import List, Dict, Set

# 足迹数据存储键
FOOTPRINTS_KEY = "user_footprints"
BADGES_KEY = "user_badges"


def init_footprints():
    """初始化足迹数据"""
    if FOOTPRINTS_KEY not in st.session_state:
        st.session_state[FOOTPRINTS_KEY] = {
            'visited_spots': [],  # 已访问景点 ID 列表
            'check_ins': []  # 打卡记录
        }
    if BADGES_KEY not in st.session_state:
        st.session_state[BADGES_KEY] = []


def check_in_spot(spot_id: int, spot_name: str) -> bool:
    """
    打卡景点

    Args:
        spot_id: 景点 ID
        spot_name: 景点名称

    Returns:
        是否首次打卡
    """
    init_footprints()
    footprints = st.session_state[FOOTPRINTS_KEY]

    is_first_visit = spot_id not in footprints['visited_spots']

    if is_first_visit:
        footprints['visited_spots'].append(spot_id)
        footprints['check_ins'].append({
            'spot_id': spot_id,
            'spot_name': spot_name,
            'check_in_time': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'weather': '晴'  # 可以结合天气 API
        })
        st.session_state[FOOTPRINTS_KEY] = footprints

        # 检查是否获得新徽章
        check_and_add_badges()

    return is_first_visit


def has_visited(spot_id: int) -> bool:
    """检查是否已访问过某景点"""
    init_footprints()
    return spot_id in st.session_state[FOOTPRINTS_KEY]['visited_spots']


def get_visited_count() -> int:
    """获取已访问景点数量"""
    init_footprints()
    return len(st.session_state[FOOTPRINTS_KEY]['visited_spots'])


def get_all_visited_spots() -> List[int]:
    """获取所有已访问景点 ID"""
    init_footprints()
    return st.session_state[FOOTPRINTS_KEY]['visited_spots'].copy()


def get_check_in_history() -> List[Dict]:
    """获取打卡历史记录"""
    init_footprints()
    return st.session_state[FOOTPRINTS_KEY]['check_ins'].copy()


def reset_footprints():
    """重置足迹数据"""
    st.session_state[FOOTPRINTS_KEY] = {
        'visited_spots': [],
        'check_ins': []
    }
    st.session_state[BADGES_KEY] = []


# 徽章系统
BADGES = {
    '新人访客': {'threshold': 1, 'icon': '🌟', 'desc': '首次打卡庐山景点'},
    '探索者': {'threshold': 3, 'icon': '🥾', 'desc': '打卡 3 个景点'},
    '旅行家': {'threshold': 6, 'icon': '🎒', 'desc': '打卡 6 个景点'},
    '庐山通': {'threshold': 10, 'icon': '🏆', 'desc': '打卡 10 个景点'},
    '征服者': {'threshold': 15, 'icon': '👑', 'desc': '打卡所有 15 个景点'},
    '自然之友': {'special': 'natural_5', 'icon': '🏞️', 'desc': '打卡 5 个自然景观'},
    '文化使者': {'special': 'cultural_3', 'icon': '🏛️', 'desc': '打卡 3 个人文景观'},
    '朝圣者': {'special': 'religious_2', 'icon': '🛕', 'desc': '打卡 2 个宗教建筑'},
}


def check_and_add_badges():
    """检查并添加徽章"""
    init_footprints()
    footprints = st.session_state[FOOTPRINTS_KEY]
    badges = st.session_state[BADGES_KEY]
    spots_data = _load_spots_data()

    new_badges = []

    # 数量徽章
    visited_count = len(footprints['visited_spots'])
    for badge_name, badge_info in BADGES.items():
        if 'threshold' in badge_info:
            if visited_count >= badge_info['threshold'] and badge_name not in badges:
                new_badges.append(badge_name)

    # 特殊徽章
    if spots_data:
        spots = spots_data.get('scenic_spots', [])
        visited_spots = [s for s in spots if s.get('id') in footprints['visited_spots']]

        natural_count = len([s for s in visited_spots if s.get('category') == '自然景观'])
        cultural_count = len([s for s in visited_spots if s.get('category') == '人文景观'])
        religious_count = len([s for s in visited_spots if s.get('category') == '宗教建筑'])

        if natural_count >= 5 and '自然之友' not in badges:
            new_badges.append('自然之友')
        if cultural_count >= 3 and '文化使者' not in badges:
            new_badges.append('文化使者')
        if religious_count >= 2 and '朝圣者' not in badges:
            new_badges.append('朝圣者')

    if new_badges:
        badges.extend(new_badges)
        st.session_state[BADGES_KEY] = badges

    return new_badges


def _load_spots_data():
    """加载景点数据"""
    import yaml
    from pathlib import Path
    DATA_DIR = Path(__file__).parent.parent / "data"
    try:
        with open(DATA_DIR / 'scenic_spots.yml', 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except:
        return None


def get_all_badges() -> List[Dict]:
    """获取所有徽章信息"""
    init_footprints()
    user_badges = st.session_state[BADGES_KEY]

    result = []
    for badge_name, badge_info in BADGES.items():
        result.append({
            'name': badge_name,
            'icon': badge_info['icon'],
            'desc': badge_info['desc'],
            'unlocked': badge_name in user_badges
        })

    return result


def render_footprint_ui():
    """渲染足迹 UI"""
    init_footprints()

    st.title("👣 我的游览足迹")
    st.markdown("记录您在庐山的每一步足迹")

    # 统计
    visited_count = get_visited_count()
    total_spots = 15

    st.progress(visited_count / total_spots)
    st.markdown(f"**已打卡**: {visited_count} / {total_spots} 个景点")

    # 徽章展示
    st.subheader("🏅 我的徽章")
    badges = get_all_badges()
    unlocked = [b for b in badges if b['unlocked']]
    locked = [b for b in badges if not b['unlocked']]

    if unlocked:
        cols = st.columns(min(len(unlocked), 4))
        for idx, badge in enumerate(unlocked):
            with cols[idx % len(cols)]:
                st.markdown(f"""
                <div style="text-align: center; padding: 10px; border: 2px solid #2E8B57; border-radius: 10px; margin: 5px;">
                    <div style="font-size: 2rem;">{badge['icon']}</div>
                    <div style="font-weight: bold; color: #2E8B57;">{badge['name']}</div>
                    <div style="font-size: 0.8rem; color: #666;">{badge['desc']}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("🔒 打卡景点解锁徽章")

    if locked:
        with st.expander(f"🔒 未解锁徽章 ({len(locked)})"):
            for badge in locked:
                st.caption(f"{badge['icon']} {badge['name']} - {badge['desc']}")

    # 打卡历史
    st.divider()
    st.subheader("📅 打卡历史")

    check_ins = get_check_in_history()
    if check_ins:
        for check_in in reversed(check_ins):
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{check_in['spot_name']}**")
                with col2:
                    st.caption(f"🕐 {check_in['check_in_time']}")
    else:
        st.info("📍 还没有打卡记录，去景点导览页面打卡吧！")

    # 重置选项
    st.divider()
    if st.button("🔄 重置所有足迹数据", type="secondary"):
        reset_footprints()
        st.success("足迹数据已重置")
        st.rerun()


def render_checkin_button(spot_id: int, spot_name: str) -> bool:
    """
    渲染打卡按钮

    Returns:
        是否执行了打卡操作
    """
    init_footprints()

    if has_visited(spot_id):
        if st.button("✅ 已打卡", disabled=True, key=f"checkin_{spot_id}"):
            pass
        return False
    else:
        if st.button("📍 打卡", key=f"checkin_{spot_id}"):
            check_in_spot(spot_id, spot_name)
            return True
    return False
