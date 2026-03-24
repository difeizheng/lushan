"""
天气工具模块
提供实时天气查询功能
"""
import requests
from typing import Optional, Dict, Any
from datetime import datetime


# 使用 Open-Meteo 免费天气 API（无需 API Key）
# 文档：https://open-meteo.com/

# 庐山牯岭镇坐标
LUSHAN_LAT = 29.5683
LUSHAN_LNG = 115.9850


def get_current_weather(lat: float = LUSHAN_LAT, lng: float = LUSHAN_LNG) -> Optional[Dict[str, Any]]:
    """
    获取当前位置的实时天气

    Args:
        lat: 纬度
        lng: 经度

    Returns:
        天气数据字典，失败返回 None
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lng,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "weather_code",
            "wind_speed_10m",
            "wind_direction_10m",
            "precipitation"
        ],
        "daily": [
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_probability_max",
            "sunrise",
            "sunset"
        ],
        "timezone": "Asia/Shanghai",
        "forecast_days": 3
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # 解析当前天气
        current = data.get('current', {})
        daily = data.get('daily', {})

        return {
            'temperature': current.get('temperature_2m'),
            'feels_like': current.get('apparent_temperature'),
            'humidity': current.get('relative_humidity_2m'),
            'weather_code': current.get('weather_code'),
            'weather_desc': get_weather_description(current.get('weather_code', 0)),
            'wind_speed': current.get('wind_speed_10m'),
            'wind_direction': current.get('wind_direction_10m'),
            'precipitation': current.get('precipitation'),
            'forecast': parse_forecast(daily),
            'update_time': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
    except Exception as e:
        print(f"获取天气数据失败：{e}")
        return None


def get_weather_description(code: int) -> str:
    """
    根据 WMO 天气代码获取天气描述

    WMO Weather interpretation codes (WW)
    """
    weather_codes = {
        0: "晴朗",
        1: "主要晴朗",
        2: "部分多云",
        3: "阴天",
        45: "雾",
        48: "雾凇",
        51: "毛毛雨",
        53: "中毛毛雨",
        55: "大毛毛雨",
        61: "小雨",
        63: "中雨",
        65: "大雨",
        71: "小雪",
        73: "中雪",
        75: "大雪",
        77: "雪粒",
        80: "小阵雨",
        81: "中阵雨",
        82: "大阵雨",
        85: "小雪阵",
        86: "大雪阵",
        95: "雷雨",
        96: "雷阵雨",
        99: "大雷阵雨"
    }
    return weather_codes.get(code, "未知")


def get_weather_icon(code: int) -> str:
    """根据天气代码获取 emoji 图标"""
    if code == 0:
        return "☀️"
    elif code <= 2:
        return "🌤️"
    elif code == 3:
        return "☁️"
    elif code <= 48:
        return "🌫️"
    elif code <= 67:
        return "🌧️"
    elif code <= 77:
        return "❄️"
    elif code <= 82:
        return "🌦️"
    elif code <= 99:
        return "⛈️"
    return "🌡️"


def parse_forecast(daily: Dict) -> list:
    """解析天气预报数据"""
    forecast = []
    if not daily:
        return forecast

    dates = daily.get('time', [])
    max_temps = daily.get('temperature_2m_max', [])
    min_temps = daily.get('temperature_2m_min', [])
    weather_codes = daily.get('weather_code', [])
    precip_probs = daily.get('precipitation_probability_max', [])

    for i in range(min(len(dates), 3)):
        forecast.append({
            'date': dates[i] if i < len(dates) else None,
            'max_temp': max_temps[i] if i < len(max_temps) else None,
            'min_temp': min_temps[i] if i < len(min_temps) else None,
            'weather_code': weather_codes[i] if i < len(weather_codes) else None,
            'weather_desc': get_weather_description(weather_codes[i] if i < len(weather_codes) else 0),
            'weather_icon': get_weather_icon(weather_codes[i] if i < len(weather_codes) else 0),
            'precip_prob': precip_probs[i] if i < len(precip_probs) else None
        })

    return forecast


def get_clothing_advice(temp: Optional[float], weather_code: int = 0) -> str:
    """
    根据温度给出穿衣建议

    Args:
        temp: 当前温度
        weather_code: 天气代码

    Returns:
        穿衣建议字符串
    """
    if temp is None:
        return "请根据实际天气情况适当增减衣物"

    if temp >= 28:
        return "炎热，建议穿短袖、短裤、裙子，注意防晒和补水"
    elif temp >= 24:
        return "温暖，建议穿短袖或薄长袖，携带防晒用品"
    elif temp >= 20:
        return "舒适，建议穿长袖 T 恤、薄外套"
    elif temp >= 15:
        return "凉爽，建议穿外套、风衣，可携带薄毛衣"
    elif temp >= 10:
        return "较凉，建议穿厚外套、毛衣，注意保暖"
    elif temp >= 5:
        return "寒冷，建议穿厚毛衣、棉衣、羽绒服"
    else:
        return "非常寒冷，建议穿厚羽绒服、保暖内衣，戴帽子手套"


def get_travel_advice(weather_code: int, precip_prob: int = 0) -> str:
    """
    根据天气给出旅游建议

    Args:
        weather_code: 天气代码
        precip_prob: 降水概率

    Returns:
        旅游建议字符串
    """
    if weather_code == 0 or weather_code == 1:
        return "天气晴好，非常适合户外活动，是游览庐山的好时机！"
    elif weather_code <= 3:
        return "天气尚可，适合游览，但观景效果可能略受影响。"
    elif weather_code <= 48:
        return "有雾天气，能见度较低，登山时请注意安全，但可能看到云海景观。"
    elif weather_code <= 67:
        if precip_prob > 50:
            return "有降雨可能，建议携带雨具，路面湿滑请注意安全。"
        return "可能有小雨，建议携带雨具，瀑布水量会增大。"
    elif weather_code <= 77:
        return "可能有降雪，路面结冰风险大，请注意防滑保暖。"
    elif weather_code >= 95:
        return "雷雨天气，不建议进行户外活动，请在室内躲避。"
    return "天气一般，请根据实际情况安排行程。"
