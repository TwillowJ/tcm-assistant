import streamlit as st
import os
import time
from llm_service import TCMAnalyzer

# 页面配置
st.set_page_config(
    page_title="中医智能小助手",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 初始化session state
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'show_welcome_message' not in st.session_state:
    st.session_state.show_welcome_message = True
if 'user_info' not in st.session_state:
    st.session_state.user_info = {'age': None, 'gender': '不方便透露'}

# 自定义CSS样式
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        max-width: 800px;
    }

    /* 优化按钮样式 */
    .stButton button {
        border-radius: 8px;
        transition: all 0.3s ease;
    }

    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    /* 优化聊天消息样式 */
    .stChatMessage {
        border-radius: 12px;
        margin-bottom: 8px;
    }

    /* 优化输入框样式 */
    .stChatInput {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 欢迎页面 ====================
def show_welcome_page():
    st.markdown("""
    <div style="text-align: center; margin-top: 8vh;">
        <h1 style="font-size: 48px; margin-bottom: 20px;
                   background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                   -webkit-background-clip: text;
                   -webkit-text-fill-color: transparent;
                   font-weight: 700;">
            🌿 中医智能小助手
        </h1>
        <p style="font-size: 18px; color: #666; margin-bottom: 50px; line-height: 1.6;">
            结合传统中医智慧与现代AI技术<br>为您提供个性化养生建议
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 功能特色 - 卡片式布局
    st.markdown("""
    <div style="text-align: center; margin: 40px auto; max-width: 600px;">
        <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    border-radius: 16px;
                    padding: 30px;
                    box-shadow: 0 8px 24px rgba(0,0,0,0.12);">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; text-align: center;">
                <div><span style="font-size: 24px;">🤖</span><br><strong>AI智能分析</strong></div>
                <div><span style="font-size: 24px;">🎯</span><br><strong>精准辨证</strong></div>
                <div><span style="font-size: 24px;">💊</span><br><strong>养生建议</strong></div>
                <div><span style="font-size: 24px;">🔒</span><br><strong>隐私保护</strong></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("⚠️ **免责声明**：本产品仅为 AI 技术演示，内容仅供参考，不能替代专业医疗诊断。")
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        if st.button("🩺 开始问诊", type="primary", use_container_width=True, key="enter_chat"):
            st.session_state.page = 'chat'
            st.session_state.show_welcome_message = True
            st.rerun()

    st.markdown("""
    <div style="text-align: center; color: #999; font-size: 13px; margin-top: 60px;">
        © 2025 中医智能小助手 v1.6 | Powered by Claude AI
    </div>
    """, unsafe_allow_html=True)

# ==================== 对话页面 ====================
def show_chat_page():
    # 顶部导航
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("← 返回", key="back_btn"):
            if len(st.session_state.chat_history) > 1:
                st.session_state.page = 'confirm_exit'
                st.rerun()
            else:
                st.session_state.page = 'welcome'
                st.rerun()
    with col2:
        st.markdown("<h3 style='text-align: center; color: #667eea; margin: 0;'>🌿 中医智能小助手</h3>",
                   unsafe_allow_html=True)
    with col3:
        if st.button("🔄 新对话", key="new_chat"):
            st.session_state.chat_history = []
            st.session_state.show_welcome_message = True
            st.rerun()

    st.markdown("---")

    # 首次进入显示欢迎消息
    if st.session_state.show_welcome_message:
        st.session_state.show_welcome_message = False
        welcome_msg = {
            'role': 'assistant',
            'content': "您好！我是您的中医智能小助手 🌿\n\n我可以帮您从中医角度分析身体症状，提供个性化养生建议。\n\n请告诉我您的症状或健康问题："
        }
        st.session_state.chat_history.append(welcome_msg)

    # 对话历史容器
    chat_container = st.container(height=500)

    with chat_container:
        for idx, message in enumerate(st.session_state.chat_history):
            with st.chat_message(message['role'], avatar="🌿" if message['role'] == 'assistant' else "👤"):
                # 如果是最后一条消息且内容为"正在分析中..."，在此处进行流式输出
                if idx == len(st.session_state.chat_history) - 1 and message['content'] == "正在分析中...":
                    # 在聊天框内直接进行流式输出
                    full_response = get_ai_response_streaming()
                    # 更新chat_history
                    st.session_state.chat_history[-1] = {
                        'role': 'assistant',
                        'content': full_response
                    }
                else:
                    st.markdown(message['content'])

    # 用户信息（折叠）- 放在快速选择之前避免UI重复
    with st.expander("📋 个人信息（可选）", expanded=False):
        st.markdown("*提供个人信息可获得更精准的养生建议*")

        col1, col2 = st.columns(2)

        with col1:
            # 年龄选择 - 使用selectbox避免默认值问题
            age_options = ["未提供"] + list(range(1, 121))

            if st.session_state.user_info['age'] is None:
                default_age_index = 0  # "未提供"
            else:
                default_age_index = age_options.index(st.session_state.user_info['age'])

            age_selection = st.selectbox(
                "年龄",
                options=age_options,
                index=default_age_index,
                key="user_age"
            )

            # 更新session state
            if age_selection == "未提供":
                st.session_state.user_info['age'] = None
            else:
                st.session_state.user_info['age'] = age_selection

        with col2:
            # 性别选择
            gender = st.selectbox(
                "性别",
                ["不方便透露", "男", "女"],
                index=["不方便透露", "男", "女"].index(st.session_state.user_info['gender']),
                key="user_gender"
            )
            st.session_state.user_info['gender'] = gender

    # 常见症状快速选择（仅在只有欢迎消息时显示）
    if len(st.session_state.chat_history) == 1:
        st.markdown("**💡 常见症状快速选择：**")
        common_issues = [
            "😴 疲劳乏力、精神不振",
            "🌙 失眠多梦、睡眠质量差",
            "🍽️ 消化不良、胃胀腹胀",
            "🤕 头痛头晕",
            "😰 焦虑心烦、情绪低落",
            "🦴 腰酸背痛、关节疼痛"
        ]

        cols = st.columns(2)  # 改为2列，更适合移动端
        for idx, issue in enumerate(common_issues):
            col_idx = idx % 2
            with cols[col_idx]:
                if st.button(issue, key=f"quick_{idx}", use_container_width=True):
                    # 移除emoji，只保留症状文字
                    clean_issue = issue.split(' ', 1)[1] if ' ' in issue else issue
                    # 立即添加用户消息并显示
                    st.session_state.chat_history.append({
                        'role': 'user',
                        'content': clean_issue
                    })
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': "正在分析中..."
                    })
                    st.rerun()

    # 输入框
    user_input = st.chat_input("请输入您的症状或问题...")

    # 处理发送
    if user_input and user_input.strip():
        # 立即添加用户消息
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input.strip()
        })
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': "正在分析中..."
        })
        st.rerun()

def get_ai_response_streaming():
    """在聊天框内流式获取并显示AI回复"""
    try:
        analyzer = TCMAnalyzer()

        # 构建对话上下文（排除"正在分析中..."）
        messages = []
        for msg in st.session_state.chat_history[:-1]:  # 排除最后的"正在分析中..."
            if msg['role'] in ['user', 'assistant']:
                if not ('我是您的中医智能小助手' in msg['content']):
                    messages.append(msg)

        # 获取用户信息
        age = st.session_state.user_info['age'] if st.session_state.user_info['age'] else 30
        gender = st.session_state.user_info['gender']

        # 在当前位置创建占位符进行流式显示
        text_placeholder = st.empty()
        full_response = ""

        # 流式获取AI回复并实时显示
        for chunk in analyzer.chat_streaming(
            messages=messages[-6:],  # 只保留最近6轮对话
            age=age,
            gender=gender
        ):
            full_response += chunk
            text_placeholder.markdown(full_response + "▌")  # 添加光标效果
            time.sleep(0.02)  # 打字效果延迟

        # 移除光标，显示最终结果
        text_placeholder.markdown(full_response)

        return full_response

    except Exception as e:
        error_msg = f"抱歉，分析过程中出现错误：{str(e)}\n\n请检查网络连接或稍后重试。"
        st.error(error_msg)
        return error_msg

# ==================== 确认退出页面 ====================
def show_confirm_exit():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.warning("### ⚠️ 确认返回首页？")
    st.write("返回首页将清除当前的对话记录，确定要继续吗？")
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("✅ 确认返回", type="primary", use_container_width=True):
            st.session_state.page = 'welcome'
            st.session_state.chat_history = []
            st.rerun()
    with col3:
        if st.button("❌ 取消", use_container_width=True):
            st.session_state.page = 'chat'
            st.rerun()

# ==================== 主程序 ====================
def main():
    if st.session_state.page == 'welcome':
        show_welcome_page()
    elif st.session_state.page == 'chat':
        show_chat_page()
    elif st.session_state.page == 'confirm_exit':
        show_confirm_exit()

if __name__ == "__main__":
    main()
