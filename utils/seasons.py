"""
四季主题模块
根据当前月份自动切换主题色和推荐内容
"""
from datetime import datetime
from typing import Dict, List, Tuple


# 四季主题配置
THEMES = {
    'spring': {
        'name': '春季',
        'months': [3, 4, 5],
        'primary_color': '#FFB7C5',  # 樱花粉
        'secondary_color': '#98D8C8',
        'icon': '🌸',
        'description': '山花烂漫，春意盎然',
        'best_spots': ['花径', '锦绣谷', '如琴湖'],
        'activities': ['赏花', '踏青', '摄影'],
        'clothing': '春装外套、薄毛衣，携带雨具',
        'tips': '春季多雨，请携带雨具。4 月是桃花盛开的最佳时期。'
    },
    'summer': {
        'name': '夏季',
        'months': [6, 7, 8],
        'primary_color': '#7BC9A6',  # 清凉绿
        'secondary_color': '#00B4D8',
        'icon': '🌋',
        'description': '清凉避暑，瀑布壮观',
        'best_spots': ['三叠泉', '含鄱口', '五老峰'],
        'activities': ['避暑', '观瀑布', '看日出'],
        'clothing': '短袖、薄裤，早晚加薄外套',
        'tips': '夏季是避暑旺季，游客较多。瀑布水量充沛，非常壮观。'
    },
    'autumn': {
        'name': '秋季',
        'months': [9, 10, 11],
        'primary_color': '#F4A460',  # 枫叶橙
        'secondary_color': '#8B4513',
        'icon': '🍁',
        'description': '天高气爽，红叶满山',
        'best_spots': ['五老峰', '汉阳峰', '含鄱口'],
        'activities': ['登高', '观景', '摄影'],
        'clothing': '长袖 T 恤、外套，登山鞋',
        'tips': '秋季是最佳旅游季节，天气稳定，适合登高观景。'
    },
    'winter': {
        'name': '冬季',
        'months': [12, 1, 2],
        'primary_color': '#B8E6F5',  # 冰雪蓝
        'secondary_color': '#E8E8E8',
        'icon': '❄️',
        'description': '雾凇雪景，银装素裹',
        'best_spots': ['含鄱口', '五老峰', '汉阳峰'],
        'activities': ['赏雪', '观雾凇', '泡温泉'],
        'clothing': '羽绒服、保暖内衣，帽子手套围巾',
        'tips': '冬季部分景点可能因雪关闭，请注意安全。有机会观赏到美丽的雾凇。'
    }
}


def get_current_season() -> str:
    """获取当前季节"""
    month = datetime.now().month

    if month in THEMES['spring']['months']:
        return 'spring'
    elif month in THEMES['summer']['months']:
        return 'summer'
    elif month in THEMES['autumn']['months']:
        return 'autumn'
    else:
        return 'winter'


def get_season_info(season: str = None) -> Dict:
    """获取季节信息"""
    if season is None:
        season = get_current_season()
    return THEMES.get(season, THEMES['spring'])


def get_season_recommendations(season: str = None) -> Dict:
    """获取季节推荐"""
    info = get_season_info(season)
    return {
        'best_spots': info['best_spots'],
        'activities': info['activities'],
        'clothing': info['clothing'],
        'tips': info['tips']
    }


def get_season_css(season: str = None) -> str:
    """获取季节 CSS 样式"""
    info = get_season_info(season)

    return f"""
    <style>
        .season-theme {{
            --primary-color: {info['primary_color']};
            --secondary-color: {info['secondary_color']};
        }}
        .season-header {{
            background: linear-gradient(135deg, {info['primary_color']}, {info['secondary_color']});
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}
    </style>
    """


def render_season_banner():
    """渲染季节横幅"""
    info = get_season_info()

    return f"""
    <div style="background: linear-gradient(135deg, {info['primary_color']}, {info['secondary_color']});
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                margin: 10px 0;">
        <div style="font-size: 2rem; font-weight: bold; color: white;">
            {info['icon']} {info['name']}的庐山
        </div>
        <div style="font-size: 1rem; color: white; margin-top: 5px;">
            {info['description']}
        </div>
    </div>
    """


def get_flower_forecast() -> Dict[str, str]:
    """
    获取花期预报

    Returns:
        花卉名称到花期状态的映射
    """
    month = datetime.now().month

    forecasts = {
        '桃花': '未开放',
        '杜鹃花': '未开放',
        '荷花': '未开放',
        '菊花': '未开放',
        '梅花': '未开放'
    }

    if month == 3:
        forecasts['桃花'] = '含苞待放'
        forecasts['梅花'] = '盛开末期'
    elif month == 4:
        forecasts['桃花'] = '盛开期'
        forecasts['杜鹃花'] = '初开'
    elif month == 5:
        forecasts['桃花'] = '已谢'
        forecasts['杜鹃花'] = '盛开期'
    elif month == 6:
        forecasts['杜鹃花'] = '盛开末期'
        forecasts['荷花'] = '初开'
    elif month in [7, 8]:
        forecasts['荷花'] = '盛开期'
    elif month in [10, 11]:
        forecasts['菊花'] = '盛开期'
    elif month in [12, 1]:
        forecasts['梅花'] = '含苞待放'
    elif month == 2:
        forecasts['梅花'] = '盛开期'

    return forecasts


def is_best_time_to_visit() -> Tuple[bool, str]:
    """
    判断是否是最佳旅游时间

    Returns:
        (是否最佳时间，原因说明)
    """
    season = get_current_season()

    if season == 'spring':
        return True, "春季山花烂漫，气温适宜，是赏花踏青的好时节"
    elif season == 'summer':
        return True, "夏季凉爽宜人，是避暑观景的最佳季节"
    elif season == 'autumn':
        return True, "秋季天高气爽，红叶满山，适合登高摄影"
    else:
        return False, "冬季较冷，但可观赏雪景和雾凇，别有风味"
