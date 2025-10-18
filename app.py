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

# 简介
st.markdown("""
### 欢迎使用中医智能小助手
本应用基于人工智能技术，从中医角度分析您的身体不适症状，并提供个性化的养生建议。

**使用说明：**
1. 在下方输入框中详细描述您的不适症状
2. 点击"开始分析"按钮
3. 等待AI分析并查看建议

⚠️ **免责声明：** 本应用仅提供参考建议，不能替代专业医疗诊断。如有严重不适，请及时就医。
""")

st.markdown("---")

# 症状输入区域
st.subheader("📝 请描述您的症状")

# 使用文本区域让用户输入症状
symptoms = st.text_area(
    "症状描述",
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
    st.markdown("### 关于")
    st.info("""
    **中医智能小助手 v1.0**

    本应用结合传统中医理论与现代AI技术，
    为您提供健康养生建议。
    """)

    st.markdown("### 常见问题")
    with st.expander("如何获得更准确的建议？"):
        st.write("请尽可能详细地描述症状，包括具体表现、持续时间、发生频率等信息。")

    with st.expander("建议的可信度如何？"):
        st.write("本应用基于大语言模型提供建议，仅供参考。严重症状请及时就医。")

    with st.expander("我的数据安全吗？"):
        st.write("您的输入仅用于生成建议，不会被永久存储。")

# 页脚
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>© 2025 中医智能小助手 | Powered by Streamlit & AI</div>",
    unsafe_allow_html=True
)