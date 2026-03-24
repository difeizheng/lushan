"""
实用信息页面 - 包含天气、交通、门票、紧急联系、美食住宿
"""
import streamlit as st
from datetime import datetime
from utils.weather import get_current_weather, get_weather_icon, get_clothing_advice, get_travel_advice
import yaml
from pathlib import Path

st.set_page_config(
    page_title="实用信息",
    page_icon="🛠️",
    layout="wide"
)

# 数据目录
DATA_DIR = Path(__file__).parent.parent / "data"

@st.cache_data
def load_data(file_name: str):
    """加载 YAML 数据文件"""
    file_path = DATA_DIR / file_name
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        return None

# 标题
st.title("🛠️ 实用信息")
st.markdown("庐山旅游必备的实用信息")

# 标签页
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🌤️ 实时天气", "🍜 美食推荐", "🏨 住宿指南", "🚌 交通指南", "📞 紧急联系"])

# ==================== 实时天气 ====================
with tab1:
    st.header("🌤️ 实时天气")

    # 获取实时天气
    @st.cache_data(ttl=1800)  # 30 分钟缓存
    def fetch_weather():
        return get_current_weather()

    weather_data = fetch_weather()

    if weather_data:
        # 天气卡片
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "当前温度",
                f"{weather_data['temperature']}°C",
                f"体感 {weather_data['feels_like']}°C"
            )

        with col2:
            st.metric("湿度", f"{weather_data['humidity']}%")

        with col3:
            st.metric("风速", f"{weather_data['wind_speed']} km/h")

        with col4:
            st.metric("降水", f"{weather_data.get('precipitation', 0)} mm")

        # 天气状况和穿衣建议
        st.divider()

        col1, col2 = st.columns([1, 2])

        with col1:
            weather_icon = get_weather_icon(weather_data['weather_code'])
            st.markdown(f"""
            <div style="text-align: center; padding: 20px;">
                <div style="font-size: 4rem;">{weather_icon}</div>
                <div style="font-size: 1.5rem; font-weight: bold;">{weather_data['weather_desc']}</div>
                <div style="color: #666; margin-top: 10px;">
                    更新于 {weather_data['update_time']}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            # 穿衣建议
            st.subheader("👔 穿衣建议")
            clothing_advice = get_clothing_advice(
                weather_data['temperature'],
                weather_data['weather_code']
            )
            st.info(clothing_advice)

            # 旅游建议
            st.subheader("🎯 旅游建议")
            precip_prob = weather_data.get('forecast', [{}])[0].get('precip_prob', 0)
            travel_advice = get_travel_advice(
                weather_data['weather_code'],
                precip_prob
            )
            st.success(travel_advice)

        # 三天天气预报
        st.divider()
        st.subheader("📅 三天天气预报")

        forecast = weather_data.get('forecast', [])
        if forecast:
            cols = st.columns(3)
            for i, day in enumerate(forecast):
                with cols[i]:
                    with st.container(border=True):
                        st.markdown(f"**{day['date']}**")
                        st.markdown(f"<div style='font-size: 2.5rem; text-align: center;'>{day['weather_icon']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='text-align: center;'>{day['weather_desc']}</div>", unsafe_allow_html=True)
                        st.markdown(f"""
                        <div style='text-align: center; color: #666;'>
                            高温 {day['max_temp']}°C | 低温 {day['min_temp']}°C<br>
                            降水概率 {day['precip_prob']}%
                        </div>
                        """, unsafe_allow_html=True)

    else:
        st.warning("暂时无法获取实时天气数据，请稍后重试")

    # 季节穿衣建议
    st.divider()
    st.subheader("📊 庐山气候特点")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **春季**（3-5 月）
        - 温暖湿润，山花烂漫
        - 建议：春装外套、薄毛衣
        - 携带雨具（春季多雨）

        **夏季**（6-8 月）
        - 凉爽宜人，避暑胜地
        - 建议：短袖、薄裤、薄外套
        - 必备：防晒霜、遮阳帽
        """)

    with col2:
        st.markdown("""
        **秋季**（9-11 月）
        - 天高气爽，红叶满山
        - 建议：长袖 T 恤、外套
        - 最佳摄影季节

        **冬季**（12-2 月）
        - 偶有降雪，可赏雾凇
        - 建议：羽绒服、保暖内衣
        - 携带：帽子、手套、围巾
        """)

# ==================== 美食推荐 ====================
with tab2:
    st.header("🍜 美食推荐")
    st.markdown("品尝庐山地道风味")

    restaurants_data = load_data("restaurants.yml")

    if restaurants_data:
        restaurants = restaurants_data.get('restaurants', [])

        # 筛选
        col1, col2 = st.columns(2)
        with col1:
            categories = ["全部"] + list(set(r.get('category', '') for r in restaurants))
            selected_category = st.selectbox("菜品分类", categories)

        with col2:
            price_ranges = ["全部"] + ["¥", "¥¥", "¥¥¥", "¥¥¥¥"]
            selected_price = st.selectbox("价格区间", price_ranges, key="restaurant_price")

        # 筛选
        filtered = restaurants
        if selected_category != "全部":
            filtered = [r for r in filtered if r.get('category') == selected_category]
        if selected_price != "全部":
            filtered = [r for r in filtered if r.get('price_range') == selected_price]

        st.markdown(f"**找到 {len(filtered)} 家餐厅**")

        # 展示餐厅
        for restaurant in filtered:
            with st.container(border=True):
                col1, col2, col3 = st.columns([3, 1, 1])

                with col1:
                    st.markdown(f"### {restaurant.get('name', '未知')}")
                    st.caption(f"{restaurant.get('category')} | {restaurant.get('price_range', 'N/A')}")

                with col2:
                    st.metric("评分", f"⭐ {restaurant.get('rating', 'N/A')}")

                with col3:
                    avg_price = restaurant.get('avg_price', 0)
                    st.metric("人均", f"¥{avg_price}")

                st.write(restaurant.get('description', '')[:100] + "...")

                # 招牌菜
                if restaurant.get('signature_dishes'):
                    st.markdown("**🥢 招牌菜**: " + "、".join(restaurant['signature_dishes']))

                # 基本信息
                col1, col2 = st.columns(2)
                with col1:
                    if restaurant.get('address'):
                        st.caption(f"📍 {restaurant['address']}")
                with col2:
                    if restaurant.get('opening_hours'):
                        st.caption(f"🕐 {restaurant['opening_hours']}")

    else:
        st.info("暂无美食数据")

# ==================== 住宿指南 ====================
with tab3:
    st.header("🏨 住宿指南")
    st.markdown("选择适合您的住宿")

    hotels_data = load_data("hotels.yml")

    if hotels_data:
        hotels = hotels_data.get('hotels', [])

        # 筛选
        col1, col2 = st.columns(2)
        with col1:
            categories = ["全部"] + list(set(h.get('category', '') for h in hotels))
            selected_category = st.selectbox("住宿类型", categories)

        with col2:
            price_ranges = ["全部"] + ["¥", "¥¥", "¥¥¥", "¥¥¥¥"]
            selected_price = st.selectbox("价格区间", price_ranges, key="hotel_price")

        # 筛选
        filtered = hotels
        if selected_category != "全部":
            filtered = [h for h in filtered if h.get('category') == selected_category]
        if selected_price != "全部":
            filtered = [h for h in filtered if h.get('price_range') == selected_price]

        st.markdown(f"**找到 {len(filtered)} 家住宿**")

        # 展示住宿
        for hotel in filtered:
            with st.container(border=True):
                col1, col2, col3 = st.columns([3, 1, 1])

                with col1:
                    st.markdown(f"### {hotel.get('name', '未知')}")
                    st.caption(f"{hotel.get('category')} | {hotel.get('price_range', 'N/A')}")

                with col2:
                    st.metric("评分", f"⭐ {hotel.get('rating', 'N/A')}")

                with col3:
                    avg_price = hotel.get('avg_price', 0)
                    st.metric("每晚", f"¥{avg_price}起")

                st.write(hotel.get('description', '')[:100] + "...")

                # 设施
                if hotel.get('amenities'):
                    st.markdown("**🛎️ 设施**: " + "、".join(hotel['amenities']))

                # 基本信息
                col1, col2 = st.columns(2)
                with col1:
                    if hotel.get('address'):
                        st.caption(f"📍 {hotel['address']}")
                with col2:
                    if hotel.get('phone'):
                        st.caption(f"📞 {hotel['phone']}")

        # 住宿建议
        st.divider()
        st.subheader("💡 住宿建议")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.info("""
            **🏆 追求品质**
            - 庐山大酒店
            - 如琴湖度假村
            """)

        with col2:
            st.info("""
            **💰 性价比高**
            - 牯岭民宿
            - 云海客栈
            """)

        with col3:
            st.info("""
            **🎒 经济实惠**
            - 青年旅舍
            - 白鹿洞书院宾馆
            """)

    else:
        st.info("暂无住宿数据")

# ==================== 交通指南 ====================
with tab4:
    st.header("🚌 交通指南")

    st.markdown("""
    ### 如何到达庐山

    #### ✈️ 飞机
    - **南昌昌北国际机场**：距离庐山约 120 公里，有高速直达
    - **九江庐山机场**：距离庐山约 40 公里
    - 机场出来后都有巴士或出租车可前往庐山

    #### 🚄 火车
    - **九江站**：从九江汽车站乘车上山，约 1 小时
    - **庐山站**：从庐山汽车站乘车上山
    - 建议提前预订火车票，特别是旅游旺季

    #### 🚗 汽车
    - **九江汽车站**：有直达庐山牯岭的班车
    - **南昌**：有直达庐山的长途汽车
    - 自驾游客可将车停放在庐山换乘中心，然后换乘景区交通

    #### 🚡 索道
    - **庐山索道**：2017 年开通，从九江县可直达牯岭
    - 全程约 10 分钟，票价约 100 元/人
    - 运营时间：7:00-17:30（季节可能有所调整）
    """)

    st.divider()

    st.markdown("""
    ### 庐山内部交通

    #### 景区观光车
    - **票价**：约 90 元/人（含主要景点）
    - **线路**：覆盖主要景点
    - **运营时间**：7:00-17:30

    #### 出租车/网约车
    - 牯岭镇内有出租车
    - 可包车游览，价格约 200-400 元/天

    #### 徒步
    - 部分景点之间适合徒步
    - 锦绣谷、五老峰等需要步行
    """)

    # 交通费用估算
    st.divider()
    st.subheader("💰 交通费用估算")

    st.markdown("""
    | 交通方式 | 单程费用 | 备注 |
    |---------|---------|------|
    | 九江 - 庐山班车 | ~20 元 | 经济实惠 |
    | 索道 | ~100 元 | 快速便捷 |
    | 出租车（九江 - 庐山）| ~200 元 | 适合多人拼车 |
    | 景区观光车 | ~90 元 | 通票 |
    | 包车游览 | ~200-400 元/天 | 灵活自由 |
    """)

# ==================== 紧急联系 ====================
with tab5:
    st.header("📞 紧急联系")

    st.markdown("""
    ### 紧急电话

    | 服务 | 电话号码 |
    |------|---------|
    | 报警 | 110 |
    | 急救 | 120 |
    | 火警 | 119 |
    | 旅游投诉 | 12301 |
    """)

    st.divider()

    st.markdown("""
    ### 庐山景区服务电话

    | 服务 | 电话 |
    |------|------|
    | 景区咨询 | 0792-828xxxx |
    | 投诉电话 | 0792-828xxxx |
    | 救援电话 | 0792-828xxxx |
    | 索道咨询 | 0792-828xxxx |

    > 💡 提示：以上电话为示例，实际号码请查询景区官网
    """)

    st.divider()

    st.markdown("""
    ### 医疗机构

    - **庐山人民医院**：牯岭镇
    - **庐山急救中心**：牯岭镇
    - 各主要景点设有医疗点

    ### 派出所

    - **庐山风景区派出所**：牯岭镇
    - 各主要景点有警务点
    """)

    # 实用提示
    st.divider()
    st.subheader("💡 实用提示")

    st.markdown("""
    1. **保存紧急联系人电话**
    2. **结伴而行，不要单独行动**
    3. **注意保管好随身物品**
    4. **遵守景区规定，不要攀爬危险区域**
    5. **如遇紧急情况，保持冷静，及时求助**
    """)

# 页脚
st.divider()
st.info("💡 提示：以上信息仅供参考，具体信息请以景区官方公布为准。建议出行前查询最新信息。")
