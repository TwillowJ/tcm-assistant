import streamlit as st
import os
from llm_service import TCMAnalyzer

# 页面配置
st.set_page_config(
    page_title="中医智能小助手",
    page_icon="🏥",
    layout="wide"
)

# 欢迎横幅 - 简洁版
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
    <h1 style="color: white; margin: 0; text-align: center; font-size: 32px;">🌿 中医智能小助手</h1>
    <p style="color: #f0f0f0; text-align: center; margin-top: 12px; font-size: 16px; opacity: 0.95;">
        结合传统中医智慧与现代AI技术，为您提供个性化养生建议
    </p>
</div>
""", unsafe_allow_html=True)

# 免责声明 - 紧凑显示
st.warning("⚠️ **免责声明：** 本应用仅提供养生保健参考建议，不能替代专业医疗诊断和治疗。如有严重或持续症状，请及时就医咨询专业医师。")

# 症状输入区域
st.markdown("### 📝 症状描述")

# 使用session_state存储选中的症状
if 'selected_symptoms' not in st.session_state:
    st.session_state.selected_symptoms = []

# 精简的常见症状列表 - 只保留最常见的症状
common_symptoms = [
    "疲劳乏力", "失眠多梦", "入睡困难", "食欲不振", "腹胀",
    "便秘", "腹泻", "头痛", "头晕", "焦虑",
    "心烦", "腰痛", "关节痛", "胸闷", "心悸",
    "怕冷", "怕热", "出汗异常", "口干"
]

# 常见症状快速选择 - 无标题，直接显示
with st.container():
    # 创建紧凑的可选择症状标签
    cols = st.columns(5)
    for idx, symptom in enumerate(common_symptoms):
        col_idx = idx % 5
        with cols[col_idx]:
            # 判断是否已选中
            is_selected = symptom in st.session_state.selected_symptoms
            button_type = "primary" if is_selected else "secondary"

            if st.button(
                f"{'✓ ' if is_selected else ''}{symptom}",
                key=f"symptom_{symptom}",
                use_container_width=True,
                type=button_type
            ):
                # 切换选中状态
                if symptom in st.session_state.selected_symptoms:
                    st.session_state.selected_symptoms.remove(symptom)
                else:
                    st.session_state.selected_symptoms.append(symptom)
                st.rerun()

# 显示已选症状（如果有）
if st.session_state.selected_symptoms:
    st.markdown("<br>", unsafe_allow_html=True)
    selected_html = " ".join([
        f'<span style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); '
        f'color: white; padding: 5px 12px; border-radius: 15px; margin: 3px; '
        f'display: inline-block; font-size: 14px;">{s}</span>'
        for s in st.session_state.selected_symptoms
    ])
    st.markdown(f'<div style="margin-bottom: 10px;">已选症状：{selected_html}</div>', unsafe_allow_html=True)

# 大文本输入框 - 不再自动填充选中的症状
st.markdown("<br>", unsafe_allow_html=True)
additional_symptoms = st.text_area(
    "补充详细症状描述（可选）",
    value="",
    placeholder="可以在此输入更详细的症状描述...\n例如：疲劳症状主要出现在下午，晚上入睡需要1小时以上，睡眠中容易醒来...",
    height=180,
    help="症状描述越详细，AI分析越准确。可以只选择上方症状，或只输入文本，或两者结合。",
    key="additional_symptoms"
)

# 添加一些可选的补充信息
st.markdown("#### 补充信息（可选）")

col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("年龄", min_value=1, max_value=120, value=30)

with col2:
    gender = st.selectbox("性别", ["男", "女", "不方便透露"])

with col3:
    duration = st.selectbox(
        "症状持续时间",
        ["1-3天", "1周左右", "2-4周", "1-3个月", "3个月以上"]
    )

st.markdown("---")

# 分析按钮
analyze_button = st.button("🔍 开始分析", type="primary", use_container_width=True)

# 结果展示区域
if analyze_button:
    # 合并选中的症状和文本框输入
    combined_symptoms = ""
    if st.session_state.selected_symptoms:
        combined_symptoms = "、".join(st.session_state.selected_symptoms)
    if additional_symptoms.strip():
        if combined_symptoms:
            combined_symptoms += "。" + additional_symptoms.strip()
        else:
            combined_symptoms = additional_symptoms.strip()

    if not combined_symptoms:
        st.error("❌ 请至少选择一个症状或输入症状描述")
    else:
        try:
            # 初始化分析器
            analyzer = TCMAnalyzer()

            # 显示加载状态并调用LLM API
            with st.spinner("🤖 AI正在分析您的症状，请稍候..."):
                # 使用流式输出获得更好的用户体验
                full_response = ""

                # 流式获取分析结果
                for chunk in analyzer.analyze_streaming(
                    symptoms=combined_symptoms,
                    age=int(age),
                    gender=gender,
                    duration=duration
                ):
                    full_response += chunk

            # 分块显示结果 - 美化输出
            # 分离中医辨证分析和养生建议
            sections = full_response.split("## 二、个性化养生建议")

            if len(sections) >= 2:
                # 第一部分：中医辨证分析
                st.markdown("""
                <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                            padding: 20px;
                            border-radius: 10px;
                            margin: 20px 0;">
                    <h3 style="color: white; margin: 0;">🔍 中医辨证分析</h3>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(sections[0].replace("## 一、中医辨证分析", ""))

                # 第二部分：个性化养生建议
                remaining = sections[1].split("## 三、重要提醒")
                st.markdown("""
                <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                            padding: 20px;
                            border-radius: 10px;
                            margin: 20px 0;">
                    <h3 style="color: white; margin: 0;">💊 个性化养生建议</h3>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(remaining[0])

                # 第三部分：重要提醒
                if len(remaining) >= 2:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                                padding: 20px;
                                border-radius: 10px;
                                margin: 20px 0;">
                        <h3 style="color: white; margin: 0;">⚠️ 重要提醒</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(remaining[1])
            else:
                # 如果分段失败，直接显示全部内容
                st.markdown(full_response)

            # 添加分隔线
            st.markdown("---")

            # 提示信息
            st.info("💡 **温馨提示：** 以上建议仅供参考，具体情况请咨询专业中医师。")

        except Exception as e:
            st.error(f"❌ 分析过程中出现错误：{str(e)}")
            st.info("💡 请检查：\n1. 是否已配置OPENAI_API_KEY\n2. API密钥是否有效\n3. 网络连接是否正常")

# 侧边栏
with st.sidebar:
    # 应用信息卡片
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;">
        <h3 style="color: white; margin: 0;">🏥 中医智能小助手</h3>
        <p style="color: #f0f0f0; font-size: 14px; margin: 10px 0 0 0;">v1.3 · 界面优化版</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📊 应用特色")
    st.markdown("""
    - ✨ **AI智能分析**：GPT-4驱动
    - 🎯 **精准辨证**：多维度综合评估
    - 💊 **实用建议**：可落地的养生方案
    - 🔒 **隐私保护**：数据不留存
    """)

    st.markdown("---")

    st.markdown("### ❓ 常见问题")
    with st.expander("如何获得更准确的建议？"):
        st.write("""
        **提供详细信息：**
        - 症状的具体表现
        - 发生的时间和频率
        - 伴随的其他症状
        - 加重或缓解的因素

        **使用快速选择：**
        - 点击症状标签快速添加
        - 可多选组合症状
        - 在文本框中补充细节
        """)

    with st.expander("建议的可信度如何？"):
        st.write("""
        本应用基于：
        - GPT-4o-mini大语言模型
        - 中医经典理论体系
        - 现代医学常识校验

        ⚠️ 注意：
        - 仅供养生保健参考
        - 不能替代专业诊断
        - 重症请及时就医
        """)

    with st.expander("我的数据安全吗？"):
        st.write("""
        **隐私保护承诺：**
        - ✓ 数据仅用于生成建议
        - ✓ 不进行永久存储
        - ✓ 不与第三方共享
        - ✓ 符合数据保护法规
        """)

    with st.expander("什么时候应该就医？"):
        st.write("""
        **立即就医的情况：**
        - 🚨 急性剧烈疼痛
        - 🚨 持续高热不退
        - 🚨 呼吸困难
        - 🚨 意识模糊
        - 🚨 大量出血
        - 🚨 症状急剧恶化

        **及时就医的情况：**
        - ⚠️ 症状持续超过2周
        - ⚠️ 症状反复发作
        - ⚠️ 影响正常生活
        - ⚠️ 有基础疾病
        """)

    st.markdown("---")

    st.markdown("### 💡 养生小贴士")
    tips = [
        "🌅 早睡早起，顺应自然",
        "🥗 饮食有节，营养均衡",
        "🧘 适度运动，量力而行",
        "😊 心态平和，情志舒畅",
        "💧 多喝温水，促进代谢"
    ]
    import random
    st.info(random.choice(tips))

# 页脚
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>© 2025 中医智能小助手 | Powered by Streamlit & AI</div>",
    unsafe_allow_html=True
)