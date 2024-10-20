import unittest
from unittest.mock import patch, MagicMock
from src.agents.conversation_agent import ConversationAgent
from langchain_core.messages import HumanMessage, AIMessage

class TestConversationAgent(unittest.TestCase):
    def setUp(self):
        self.agent = ConversationAgent()

    def test_init(self):
        self.assertIsNotNone(self.agent.prompt)
        self.assertIsNotNone(self.agent.chatbot)
        self.assertIsNotNone(self.agent.chatbot_with_history)

    @patch('src.agents.conversation_agent.OpenAI')
    def test_chat(self, mock_openai):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Hello, I'm an AI assistant."
        mock_openai.return_value.chat.completions.create.return_value = mock_response

        result = self.agent.chat("Hello, AI!")
        self.assertEqual(result, "Hello, I'm an AI assistant.")

    @patch('src.agents.conversation_agent.OpenAI')
    @patch('src.agents.conversation_agent.get_session_history')
    def test_chat_with_history(self, mock_get_history, mock_openai):
        mock_history = MagicMock()
        mock_history.messages = [
            HumanMessage(content="Previous user message"),
            AIMessage(content="Previous AI response")
        ]
        mock_get_history.return_value = mock_history

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "I remember our conversation."
        mock_openai.return_value.chat.completions.create.return_value = mock_response

        result = self.agent.chat_with_history("Do you remember our conversation?")
        self.assertEqual(result, "I remember our conversation.")
        self.assertEqual(len(mock_history.messages), 4)

    @patch('src.agents.conversation_agent.OpenAI')
    def test_chat_error_handling(self, mock_openai):
        mock_openai.return_value.chat.completions.create.side_effect = Exception("API Error")
        result = self.agent.chat("This should fail")
        self.assertIn("Sorry, I encountered an error", result)


if __name__ == '__main__':
    unittest.main()