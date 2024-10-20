import json
from abc import ABC, abstractmethod
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_ollama.chat_models import ChatOllama  # 导入 ChatOllama 模型
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  # 导入提示模板相关类
from langchain_core.messages import HumanMessage, AIMessage  # 导入人类消息类
from langchain_core.runnables.history import RunnableWithMessageHistory  # 导入带有消息历史的可运行类

from .session_history import get_session_history  # 导入会话历史相关方法
from utils.logger import LOG  # 导入日志工具

class AgentBase(ABC):
    """
    抽象基类，提供代理的共有功能。
    """
    def __init__(self, name, prompt_file, intro_file=None, session_id=None):
        self.name = name
        self.prompt_file = prompt_file
        self.intro_file = intro_file
        self.session_id = session_id if session_id else self.name
        self.prompt = self.load_prompt()
        self.intro_messages = self.load_intro() if self.intro_file else []
        self.client = OpenAI(
            api_key="51c7d9491590602cc291a879b3455f32.7PHWpwiNAVWfr8Dj",
            base_url="https://open.bigmodel.cn/api/paas/v4/"
        )
        self.create_chatbot()

    def load_prompt(self):
        """
        从文件加载系统提示语。
        """
        try:
            with open(self.prompt_file, "r", encoding="utf-8") as file:
                return file.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"找不到提示文件 {self.prompt_file}!")

    def load_intro(self):
        """
        从 JSON 文件加载初始消息。
        """
        try:
            with open(self.intro_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"找不到初始消息文件 {self.intro_file}!")
        except json.JSONDecodeError:
            raise ValueError(f"初始消息文件 {self.intro_file} 包含无效的 JSON!")

    def create_chatbot(self):
        """
        初始化聊天机器人，包括系统提示和消息历史记录。
        """
        # 创建聊天提示模板，包括系统提示和消息占位符
        system_prompt = ChatPromptTemplate.from_messages([
            ("system", self.prompt),  # 系统提示部分
            MessagesPlaceholder(variable_name="messages"),  # 消息占位符
        ])

        # 初始化 ChatOllama 模型，配置模型参数
        self.chatbot = system_prompt | ChatOpenAI(
            temperature=0.95,
            model="glm-4-flash",
            openai_api_key="51c7d9491590602cc291a879b3455f32.7PHWpwiNAVWfr8Dj",
            openai_api_base="https://open.bigmodel.cn/api/paas/v4/chat/completions",
            client=self.client,  # 使用自定义的客户端
        )

        # 将聊天机器人与消息历史记录关联
        self.chatbot_with_history = RunnableWithMessageHistory(self.chatbot, get_session_history)

    def chat_with_history(self, user_input, session_id=None):
        """
        处理用户输入，生成包含聊天历史的回复。

        参数:
            user_input (str): 用户输入的消息
            session_id (str, optional): 会话的唯一标识符

        返回:
            str: AI 生成的回复
        """
        if session_id is None:
            session_id = self.name
        try:
            history = get_session_history(session_id)
            messages = [{"role": "system", "content": self.prompt}]
            for msg in history.messages:
                if isinstance(msg, HumanMessage):
                    messages.append({"role": "user", "content": msg.content})
                elif isinstance(msg, AIMessage):
                    messages.append({"role": "assistant", "content": msg.content})
            messages.append({"role": "user", "content": user_input})

            response = self.client.chat.completions.create(
                model="glm-4-flash",
                messages=messages
            )
            bot_message = response.choices[0].message.content
            history.add_user_message(user_input)
            history.add_ai_message(bot_message)
            LOG.debug(f"API Response: {bot_message}")
            return bot_message
        except Exception as e:
            LOG.error(f"Error in chat_with_history: {str(e)}")
            return "Sorry, I encountered an error while processing your request."
