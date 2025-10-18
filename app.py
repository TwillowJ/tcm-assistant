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
    st.session_state.user_info = {'age': 30, 'gender': '不方便透露'}
if 'current_response' not in st.session_state:
    st.session_state.current_response = ""
if 'is_generating' not in st.session_state:
    st.session_state.is_generating = False

# 自定义CSS样式
st.markdown("""
<style>
    /* 隐藏默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 移除顶部空白 */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }

    /* 固定高度的聊天容器 */
    .chat-container {
        height: 60vh;
        overflow-y: auto;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        background: #fafafa;
    }

    /* 聊天消息样式 */
    .chat-message {
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
        animation: fadeIn 0.3s ease-in;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .chat-message.user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 15%;
    }

    .chat-message.assistant {
        background: white;
        color: #333;
        margin-right: 15%;
        border: 1px solid #e0e0e0;
    }

    .message-content {
        margin-top: 0.5rem;
        line-height: 1.6;
        white-space: pre-wrap;
    }

    /* 打字机效果 */
    .typing-indicator {
        display: inline-block;
        animation: blink 1.4s infinite;
    }

    @keyframes blink {
        0%, 100% { opacity: 0; }
        50% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# ==================== 欢迎页面 ====================
def show_welcome_page():
    # 标题
    st.markdown("""
    <div style="text-align: center; margin-top: 10vh;">
        <h1 style="font-size: 42px; margin-bottom: 15px;">🌿 中医智能小助手</h1>
        <p style="font-size: 18px; color: #666; margin-bottom: 40px;">
            结合传统中医智慧与现代AI技术，为您提供个性化养生建议
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 功能特色 - 紧凑版
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("🤖 **AI智能分析**")
        st.markdown("💊 **实用养生建议**")
    with col2:
        st.markdown("🎯 **精准辨证**")
        st.markdown("🔒 **隐私保护**")

    st.markdown("<br>", unsafe_allow_html=True)

    # 免责声明 - 精简版
    st.info("⚠️ **免责声明**：本产品仅为 AI 技术演示，内容仅供参考，不能替代专业医疗诊断。")

    st.markdown("<br>", unsafe_allow_html=True)

    # 进入问诊按钮
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🩺 进入问诊", type="primary", use_container_width=True, key="enter_chat"):
            st.session_state.page = 'chat'
            st.session_state.show_welcome_message = True
            st.rerun()

    # 页脚
    st.markdown("""
    <div style="text-align: center; color: #999; font-size: 14px; margin-top: 40px;">
        © 2025 中医智能小助手 v1.4 | Powered by AI
    </div>
    """, unsafe_allow_html=True)

# ==================== 对话页面 ====================
def show_chat_page():
    # 顶部导航
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("← 返回", key="back_btn"):
            # 确认对话
            if len(st.session_state.chat_history) > 1:  # 除了欢迎消息外还有其他消息
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
            'content': """您好！我是您的中医智能小助手 🌿

我可以帮您：
- 从中医角度分析身体症状
- 提供个性化养生建议
- 解答中医养生相关问题

请告诉我您的症状或健康问题，也可以点击下方常见症状快速咨询："""
        }
        st.session_state.chat_history.append(welcome_msg)

    # 对话历史容器（固定高度，可滚动）
    chat_html = '<div class="chat-container">'

    for idx, message in enumerate(st.session_state.chat_history):
        if message['role'] == 'user':
            chat_html += f'''
            <div class="chat-message user">
                <div style="font-weight: bold;">👤 您</div>
                <div class="message-content">{message['content']}</div>
            </div>
            '''
        else:
            chat_html += f'''
            <div class="chat-message assistant">
                <div style="font-weight: bold;">🌿 中医小助手</div>
                <div class="message-content">{message['content']}</div>
            </div>
            '''

            # 在第一条消息后显示快速选择
            if idx == 0:
                chat_html += '</div>'
                st.markdown(chat_html, unsafe_allow_html=True)
                show_quick_symptoms()
                chat_html = '<div class="chat-container">'

    # 如果正在生成回复，显示当前进度
    if st.session_state.is_generating and st.session_state.current_response:
        chat_html += f'''
        <div class="chat-message assistant">
            <div style="font-weight: bold;">🌿 中医小助手</div>
            <div class="message-content">{st.session_state.current_response}<span class="typing-indicator">▊</span></div>
        </div>
        '''

    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

    # 用户信息（折叠）
    with st.expander("📋 个人信息（可选）", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("年龄", min_value=1, max_value=120,
                                 value=st.session_state.user_info['age'],
                                 key="user_age")
            st.session_state.user_info['age'] = age
        with col2:
            gender = st.selectbox("性别", ["男", "女", "不方便透露"],
                                 index=["男", "女", "不方便透露"].index(st.session_state.user_info['gender']),
                                 key="user_gender")
            st.session_state.user_info['gender'] = gender

    # 输入框
    col_input, col_send = st.columns([5, 1])
    with col_input:
        user_input = st.text_input(
            "输入您的症状或问题...",
            key="user_input",
            label_visibility="collapsed",
            placeholder="请详细描述您的症状...",
            disabled=st.session_state.is_generating
        )
    with col_send:
        send_button = st.button(
            "发送 📤",
            type="primary",
            use_container_width=True,
            disabled=st.session_state.is_generating
        )

    # 处理发送
    if send_button and user_input.strip():
        handle_user_input(user_input.strip())

# 显示常见症状快速选择
def show_quick_symptoms():
    st.markdown("<br>", unsafe_allow_html=True)

    common_issues = [
        "疲劳乏力、精神不振",
        "失眠多梦、睡眠质量差",
        "消化不良、胃胀腹胀",
        "头痛头晕",
        "焦虑心烦、情绪低落",
        "腰酸背痛、关节疼痛"
    ]

    cols = st.columns(3)
    for idx, issue in enumerate(common_issues):
        col_idx = idx % 3
        with cols[col_idx]:
            if st.button(issue, key=f"quick_{idx}", use_container_width=True,
                        disabled=st.session_state.is_generating):
                handle_user_input(issue)

# 处理用户输入
def handle_user_input(user_input):
    # 添加用户消息
    st.session_state.chat_history.append({
        'role': 'user',
        'content': user_input
    })

    # 标记正在生成
    st.session_state.is_generating = True
    st.session_state.current_response = ""

    # 先显示"思考中"状态
    st.rerun()

    # 获取AI回复
    try:
        analyzer = TCMAnalyzer()

        # 构建对话上下文
        messages = []
        for msg in st.session_state.chat_history[-6:]:
            if msg['role'] in ['user', 'assistant']:
                if not ('我是您的中医智能小助手' in msg['content']):
                    messages.append(msg)

        # 流式获取回复
        full_response = ""
        response_placeholder = st.empty()

        for chunk in analyzer.chat_streaming(
            messages=messages,
            age=st.session_state.user_info['age'],
            gender=st.session_state.user_info['gender']
        ):
            full_response += chunk
            st.session_state.current_response = full_response
            # 每隔几个字符更新一次显示（模拟打字效果）
            if len(full_response) % 5 == 0:
                time.sleep(0.01)

        # 添加完整回复到历史
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': full_response
        })

    except Exception as e:
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': f"抱歉，分析过程中出现错误：{str(e)}\n\n请检查网络连接或稍后重试。"
        })

    finally:
        # 重置生成状态
        st.session_state.is_generating = False
        st.session_state.current_response = ""
        st.rerun()

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