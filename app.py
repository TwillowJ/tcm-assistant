import streamlit as st
import os
from llm_service import TCMAnalyzer

# 页面配置
st.set_page_config(
    page_title="中医智能小助手",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 初始化session state
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'  # 'welcome' 或 'chat'
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'show_welcome_message' not in st.session_state:
    st.session_state.show_welcome_message = True
if 'user_info' not in st.session_state:
    st.session_state.user_info = {'age': 30, 'gender': '不方便透露'}

# 自定义CSS样式
st.markdown("""
<style>
    /* 隐藏默认的Streamlit元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 聊天消息样式 */
    .chat-message {
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .chat-message.user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 20%;
    }
    .chat-message.assistant {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        color: #333;
        margin-right: 20%;
    }
    .message-content {
        margin-top: 0.5rem;
        line-height: 1.6;
    }

    /* 快速选择按钮样式 */
    .quick-option {
        display: inline-block;
        margin: 5px;
        padding: 10px 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        cursor: pointer;
        transition: all 0.3s;
    }
    .quick-option:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# ==================== 欢迎页面 ====================
def show_welcome_page():
    # 居中布局
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)

        # 应用标题和介绍
        st.markdown("""
        <div style="text-align: center;">
            <h1 style="font-size: 48px; margin-bottom: 10px;">🌿 中医智能小助手</h1>
            <p style="font-size: 20px; color: #666; margin-bottom: 30px;">
                结合传统中医智慧与现代AI技术，为您提供个性化养生建议
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 功能特色
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 30px;
                    border-radius: 15px;
                    color: white;
                    margin-bottom: 30px;">
            <h3 style="text-align: center; margin-bottom: 20px;">✨ 应用特色</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <div>🤖 <strong>AI智能分析</strong><br/>GPT-4o-mini驱动的专业分析</div>
                <div>🎯 <strong>精准辨证</strong><br/>多维度综合评估</div>
                <div>💊 <strong>实用建议</strong><br/>可落地的养生方案</div>
                <div>🔒 <strong>隐私保护</strong><br/>数据不留存</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 免责声明
        st.markdown("""
        <div style="background: #fff3cd;
                    border-left: 4px solid #ffc107;
                    padding: 20px;
                    border-radius: 10px;
                    margin-bottom: 30px;">
            <h4 style="color: #856404; margin-top: 0;">⚠️ 免责声明</h4>
            <p style="color: #856404; margin-bottom: 0; line-height: 1.6;">
                本应用仅提供养生保健参考建议，不能替代专业医疗诊断和治疗。
                建议仅为养生保健参考，不涉及具体药物治疗。
                如有严重或持续性症状，请及时就医咨询专业医师。
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 进入问诊按钮
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn2:
            if st.button("🩺 进入问诊", type="primary", use_container_width=True, key="enter_chat"):
                st.session_state.page = 'chat'
                st.session_state.show_welcome_message = True
                st.rerun()

        st.markdown("<br><br>", unsafe_allow_html=True)

        # 页脚
        st.markdown("""
        <div style="text-align: center; color: #999; font-size: 14px;">
            © 2025 中医智能小助手 v2.0 | Powered by Streamlit & AI
        </div>
        """, unsafe_allow_html=True)

# ==================== 对话页面 ====================
def show_chat_page():
    # 顶部导航栏
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        if st.button("← 返回首页", key="back_to_welcome"):
            st.session_state.page = 'welcome'
            st.rerun()
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 10px;">
            <h3 style="margin: 0; color: #667eea;">🌿 中医智能小助手</h3>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        if st.button("🔄 新对话", key="new_chat"):
            st.session_state.chat_history = []
            st.session_state.show_welcome_message = True
            st.rerun()

    st.markdown("---")

    # 显示AI欢迎消息（仅首次进入时）
    if st.session_state.show_welcome_message:
        st.session_state.show_welcome_message = False

        # AI欢迎消息
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

    # 显示对话历史
    chat_container = st.container()
    with chat_container:
        for idx, message in enumerate(st.session_state.chat_history):
            if message['role'] == 'user':
                st.markdown(f"""
                <div class="chat-message user">
                    <div style="font-weight: bold;">👤 您</div>
                    <div class="message-content">{message['content']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant">
                    <div style="font-weight: bold;">🌿 中医小助手</div>
                    <div class="message-content">{message['content']}</div>
                </div>
                """, unsafe_allow_html=True)

                # 在第一条AI消息后显示常见症状快速选择
                if idx == 0:
                    show_quick_symptoms()

    # 底部输入框
    st.markdown("<br>", unsafe_allow_html=True)

    # 用户信息（可折叠）
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

    # 输入框和发送按钮
    col_input, col_send = st.columns([5, 1])
    with col_input:
        user_input = st.text_input("请输入您的症状或问题...",
                                   key="user_input",
                                   label_visibility="collapsed",
                                   placeholder="请详细描述您的症状...")
    with col_send:
        send_button = st.button("发送 📤", type="primary", use_container_width=True)

    # 处理用户输入
    if send_button and user_input.strip():
        handle_user_input(user_input)

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
            if st.button(issue, key=f"quick_{idx}", use_container_width=True):
                handle_user_input(issue)

# 处理用户输入
def handle_user_input(user_input):
    # 添加用户消息到历史
    st.session_state.chat_history.append({
        'role': 'user',
        'content': user_input
    })

    # 调用AI获取回复
    try:
        analyzer = TCMAnalyzer()

        # 构建对话上下文
        messages = []
        for msg in st.session_state.chat_history[-5:]:  # 只保留最近5轮对话作为上下文
            messages.append({
                'role': msg['role'],
                'content': msg['content']
            })

        # 获取AI回复（使用流式输出）
        with st.spinner("🤔 正在思考..."):
            full_response = ""
            for chunk in analyzer.chat_streaming(
                messages=messages,
                age=st.session_state.user_info['age'],
                gender=st.session_state.user_info['gender']
            ):
                full_response += chunk

        # 添加AI回复到历史
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': full_response
        })

    except Exception as e:
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': f"抱歉，分析过程中出现错误：{str(e)}\n\n请检查网络连接或稍后重试。"
        })

    st.rerun()

# ==================== 主程序 ====================
def main():
    if st.session_state.page == 'welcome':
        show_welcome_page()
    else:
        show_chat_page()

if __name__ == "__main__":
    main()