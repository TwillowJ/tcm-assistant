import streamlit as st
import os
from llm_service import TCMAnalyzer

# 页面配置
st.set_page_config(
    page_title="中医智能小助手",
    page_icon="🏥",
    layout="wide"
)

# 主标题
st.title("🏥 中医智能小助手")
st.markdown("---")

# 欢迎横幅
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    <h2 style="color: white; margin: 0; text-align: center;">🌿 欢迎使用中医智能小助手</h2>
    <p style="color: #f0f0f0; text-align: center; margin-top: 10px; font-size: 16px;">
        结合传统中医智慧与现代AI技术，为您提供个性化养生建议
    </p>
</div>
""", unsafe_allow_html=True)

# 功能卡片
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="text-align: center; padding: 20px; background-color: #f8f9fa; border-radius: 10px;">
        <div style="font-size: 40px; margin-bottom: 10px;">🔍</div>
        <h4 style="margin: 0;">智能分析</h4>
        <p style="color: #666; font-size: 14px;">AI辨证施治</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="text-align: center; padding: 20px; background-color: #f8f9fa; border-radius: 10px;">
        <div style="font-size: 40px; margin-bottom: 10px;">💊</div>
        <h4 style="margin: 0;">个性方案</h4>
        <p style="color: #666; font-size: 14px;">定制养生建议</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="text-align: center; padding: 20px; background-color: #f8f9fa; border-radius: 10px;">
        <div style="font-size: 40px; margin-bottom: 10px;">🌱</div>
        <h4 style="margin: 0;">科学养生</h4>
        <p style="color: #666; font-size: 14px;">中西医结合</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 使用提示
with st.expander("📖 使用指南", expanded=False):
    st.markdown("""
    **如何使用本应用：**
    1. 📝 选择或输入您的症状描述（越详细越好）
    2. 👤 填写基本信息（年龄、性别、持续时间）
    3. 🔍 点击"开始分析"按钮
    4. ⏱️ 等待AI分析（通常10-30秒）
    5. 📋 查看个性化的养生建议

    **温馨提示：**
    - 症状描述越详细，分析越准确
    - 可以使用快速选择功能快速添加症状
    - 建议定期评估调整养生方案

    ⚠️ **免责声明：** 本应用仅提供养生保健参考建议，不能替代专业医疗诊断和治疗。如有严重或持续症状，请及时就医咨询专业医师。
    """)

st.markdown("---")

# 症状输入区域
st.subheader("📝 请描述您的症状")

# 常见症状快速选择
st.markdown("#### 💡 常见症状快速选择")
st.caption("点击下方标签快速添加症状，或直接在文本框中输入")

# 定义常见症状分类
symptom_categories = {
    "疲劳乏力": ["容易疲劳", "精神不振", "四肢无力", "气短懒言"],
    "睡眠问题": ["失眠多梦", "入睡困难", "早醒", "睡眠质量差", "嗜睡"],
    "消化系统": ["食欲不振", "腹胀", "便秘", "腹泻", "恶心", "胃痛"],
    "头部症状": ["头痛", "头晕", "头重", "耳鸣"],
    "情绪相关": ["易怒", "焦虑", "抑郁", "心烦", "情绪低落"],
    "疼痛不适": ["腰痛", "关节痛", "肌肉酸痛", "胸闷", "心悸"],
    "其他症状": ["怕冷", "怕热", "出汗异常", "口干", "口苦", "咽干"],
}

# 使用session_state存储选中的症状
if 'selected_symptoms' not in st.session_state:
    st.session_state.selected_symptoms = []

# 创建症状选择界面
cols_per_row = 4
for category, symptoms_list in symptom_categories.items():
    with st.expander(f"🔹 {category}", expanded=False):
        cols = st.columns(cols_per_row)
        for idx, symptom in enumerate(symptoms_list):
            col_idx = idx % cols_per_row
            with cols[col_idx]:
                if st.button(symptom, key=f"symptom_{category}_{symptom}", use_container_width=True):
                    if symptom not in st.session_state.selected_symptoms:
                        st.session_state.selected_symptoms.append(symptom)

# 显示已选症状
if st.session_state.selected_symptoms:
    st.markdown("**已选症状：**")
    selected_text = "、".join(st.session_state.selected_symptoms)
    st.info(f"📌 {selected_text}")

    if st.button("🗑️ 清空已选症状", key="clear_symptoms"):
        st.session_state.selected_symptoms = []
        st.rerun()

st.markdown("---")

# 使用文本区域让用户输入症状
# 自动填充已选症状
default_symptoms = "、".join(st.session_state.selected_symptoms) if st.session_state.selected_symptoms else ""
symptoms = st.text_area(
    "症状描述（可在快速选择的基础上补充详细信息）",
    value=default_symptoms,
    placeholder="例如：最近经常感到疲劳，容易出汗，晚上睡眠质量不好，偶尔会有头晕...",
    height=150,
    help="请尽可能详细地描述您的症状，包括持续时间、发生频率、伴随症状等"
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
    if not symptoms.strip():
        st.error("❌ 请先输入症状描述")
    else:
        try:
            # 初始化分析器
            analyzer = TCMAnalyzer()

            # 显示加载状态并调用LLM API
            with st.spinner("🤖 AI正在分析您的症状，请稍候..."):
                # 使用流式输出获得更好的用户体验
                result_placeholder = st.empty()
                full_response = ""

                # 流式获取分析结果
                for chunk in analyzer.analyze_streaming(
                    symptoms=symptoms,
                    age=int(age),
                    gender=gender,
                    duration=duration
                ):
                    full_response += chunk
                    result_placeholder.markdown(full_response)

            st.success("✅ 分析完成！")

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
        <p style="color: #f0f0f0; font-size: 14px; margin: 10px 0 0 0;">v1.1 · 优化版</p>
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