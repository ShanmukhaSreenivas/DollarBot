import pytest
from mock import MagicMock, patch
from code import code, helper  # Adjust imports based on your folder structure
# from code import helper

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
@patch("code.helper.calculate_savings_progress")
def test_display_savings_progress(mock_calculate_savings_progress, mock_bot, mock_message):
    """Test the savings progress display."""
    mock_calculate_savings_progress.return_value = (1000, 200)

    code.display_savings_progress(mock_message.chat.id)

    # Assert the correct progress is displayed
    assert len(mock_bot.sent_messages) == 1
    chat_id, text, _, _ = mock_bot.sent_messages[0]
    assert chat_id == 123456
    assert "Savings Goal: $1000" in text
    assert "Remaining Savings: $200" in text
    assert "Goal Status: On Track!" in text

#Test Invalid Input for Savings Goal
def test_set_savings_goal_invalid_input(mock_bot, mock_message):
    """Test handling of invalid input for savings goal."""
    mock_message.text = "abc"  # Invalid input
    code.set_savings_goal(mock_message)

    # Assert error message is sent
    assert len(mock_bot.sent_messages) == 1
    chat_id, text, _, _ = mock_bot.sent_messages[0]
    assert chat_id == 123456
    assert "Invalid input. Please enter a numeric value." in text

#Test No Savings Goal Set
@patch("code.helper.calculate_savings_progress")
def test_display_savings_progress_no_goal(mock_calculate_savings_progress, mock_bot, mock_message):
    """Test displaying progress when no savings goal is set."""
    mock_calculate_savings_progress.return_value = (None, None)

    code.display_savings_progress(mock_message.chat.id)

    # Assert reminder to set a savings goal
    assert len(mock_bot.sent_messages) == 1
    chat_id, text, _, _ = mock_bot.sent_messages[0]
    assert chat_id == 123456
    assert "No savings goal set. Use 'Set Goal' to add one." in text
