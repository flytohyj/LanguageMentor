import unittest
from unittest.mock import patch, MagicMock
from src.main import main

class TestMain(unittest.TestCase):

    @patch('src.main.gr.Blocks')
    @patch('src.main.create_scenario_tab')
    @patch('src.main.create_conversation_tab')
    @patch('src.main.create_vocab_tab')
    def test_main(self, mock_vocab_tab, mock_conv_tab, mock_scenario_tab, mock_blocks):
        mock_app = MagicMock()
        mock_blocks.return_value.__enter__.return_value = mock_app

        main()

        mock_scenario_tab.assert_called_once()
        mock_conv_tab.assert_called_once()
        mock_vocab_tab.assert_called_once()
        mock_app.launch.assert_called_once_with(share=True, server_name="0.0.0.0")

if __name__ == '__main__':
    unittest.main()