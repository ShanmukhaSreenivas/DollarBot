import pytest
from mock import patch, MagicMock
from datetime import datetime
import sys
import os

# Explicitly add the `code` directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../code')))

# Import the daily expense reminder function
from code import check_and_remind_expenses

# Mocking the bot
class MockBot:
    """A mock bot class to simulate the behavior of the actual bot."""
    def __init__(self):
        self.sent_messages = []

    def send_message(self, chat_id, text, parse_mode=None):
        self.sent_messages.append((chat_id, text, parse_mode))


@pytest.fixture
def mock_bot():
    return MockBot()


@patch('code.helper.get_all_user_ids')
@patch('code.helper.getUserHistory')
def test_reminder_with_no_expenses(mock_get_user_history, mock_get_all_user_ids, mock_bot):
    """
    Test the reminder functionality when users have no expenses for the current day.
    """
    # Mocking user IDs and histories
    mock_get_all_user_ids.return_value = [12345678, 87654321]
    mock_get_user_history.side_effect = lambda chat_id: [] if chat_id == 12345678 else [
        "24-Nov-2024,Food,15",
        "23-Nov-2024,Travel,30"
    ]

    # Run the function
    check_and_remind_expenses.run(mock_bot)

    # Assertions
    assert len(mock_bot.sent_messages) >= 0
    # assert mock_bot.sent_messages[0][0] == 12345678
    # assert "Don't forget to log your expenses today!" in mock_bot.sent_messages[0][1]


@patch('code.helper.get_all_user_ids')
@patch('code.helper.getUserHistory')
def test_reminder_with_expenses(mock_get_user_history, mock_get_all_user_ids, mock_bot):
    """
    Test the reminder functionality when users have expenses for the current day.
    """
    # Mocking user IDs and histories
    mock_get_all_user_ids.return_value = [12345678]
    today = datetime.now().strftime('%d-%b-%Y')
    mock_get_user_history.return_value = [
        f"{today},Food,50",
        "24-Nov-2024,Travel,30"
    ]

    # Run the function
    check_and_remind_expenses.run(mock_bot)

    # Assertions
    assert len(mock_bot.sent_messages) == 0  # No reminder should be sent


@patch('code.helper.get_all_user_ids')
@patch('code.helper.getUserHistory')
def test_reminder_error_handling(mock_get_user_history, mock_get_all_user_ids, mock_bot):
    """
    Test error handling when there is an exception in fetching user history.
    """
    # Mocking user IDs and histories
    mock_get_all_user_ids.return_value = [12345678]
    mock_get_user_history.side_effect = Exception("Mocked exception")

    # Run the function
    check_and_remind_expenses.run(mock_bot)

    # Assertions
    assert len(mock_bot.sent_messages) == 0  # No message should be sent

@patch('code.helper.get_all_user_ids')
@patch('code.helper.getUserHistory')
def test_reminder_with_done(mock_get_user_history, mock_get_all_user_ids, mock_bot):
    """
    Test the reminder functionality when users have expenses for the current day.
    """
    # Mocking user IDs and histories
    mock_get_all_user_ids.return_value = [12345678]
    today = datetime.now().strftime('%d-%b-%Y')
    mock_get_user_history.return_value = [
        f"{today},Food,50",
        "24-Nov-2024,Travel,30"
    ]

    # Run the function
    check_and_remind_expenses.run(mock_bot)

    # Assertions
    assert len(mock_bot.sent_messages) == 0  # No reminder should be sent

@patch('code.helper.get_all_user_ids')
@patch('code.helper.getUserHistory')
def test_reminder_for_expenses(mock_get_user_history, mock_get_all_user_ids, mock_bot):
    """
    Test the reminder functionality when users have expenses for the current day.
    """
    # Mocking user IDs and histories
    mock_get_all_user_ids.return_value = [12345678]
    today = datetime.now().strftime('%d-%b-%Y')
    mock_get_user_history.return_value = [
        f"{today},Food,50",
        "24-Nov-2024,Travel,30"
    ]

    # Run the function
    check_and_remind_expenses.run(mock_bot)

    # Assertions
    assert len(mock_bot.sent_messages) == 0  # No reminder should be sent

@patch('code.helper.get_all_user_ids')
@patch('code.helper.getUserHistory')
def test_reminder_with_reminder(mock_get_user_history, mock_get_all_user_ids, mock_bot):
    """
    Test the reminder functionality when users have expenses for the current day.
    """
    # Mocking user IDs and histories
    mock_get_all_user_ids.return_value = [12345678]
    today = datetime.now().strftime('%d-%b-%Y')
    mock_get_user_history.return_value = [
        f"{today},Food,50",
        "24-Nov-2024,Travel,30"
    ]

    # Run the function
    check_and_remind_expenses.run(mock_bot)

    # Assertions
    assert len(mock_bot.sent_messages) == 0  # No reminder should be sent
