import pytest
from mock import MagicMock, patch
from code import helper, code  # Adjust imports based on your folder structure

class MockBot:
    """Mock bot class to simulate the bot's behavior."""
    def __init__(self):
        self.sent_messages = []

    def send_message(self, chat_id, text, reply_markup=None, parse_mode=None):
        self.sent_messages.append((chat_id, text, reply_markup, parse_mode))

    def reply_to(self, message, text):
        self.sent_messages.append((message.chat.id, text, None, None))


@pytest.fixture
def mock_bot():
    return MockBot()


@pytest.fixture
def mock_message():
    class MockMessage:
        def __init__(self, chat_id):
            self.chat = MagicMock(id=chat_id)
            self.text = ""
    return MockMessage(chat_id=123456)

#Test Setting a Savings Goal
@patch("code.helper.set_savings_goal")
def test_set_savings_goal(mock_set_savings_goal, mock_bot, mock_message):
    """Test the functionality for setting a savings goal."""
    mock_message.text = "500"  # User input for savings goal
    code.set_savings_goal(mock_message)

    # Assert the savings goal is set
    mock_set_savings_goal.assert_called_with(123456, 500)
    assert len(mock_bot.sent_messages) == 1
    chat_id, text, _, _ = mock_bot.sent_messages[0]
    assert chat_id == 123456
    assert "Savings goal of $500 set successfully!" in text

#Test Viewing Savings Progress
