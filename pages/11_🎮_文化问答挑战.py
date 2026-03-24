"""
文化问答挑战页面 - 互动学习庐山文化
"""
import streamlit as st
import yaml
import random
from pathlib import Path

st.set_page_config(
    page_title="文化问答挑战",
    page_icon="🎮",
    layout="wide"
)

# 数据目录
DATA_DIR = Path(__file__).parent.parent / "data"

# ==================== 题库数据 ====================
# 诗词填空题目
poem_quiz_data = [
    {
        "question": "日照香炉生紫烟，__________。",
        "answer": "遥看瀑布挂前川",
        "options": ["遥看瀑布挂前川", "飞流直下三千尺", "疑是银河落九天", "瀑布挂前川"],
        "author": "李白",
        "title": "望庐山瀑布"
    },
    {
        "question": "飞流直下三千尺，__________。",
        "answer": "疑是银河落九天",
        "options": ["遥看瀑布挂前川", "飞流直下三千尺", "疑是银河落九天", "银河落九天"],
        "author": "李白",
        "title": "望庐山瀑布"
    },
    {
        "question": "人间四月芳菲尽，__________。",
        "answer": "山寺桃花始盛开",
        "options": ["山寺桃花始盛开", "桃花始盛开", "长恨春归无觅处", "不知转入此中来"],
        "author": "白居易",
        "title": "大林寺桃花"
    },
    {
        "question": "横看成岭侧成峰，__________。",
        "answer": "远近高低各不同",
        "options": ["远近高低各不同", "只缘身在此山中", "不识庐山真面目", "各不同"],
        "author": "苏轼",
        "title": "题西林壁"
    },
    {
        "question": "不识庐山真面目，__________。",
        "answer": "只缘身在此山中",
        "options": ["远近高低各不同", "只缘身在此山中", "身在此山中", "缘身在此山中"],
        "author": "苏轼",
        "title": "题西林壁"
    },
    {
        "question": "采菊东篱下，__________。",
        "answer": "悠然见南山",
        "options": ["悠然见南山", "见南山", "心远地自偏", "而无车马喧"],
        "author": "陶渊明",
        "title": "饮酒·其五"
    },
    {
        "question": "__________，性本爱丘山。",
        "answer": "少无适俗韵",
        "options": ["少无适俗韵", "性本爱丘山", "误落尘网中", "羁鸟恋旧林"],
        "author": "陶渊明",
        "title": "归园田居·其一"
    },
    {
        "question": "我本楚狂人，__________。",
        "answer": "凤歌笑孔丘",
        "options": ["凤歌笑孔丘", "手持绿玉杖", "朝别黄鹤楼", "一生好入名山游"],
        "author": "李白",
        "title": "庐山谣寄卢侍御虚舟"
    },
    {
        "question": "__________，青天削出金芙蓉。",
        "answer": "庐山东南五老峰",
        "options": ["庐山东南五老峰", "五老峰前云作堆", "庐山秀出南斗傍", "庐山高哉不可上"],
        "author": "张九龄",
        "title": "庐山寄韦荆州"
    },
    {
        "question": "五老峰前云作堆，__________。",
        "answer": "五老峰后雪成堆",
        "options": ["五老峰后雪成堆", "峰后雪成堆", "共看青天挂玉杯", "何当携取山中伴"],
        "author": "陆游",
        "title": "登庐山五老峰"
    },
    {
        "question": "__________，此中有真意。",
        "answer": "欲辨已忘言",
        "options": ["欲辨已忘言", "此中有真意", "飞鸟相与还", "山气日夕佳"],
        "author": "陶渊明",
        "title": "饮酒·其五"
    },
    {
        "question": "一山飞峙大江边，__________。",
        "answer": "跃上葱茏四百旋",
        "options": ["跃上葱茏四百旋", "冷眼向洋看世界", "热风吹雨洒江天", "云横九派浮黄鹤"],
        "author": "毛泽东",
        "title": "七律·登庐山"
    },
    {
        "question": "__________，为有源头活水来。",
        "answer": "问渠那得清如许",
        "options": ["问渠那得清如许", "半亩方塘一鉴开", "天光云影共徘徊", "源头活水来"],
        "author": "朱熹",
        "title": "白鹿洞书院"
    },
    {
        "question": "庐山东南五老峰，__________。",
        "answer": "青天削出金芙蓉",
        "options": ["青天削出金芙蓉", "九江秀色可揽结", "吾将此地巢云松", "金芙蓉"],
        "author": "张九龄",
        "title": "庐山寄韦荆州"
    },
    {
        "question": "__________，白云深处访高贤。",
        "answer": "我欲因之寻隐者",
        "options": ["我欲因之寻隐者", "人行谷底疑无路", "鸟度林间别有天", "白云深处"],
        "author": "柳宗元",
        "title": "石门涧"
    }
]

# 名人匹配题目
celebrity_quiz_data = [
    {
        "question": "哪位诗人在庐山写下'望庐山瀑布'？",
        "answer": "李白",
        "options": ["李白", "杜甫", "白居易", "苏轼"],
        "dynasty": "唐",
        "story": "李白五次游庐山，留下多首经典诗作。"
    },
    {
        "question": "谁在庐山创建东林寺，开创佛教净土宗？",
        "answer": "慧远",
        "options": ["慧远", "鉴真", "玄奘", "达摩"],
        "dynasty": "东晋",
        "story": "慧远大师于 386 年创建东林寺，使庐山成为佛教圣地。"
    },
    {
        "question": "哪位理学大师在白鹿洞书院制定学规并讲学？",
        "answer": "朱熹",
        "options": ["朱熹", "程颐", "陆九渊", "王阳明"],
        "dynasty": "南宋",
        "story": "朱熹复兴白鹿洞书院，制定《白鹿洞书院揭示》。"
    },
    {
        "question": "谁在庐山脚下隐居，写下'采菊东篱下，悠然见南山'？",
        "answer": "陶渊明",
        "options": ["陶渊明", "谢灵运", "王维", "孟浩然"],
        "dynasty": "东晋",
        "story": "陶渊明辞官归隐，在庐山脚下过着田园生活。"
    },
    {
        "question": "哪位诗人任江州司马期间，在大林寺写下桃花诗？",
        "answer": "白居易",
        "options": ["白居易", "李白", "杜甫", "李商隐"],
        "dynasty": "唐",
        "story": "白居易感慨山下春花已谢，山上桃花始开，作《大林寺桃花》。"
    },
    {
        "question": "谁写下'不识庐山真面目，只缘身在此山中'的千古名句？",
        "answer": "苏轼",
        "options": ["苏轼", "黄庭坚", "王安石", "欧阳修"],
        "dynasty": "宋",
        "story": "苏轼于 1084 年游庐山，在西林寺墙壁上题写此诗。"
    },
    {
        "question": "哪位旅行家详细记录庐山景色于《徐霞客游记》中？",
        "answer": "徐霞客",
        "options": ["徐霞客", "郦道元", "沈括", "宋应星"],
        "dynasty": "明",
        "story": "徐霞客游历庐山，详细记录三叠泉等景点。"
    },
    {
        "question": "1959 年写下'七律·登庐山'的是谁？",
        "answer": "毛泽东",
        "options": ["毛泽东", "周恩来", "陈毅", "郭沫若"],
        "dynasty": "现代",
        "story": "毛泽东在庐山会议期间登山远眺，写下此诗。"
    },
    {
        "question": "谁在庐山简寂观修道，整理道教经典？",
        "answer": "陆修静",
        "options": ["陆修静", "张道陵", "葛洪", "丘处机"],
        "dynasty": "南朝",
        "story": "陆修静在庐山简寂观修道，使庐山成为道教圣地之一。"
    },
    {
        "question": "哪位画家以画庐山松闻名？",
        "answer": "齐白石",
        "options": ["齐白石", "徐悲鸿", "张大千", "黄宾虹"],
        "dynasty": "现代",
        "story": "齐白石画庐山松，题诗'千年风骨自昂然'。"
    }
]

# 历史文化知识题目
history_quiz_data = [
    {
        "question": "庐山被列为世界遗产是在哪一年？",
        "answer": "1996 年",
        "options": ["1996 年", "1998 年", "2000 年", "1994 年"],
        "explanation": "1996 年，庐山以'庐山国家公园'之名被列入《世界遗产名录》。"
    },
    {
        "question": "白鹿洞书院始建于哪个朝代？",
        "answer": "南唐",
        "options": ["南唐", "北宋", "南宋", "唐代"],
        "explanation": "白鹿洞书院始建于南唐升元年间（940 年），距今已有 1000 多年历史。"
    },
    {
        "question": "庐山云雾茶在哪个朝代被列为贡茶？",
        "answer": "唐代",
        "options": ["唐代", "宋代", "明代", "清代"],
        "explanation": "唐代庐山云雾茶开始闻名全国，被列为贡茶。"
    },
    {
        "question": "以下哪个景点不是庐山的？",
        "answer": "飞来峰",
        "options": ["五老峰", "汉阳峰", "飞来峰", "香炉峰"],
        "explanation": "飞来峰位于杭州灵隐寺，不是庐山景点。"
    },
    {
        "question": "庐山有多少处摩崖石刻？",
        "answer": "1000 多处",
        "options": ["100 多处", "500 多处", "1000 多处", "2000 多处"],
        "explanation": "庐山有 1000 多处摩崖石刻，跨越 1500 多年历史。"
    },
    {
        "question": "东林寺是由谁创建的？",
        "answer": "慧远",
        "options": ["慧远", "慧能", "慧思", "慧海"],
        "explanation": "高僧慧远于 386 年创建东林寺，开创佛教净土宗。"
    },
    {
        "question": "庐山会议是在哪一年召开的？",
        "answer": "1959 年",
        "options": ["1958 年", "1959 年", "1960 年", "1961 年"],
        "explanation": "1959 年 7 月，中共中央在庐山召开政治局扩大会议。"
    },
    {
        "question": "庐山云雾茶获得巴拿马万国博览会金奖是在哪一年？",
        "answer": "1915 年",
        "options": ["1910 年", "1915 年", "1920 年", "1925 年"],
        "explanation": "1915 年，庐山云雾茶获巴拿马万国博览会金奖。"
    },
    {
        "question": "以下哪位名人没有在庐山留下诗词？",
        "answer": "杜甫",
        "options": ["李白", "杜甫", "苏轼", "白居易"],
        "explanation": "杜甫未曾到过庐山，但写过赞美李白庐山诗作的诗。"
    },
    {
        "question": "庐山海拔最高峰是？",
        "answer": "汉阳峰",
        "options": ["五老峰", "汉阳峰", "香炉峰", "太乙峰"],
        "explanation": "汉阳峰海拔 1474 米，是庐山最高峰。"
    },
    {
        "question": "中国四大书院之首是？",
        "answer": "白鹿洞书院",
        "options": ["白鹿洞书院", "岳麓书院", "应天书院", "嵩阳书院"],
        "explanation": "白鹿洞书院是中国古代四大书院之首。"
    },
    {
        "question": "庐山被称为'匡庐'，与哪位历史人物有关？",
        "answer": "匡俗",
        "options": ["匡俗", "匡衡", "匡章", "匡救"],
        "explanation": "传说殷周时期有匡俗兄弟七人在山中结庐隐居，故称'匡山'或'匡庐'。"
    },
    {
        "question": "《白鹿洞书院揭示》的作者是谁？",
        "answer": "朱熹",
        "options": ["朱熹", "陆九渊", "王阳明", "顾宪成"],
        "explanation": "朱熹制定《白鹿洞书院揭示》，成为后世书院教育的楷模。"
    },
    {
        "question": "庐山避暑地是由谁开辟的？",
        "answer": "李德立",
        "options": ["李德立", "李鸿章", "李宗仁", "李白"],
        "explanation": "1895 年，英国传教士李德立获准在庐山牯岭租地建房，开辟避暑地。"
    },
    {
        "question": "以下哪项不是庐山云雾茶的特点？",
        "answer": "发酵茶",
        "options": ["条索紧秀", "色泽翠绿", "发酵茶", "香气清高"],
        "explanation": "庐山云雾茶是绿茶，属于不发酵茶。"
    }
]

# ==================== 页面逻辑 ====================

st.title("🎮 文化问答挑战")
st.markdown("测试你对庐山文化的了解程度！")

# 侧边栏
st.sidebar.header("📋 选择挑战类型")
quiz_type = st.sidebar.radio(
    "选择题目类型",
    ["诗词填空", "名人匹配", "历史文化知识"],
    index=0
)

# 初始化会话状态
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'answered' not in st.session_state:
    st.session_state.answered = []
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'show_result' not in st.session_state:
    st.session_state.show_result = False
if 'selected_answer' not in st.session_state:
    st.session_state.selected_answer = None
if 'quiz_mode' not in st.session_state:
    st.session_state.quiz_mode = False

# 重置按钮
if st.sidebar.button("🔄 重置进度"):
    st.session_state.score = 0
    st.session_state.answered = []
    st.session_state.current_question = None
    st.session_state.show_result = False
    st.session_state.selected_answer = None
    st.session_state.quiz_mode = False
    st.rerun()

# 获取题库
if quiz_type == "诗词填空":
    quiz_data = poem_quiz_data
    quiz_icon = "📜"
elif quiz_type == "名人匹配":
    quiz_data = celebrity_quiz_data
    quiz_icon = "👤"
else:
    quiz_data = history_quiz_data
    quiz_icon = "📚"

# 显示进度
total_questions = len(quiz_data)
answered_count = len([q for q in st.session_state.answered if q in [i for i, d in enumerate(quiz_data)]])
st.sidebar.markdown(f"**进度**: {answered_count}/{total_questions}")
st.sidebar.markdown(f"**得分**: {st.session_state.score}分")

# 进度条
progress = answered_count / total_questions
st.sidebar.progress(progress)

st.sidebar.divider()

# 开始按钮
if not st.session_state.quiz_mode:
    if st.sidebar.button(f"🚀 开始 {quiz_type} 挑战"):
        st.session_state.quiz_mode = True
        st.session_state.score = 0
        st.session_state.answered = []
        st.session_state.current_question = None
        st.rerun()
else:
    # 获取未回答的题目
    available_questions = [i for i in range(len(quiz_data)) if i not in st.session_state.answered]

    if available_questions:
        # 如果没有当前题目，随机选择一个
        if st.session_state.current_question is None:
            st.session_state.current_question = random.choice(available_questions)

        current_q = quiz_data[st.session_state.current_question]

        # 显示题目
        st.markdown(f"### {quiz_icon} {current_q['question']}")

        # 打乱选项
        if 'shuffled_options' not in st.session_state:
            options = current_q['options'].copy()
            random.shuffle(options)
            st.session_state.shuffled_options = options

        # 显示选项
        cols = st.columns(2)
        for i, option in enumerate(st.session_state.shuffled_options):
            col_idx = i % 2
            with cols[col_idx]:
                if st.button(option, key=f"option_{i}", use_container_width=True):
                    st.session_state.selected_answer = option
                    st.session_state.show_result = True
                    st.rerun()

        # 显示结果
        if st.session_state.show_result and st.session_state.selected_answer:
            st.divider()
            if st.session_state.selected_answer == current_q['answer']:
                st.success(f"✅ 回答正确！+10 分")
                st.session_state.score += 10
                if current_q.get('author'):
                    st.info(f"📖 出自 {current_q['author']} 的《{current_q.get('title', '')}》")
                if current_q.get('story'):
                    with st.expander("📚 背景知识"):
                        st.write(current_q['story'])
                if current_q.get('explanation'):
                    with st.expander("💡 解析"):
                        st.write(current_q['explanation'])
            else:
                st.error(f"❌ 回答错误！正确答案是：**{current_q['answer']}**")
                if current_q.get('author'):
                    st.info(f"📖 出自 {current_q['author']} 的《{current_q.get('title', '')}》")
                if current_q.get('story'):
                    with st.expander("📚 背景知识"):
                        st.write(current_q['story'])
                if current_q.get('explanation'):
                    with st.expander("💡 解析"):
                        st.write(current_q['explanation'])

            # 记录已回答
            st.session_state.answered.append(st.session_state.current_question)
            st.session_state.show_result = False
            st.session_state.selected_answer = None
            st.session_state.current_question = None
            st.session_state.shuffled_options = None

            st.divider()
            if st.button("下一题 →"):
                st.rerun()
            else:
                st.stop()
    else:
        # 所有题目已完成
        st.success("🎉 恭喜！你已完成所有题目！")
        st.markdown(f"### 🏆 最终得分：{st.session_state.score}分")

        # 评价
        max_score = len(quiz_data) * 10
        accuracy = st.session_state.score / max_score

        if accuracy >= 0.9:
            st.balloons()
            st.markdown("### 🌟 评价：庐山文化大师！")
            st.write("你对庐山文化了如指掌，简直是专家级别！")
        elif accuracy >= 0.7:
            st.markdown("### 🌟 评价：庐山文化达人！")
            st.write("你对庐山文化有很好的了解，继续加油！")
        elif accuracy >= 0.5:
            st.markdown("### 🌟 评价：庐山文化学习者！")
            st.write("你对庐山文化有一定了解，可以多学习哦！")
        else:
            st.markdown("### 🌟 评价：庐山文化新手！")
            st.write("继续努力，多了解庐山文化吧！")

        # 重新开始
        st.divider()
        if st.button("🔄 重新开始"):
            st.session_state.score = 0
            st.session_state.answered = []
            st.session_state.current_question = None
            st.session_state.show_result = False
            st.session_state.selected_answer = None
            st.rerun()

# 排名系统
st.sidebar.divider()
st.sidebar.markdown("### 🏅 等级称号")

if st.session_state.score >= 500:
    st.sidebar.success("🏆 庐山文化泰斗")
elif st.session_state.score >= 300:
    st.sidebar.success("🥇 庐山文化大师")
elif st.session_state.score >= 200:
    st.sidebar.info("🥈 庐山文化达人")
elif st.session_state.score >= 100:
    st.sidebar.info("🥉 庐山文化学习者")
else:
    st.sidebar.caption("🌱 庐山文化新手")

# 底部统计
st.divider()
col1, col2, col3 = st.columns(3)
col1.metric("总题数", len(quiz_data))
col2.metric("已答题", len(st.session_state.answered))
col3.metric("正确率", f"{int(st.session_state.score / 10 / max(len(st.session_state.answered), 1) * 100)}%" if st.session_state.answered else "0%")
