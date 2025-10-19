import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class TCMAnalyzer:
    """中医智能分析器"""

    def __init__(self):
        """初始化OpenAI客户端"""
        # 优先从Streamlit secrets读取，然后从环境变量读取
        api_key = None
        try:
            import streamlit as st
            if hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
                api_key = st.secrets['OPENAI_API_KEY']
        except:
            pass

        if not api_key:
            api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("未找到OPENAI_API_KEY，请在.env文件或Streamlit secrets中配置")

        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"  # 使用GPT-4 Turbo模型以获得更好的中医分析能力

    def _build_system_prompt(self):
        """构建系统提示词 - 定义AI助手的角色和行为准则"""
        return """你是一位经验丰富的中医养生专家，拥有深厚的中医理论功底和丰富的临床经验。你精通：
- 中医基础理论：阴阳五行、藏象学说、经络学说、病因病机
- 中医诊断：望闻问切、八纲辨证、脏腑辨证、气血津液辨证
- 养生之道：饮食调理、情志调摄、起居有常、运动养生

你的分析特点：
1. 辨证准确：能从症状中识别证型特征，分析病机
2. 建议实用：提供具体可操作的养生方案，避免空泛
3. 解释清晰：用现代语言解释中医概念，深入浅出
4. 因人制宜：考虑年龄、性别、体质等个体差异

重要原则：
✓ 本建议仅供养生保健参考，不能替代专业医疗诊断和治疗
✓ 遇到以下情况必须明确建议就医：急性重症、持续恶化、疑似器质性病变
✓ 不推荐具体中药方剂，重点在食疗和生活方式调整
✓ 保持专业、客观、温和的语气，避免夸大或恐吓
✓ 建议要科学合理，符合现代医学常识"""

    def _build_user_prompt(self, symptoms, age, gender, duration):
        """构建用户提示词 - 整合用户输入的症状信息"""
        prompt = f"""请为以下用户提供专业的中医养生分析和建议：

【用户基本信息】
- 年龄：{age}岁
- 性别：{gender}
- 症状持续时间：{duration}

【症状描述】
{symptoms}

【分析要求】
请按以下结构提供详细、专业且实用的分析和建议：

## 一、中医辨证分析

1. **证型判断**：基于描述的症状，分析最可能的1-2个证型
   - 常见证型包括：气虚、血虚、阴虚、阳虚、气滞、血瘀、痰湿、湿热等
   - 说明选择该证型的主要依据

2. **病机分析**：用通俗语言解释
   - 为什么会出现这些症状？
   - 中医如何理解这种身体状态？
   - 与年龄、性别的关联

## 二、个性化养生建议

### 1. 饮食调理（重点推荐）
- **推荐食物**：列举3-5种具体食物，说明功效
- **食疗方**：提供1-2个简单易做的食疗方，标注材料和做法
- **避免食物**：明确哪些食物不宜多吃
- **饮食习惯**：用餐时间、份量、温度等建议

### 2. 生活起居
- **作息建议**：具体的睡眠时间（如"建议23:00前入睡"）
- **睡眠改善**：提供2-3个实用方法
- **情绪调节**：针对症状的情志调摄建议
- **日常注意**：需要避免的生活习惯

### 3. 运动养生
- **推荐运动**：列举2-3种适合的运动方式
- **运动方案**：具体的频率、时长、强度建议
- **传统功法**：如适合，推荐八段锦、太极等，说明练习要点
- **运动禁忌**：需要避免的运动类型或注意事项

### 4. 其他调理方法
- **穴位保健**：推荐2-3个穴位，说明位置和按摩方法
- **外治方法**：如泡脚、艾灸等，提供具体方案
- **季节调养**：当前季节的特别注意事项

## 三、重要提醒

### ⚠️ 需要就医的情况
明确列出哪些症状变化需要及时就医，不要延误

### 📅 调理周期
- 预期多久能看到改善
- 需要坚持多久
- 定期评估的建议

### 💊 特别说明
- 强调这是养生保健建议，不能替代医疗诊断
- 如有基础疾病或在服药，需咨询医生
- 建议要循序渐进，不可操之过急

【输出要求】
- 语言通俗易懂，避免过多专业术语
- 建议具体可操作，给出明确的数量、时间等
- 重视安全性，对可能的风险做出提醒
- 整体积极温和，给用户信心和方向"""

        return prompt

    def analyze(self, symptoms, age=30, gender="不方便透露", duration="1-3天"):
        """
        执行中医分析

        参数:
            symptoms: 症状描述
            age: 年龄
            gender: 性别
            duration: 症状持续时间

        返回:
            分析结果文本
        """
        try:
            # 构建消息
            messages = [
                {"role": "system", "content": self._build_system_prompt()},
                {"role": "user", "content": self._build_user_prompt(symptoms, age, gender, duration)}
            ]

            # 调用OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,  # 适度的创造性，保持专业性
                max_tokens=2000,  # 确保回答足够详细
            )

            # 提取回答
            result = response.choices[0].message.content
            return result

        except Exception as e:
            raise Exception(f"调用LLM API时出错: {str(e)}")

    def analyze_streaming(self, symptoms, age=30, gender="不方便透露", duration="1-3天"):
        """
        流式执行中医分析（支持实时显示结果）

        参数:
            symptoms: 症状描述
            age: 年龄
            gender: 性别
            duration: 症状持续时间

        返回:
            生成器，逐步返回分析结果
        """
        try:
            # 构建消息
            messages = [
                {"role": "system", "content": self._build_system_prompt()},
                {"role": "user", "content": self._build_user_prompt(symptoms, age, gender, duration)}
            ]

            # 调用OpenAI API（流式）
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000,
                stream=True  # 启用流式输出
            )

            # 逐步返回结果
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            raise Exception(f"调用LLM API时出错: {str(e)}")

    def chat_streaming(self, messages, age="未提供", gender="不方便透露"):
        """
        多轮对话流式输出

        参数:
            messages: 对话历史 [{"role": "user/assistant", "content": "..."}]
            age: 年龄（可以是数字或"未提供"）
            gender: 性别

        返回:
            生成器，逐步返回AI回复
        """
        try:
            # 格式化年龄信息
            if age == "未提供":
                age_info = "未提供（请勿在回复中假设或提及具体年龄）"
            else:
                age_info = f"{age}岁"

            # 构建系统提示词（针对多轮对话优化）
            system_prompt = f"""你是一位经验丰富的中医养生专家，正在与用户进行多轮对话咨询。

用户信息：
- 年龄：{age_info}
- 性别：{gender}

你的职责：
1. 耐心倾听用户的症状和问题
2. 通过提问了解更多细节（如症状持续时间、加重缓解因素等）
3. 从中医角度分析症状，给出辨证结果
4. 提供实用的养生建议（饮食、起居、运动等）
5. 回答用户的追问，解释中医理论

对话原则：
- 语言简洁友好，避免过于专业的术语
- 根据对话上下文给出针对性回复
- 如果信息不足，先主动询问更多细节（如症状持续时间、程度、伴随症状等）
- 当收集到足够信息后，必须提供完整的分析，包括：
  * 中医辨证分析（证型判断及依据）
  * 个性化养生建议（饮食、起居、运动等）
- 强调这是养生保健建议，不能替代医疗诊断
- 遇到严重症状，建议就医

回复格式要求：
- 简短问答：直接回复即可
- 症状分析：当用户描述完整症状或你已收集足够信息时，必须按以下结构提供详细回复：

**中医辨证分析：**
1. 证型判断：明确指出1-2个最可能的证型（如气虚、血虚、阴虚、阳虚、气滞、血瘀、痰湿、湿热等）
2. 辨证依据：详细说明为什么判断为该证型，结合用户症状逐一分析
3. 病机解释：用通俗易懂的语言解释中医如何理解这种身体状态
4. 个体因素：考虑年龄、性别对症状的影响

**养生建议：**（每项都要具体、可操作）

1. 饮食调理：
   - 推荐食物：列举5-8种具体食物，说明功效和食用方法
   - 食疗方：提供2-3个简单易做的食疗方，标注材料用量和详细做法
   - 避免食物：明确列出不宜食物及原因
   - 饮食习惯：用餐时间、份量、温度、烹饪方式等建议

2. 生活起居：
   - 作息建议：具体的睡眠时间和午休建议
   - 睡眠改善：提供3-5个实用方法
   - 情绪调节：针对症状的具体情志调摄建议
   - 日常注意：需要避免的生活习惯，给出替代方案

3. 运动养生：
   - 推荐运动：列举3-5种适合的运动方式及理由
   - 运动方案：具体的频率（每周几次）、时长、强度、最佳时间
   - 传统功法：如适合，推荐八段锦、太极、五禽戏等，说明练习要点和注意事项
   - 运动禁忌：明确需要避免的运动类型

4. 其他调理方法：
   - 穴位保健：推荐3-5个穴位，详细说明位置、按摩手法、频率和作用
   - 外治方法：如泡脚、艾灸、刮痧等，提供具体操作方案
   - 季节调养：当前季节的特别注意事项和调养重点
   - 日常小妙招：提供2-3个简单实用的养生技巧

**重要提醒：**
1. 就医建议：明确列出哪些症状变化需要及时就医
2. 调理周期：预期多久能看到改善，需要坚持多久
3. 注意事项：如有基础疾病或在服药的特别提醒
4. 跟踪评估：建议定期自我评估和调整的方法

内容要求：
- 每个建议都要具体、详细、可操作
- 避免空泛的建议，给出明确的数量、时间、方法
- 语言通俗易懂，适当使用比喻帮助理解
- 整体积极温和，给用户信心和方向

请保持温和、专业的语气，像一位可信赖的中医师一样与用户交流。"""

            # 构建完整的消息列表
            api_messages = [{"role": "system", "content": system_prompt}]

            # 添加对话历史（跳过欢迎消息）
            for msg in messages:
                if msg['role'] in ['user', 'assistant']:
                    # 过滤掉欢迎消息
                    if not (msg['role'] == 'assistant' and '我是您的中医智能小助手' in msg['content']):
                        api_messages.append({
                            "role": msg['role'],
                            "content": msg['content']
                        })

            # 调用OpenAI API（流式）
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=api_messages,
                temperature=0.7,
                max_tokens=1500,
                stream=True
            )

            # 逐步返回结果
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            raise Exception(f"调用LLM API时出错: {str(e)}")