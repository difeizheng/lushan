"""
工具函数模块
"""
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional

# 子模块
from .weather import (
    get_current_weather,
    get_weather_description,
    get_weather_icon,
    get_clothing_advice,
    get_travel_advice
)

__all__ = [
    # 数据加载
    'load_yaml_data',
    'get_scenic_spots',
    'get_celebrities',
    'get_poems',
    'get_routes',
    # 工具函数
    'filter_spots_by_category',
    'search_spots',
    'get_spot_by_id',
    'get_poems_by_author',
    'format_altitude',
    'get_difficulty_emoji',
    'get_category_icon',
    # 天气函数
    'get_current_weather',
    'get_weather_description',
    'get_weather_icon',
    'get_clothing_advice',
    'get_travel_advice'
]

# 数据目录
DATA_DIR = Path(__file__).parent.parent / "data"


def load_yaml_data(file_name: str) -> Optional[Dict]:
    """加载 YAML 数据文件"""
    file_path = DATA_DIR / file_name
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"加载数据失败：{e}")
        return None


def get_scenic_spots() -> List[Dict[str, Any]]:
    """获取所有景点数据"""
    data = load_yaml_data("scenic_spots.yml")
    if data:
        return data.get('scenic_spots', [])
    return []


def get_celebrities() -> List[Dict[str, Any]]:
    """获取所有名人数据"""
    data = load_yaml_data("celebrities.yml")
    if data:
        return data.get('celebrities', [])
    return []


def get_poems() -> List[Dict[str, Any]]:
    """获取所有诗词数据"""
    data = load_yaml_data("poems.yml")
    if data:
        return data.get('poems', [])
    return []


def get_routes() -> List[Dict[str, Any]]:
    """获取所有路线数据"""
    data = load_yaml_data("routes.yml")
    if data:
        return data.get('routes', [])
    return []


def filter_spots_by_category(spots: List[Dict], category: str) -> List[Dict]:
    """按分类筛选景点"""
    return [s for s in spots if s.get('category') == category]


def search_spots(spots: List[Dict], keyword: str) -> List[Dict]:
    """搜索景点"""
    keyword = keyword.lower()
    results = []
    for spot in spots:
        if (keyword in spot.get('name', '').lower() or
            keyword in spot.get('description', '').lower() or
            keyword in ' '.join(spot.get('tags', []))):
            results.append(spot)
    return results


def get_spot_by_id(spot_id: int) -> Optional[Dict]:
    """根据 ID 获取景点"""
    spots = get_scenic_spots()
    for spot in spots:
        if spot.get('id') == spot_id:
            return spot
    return None


def get_poems_by_author(poems: List[Dict], author: str) -> List[Dict]:
    """获取作者的所有诗词"""
    return [p for p in poems if p.get('author') == author]


def format_altitude(altitude: Optional[int]) -> str:
    """格式化海拔高度"""
    if altitude:
        return f"{altitude}米"
    return "未知"


def get_difficulty_emoji(difficulty: str) -> str:
    """获取难度对应的 emoji"""
    emojis = {
        '简单': '🟢',
        '中等': '🟡',
        '较难': '🔴'
    }
    return emojis.get(difficulty, '⚪')


def get_category_icon(category: str) -> str:
    """获取分类对应的图标"""
    icons = {
        '自然景观': '🏞️',
        '人文景观': '🏛️',
        '宗教建筑': '🛕'
    }
    return icons.get(category, '📍')
