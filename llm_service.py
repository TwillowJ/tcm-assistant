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
        return """你是一位专业的中医养生顾问，精通中医理论，包括阴阳五行、脏腑经络、气血津液等理论体系。

你的职责是：
1. 根据用户描述的症状，从中医角度进行辨证分析
2. 提供个性化的养生建议，包括饮食、作息、运动等方面
3. 用通俗易懂的语言解释中医概念，让普通人也能理解

重要原则：
- 始终强调这是养生建议，不能替代专业医疗诊断
- 如果症状严重或持续，明确建议用户就医
- 避免推荐具体药物，可以提及食疗和生活方式调整
- 保持客观、专业、温和的语气
- 回答要结构化、条理清晰"""

    def _build_user_prompt(self, symptoms, age, gender, duration):
        """构建用户提示词 - 整合用户输入的症状信息"""
        prompt = f"""请根据以下信息进行中医养生分析：

【基本信息】
- 年龄：{age}岁
- 性别：{gender}
- 症状持续时间：{duration}

【症状描述】
{symptoms}

请按以下结构提供分析和建议：

## 一、中医辨证分析
从中医角度分析可能的证型（如气虚、血虚、阴虚、阳虚、气滞、血瘀、痰湿等），解释症状与证型的对应关系。

## 二、养生建议

### 1. 饮食调理
- 推荐的食物和食疗方
- 应避免的食物
- 饮食习惯建议

### 2. 生活起居
- 作息时间建议
- 睡眠质量改善方法
- 情绪调节建议

### 3. 运动养生
- 适合的运动类型
- 运动强度和时长建议
- 可以尝试的传统养生功法（如八段锦、太极等）

### 4. 其他调理方法
- 穴位按摩建议
- 泡脚或其他外治方法
- 季节养生注意事项

## 三、注意事项
- 需要特别注意的症状变化
- 什么情况下应该就医
- 预期的调理周期

请确保建议科学、安全、易于实施。"""

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