import unittest
from unittest.mock import patch, MagicMock
from src.tabs.scenario_tab import create_scenario_tab
from src.tabs.conversation_tab import create_conversation_tab
from src.tabs.vocab_tab import create_vocab_tab

class TestTabs(unittest.TestCase):
    @patch('src.tabs.scenario_tab.gr.Tab')
    def test_create_scenario_tab(self, mock_tab):
        create_scenario_tab()
        mock_tab.assert_called_once()

    @patch('src.tabs.conversation_tab.gr.Tab')
    def test_create_conversation_tab(self, mock_tab):
        create_conversation_tab()
        mock_tab.assert_called_once()

    @patch('src.tabs.vocab_tab.gr.Tab')
    def test_create_vocab_tab(self, mock_tab):
        create_vocab_tab()
        mock_tab.assert_called_once()

if __name__ == '__main__':
    unittest.main()
