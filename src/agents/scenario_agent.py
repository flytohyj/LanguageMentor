import random

from langchain_core.messages import AIMessage  # 导入消息类

from .session_history import get_session_history  # 导入会话历史相关方法
from .agent_base import AgentBase
from utils.logger import LOG


class ScenarioAgent(AgentBase):
    """
       场景代理类，负责处理特定场景下的对话。
       """

    def __init__(self, scenario_name, session_id=None):
        prompt_file = f"../prompts/{scenario_name}_prompt.txt"
        intro_file = f"../content/intro/{scenario_name}.json"
        super().__init__(
            name=scenario_name,
            prompt_file=prompt_file,
            intro_file=intro_file,
            session_id=session_id
        )


    def start_new_session(self, session_id: str = None):
        """
        开始一个新的聊天会话，并发送初始AI消息。
        
        参数:
            session_id (str): 会话的唯一标识符
        """
        if session_id is None:
            session_id = self.name

        history = get_session_history(session_id)
        LOG.debug(f"[history]:{history}")

        if not history.messages:  # 检查历史记录是否为空
            initial_ai_message = random.choice(self.intro_messages)  # 随机选择初始AI消息
            history.add_message(AIMessage(content=initial_ai_message))  # 添加初始AI消息到历史记录
            return initial_ai_message
        else:
            return history.messages[-1].content  # 返回历史记录中的最后一条消息


