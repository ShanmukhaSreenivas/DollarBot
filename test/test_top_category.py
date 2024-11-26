import pytest
from mock import MagicMock, patch

from code import top_expense_category

# Mocking the bot and helper modules
class MockBot:
    """A mock bot class to simulate the behavior of the actual bot."""
    def __init__(self):
        self.sent_messages = []

    def send_message(self, chat_id, text, parse_mode=None):
        self.sent_messages.append((chat_id, text, parse_mode))

    def reply_to(self, message, text):
        self.sent_messages.append((message.chat.id, text, None))


# Test cases for the Top Expense Category feature
@pytest.fixture
def mock_bot():
    return MockBot()


@pytest.fixture
def mock_message():
    class MockMessage:
        def __init__(self, chat_id):
            self.chat = MagicMock(id=chat_id)
    return MockMessage(chat_id=123456)


@patch('code.helper.getUserHistory')
def test_top_category_with_data(mock_get_user_history, mock_message, mock_bot):
    """Test the top expense category with valid expense data."""
    # Mock user history data
    mock_get_user_history.return_value = [
        "25-Nov-2024,Food,100",
        "25-Nov-2024,Travel,50",
        "25-Nov-2024,Food,150",
        "24-Nov-2024,Entertainment,200"
    ]

    # Run the function
    top_expense_category.run(mock_message, mock_bot)

    # Assert the correct message is sent
    assert len(mock_bot.sent_messages) == 1
    chat_id, message_text, _ = mock_bot.sent_messages[0]
    assert chat_id == 123456
    assert "Your top expense category is: **Food**" in message_text
    assert "Total spent: **$250.00**" in message_text


@patch('code.helper.getUserHistory')
def test_top_category_no_data(mock_get_user_history, mock_message, mock_bot):
    """Test the top expense category when no data is available."""
    # Mock empty user history
    mock_get_user_history.return_value = []

    # Run the function
    top_expense_category.run(mock_message, mock_bot)

    # Assert the reminder message is sent
    assert len(mock_bot.sent_messages) == 1
    chat_id, message_text, _ = mock_bot.sent_messages[0]
    assert chat_id == 123456
    assert "No spending records found." in message_text


@patch('code.helper.getUserHistory')
def test_top_category_error_handling(mock_get_user_history, mock_message, mock_bot):
    """Test error handling in the top expense category."""
    # Mock an exception in user history retrieval
    mock_get_user_history.side_effect = Exception("Mocked exception")

    # Run the function
    top_expense_category.run(mock_message, mock_bot)

    # Assert the error message is sent
    assert len(mock_bot.sent_messages) == 1
    chat_id, message_text, _ = mock_bot.sent_messages[0]
    assert chat_id == 123456
    assert "An error occurred" in message_text


@patch('code.helper.getUserHistory')
def test_top_category_tied_totals(mock_get_user_history, mock_message, mock_bot):
    """Test the case where multiple categories have the same total."""
    # Mock user history with tied totals
    mock_get_user_history.return_value = [
        "25-Nov-2024,Food,100",
        "25-Nov-2024,Travel,100"
    ]

    # Run the function
    top_expense_category.run(mock_message, mock_bot)

    # Assert one of the tied categories is selected as the top category
    assert len(mock_bot.sent_messages) == 1
    chat_id, message_text, _ = mock_bot.sent_messages[0]
    assert chat_id == 123456
    assert "Your top expense category is: **" in message_text
    assert "Total spent: **$100.00**" in message_text


@patch('code.helper.getUserHistory')
def test_top_category_large_numbers(mock_get_user_history, mock_message, mock_bot):
    """Test the top expense category with large expense amounts."""
    # Mock user history with large numbers
    mock_get_user_history.return_value = [
        "25-Nov-2024,Food,1000000",
        "25-Nov-2024,Travel,500000",
        "25-Nov-2024,Entertainment,200000"
    ]

    # Run the function
    top_expense_category.run(mock_message, mock_bot)

    # Assert the correct message is sent
    assert len(mock_bot.sent_messages) == 1
    chat_id, message_text, _ = mock_bot.sent_messages[0]
    assert chat_id == 123456
    assert "Your top expense category is: **Food**" in message_text
    assert "Total spent: **$1000000.00**" in message_text


@patch('code.helper.getUserHistory')
def test_top_category_decimal_values(mock_get_user_history, mock_message, mock_bot):
    """Test the top expense category with decimal values."""
    # Mock user history with decimal expenses
    mock_get_user_history.return_value = [
        "25-Nov-2024,Food,10.75",
        "25-Nov-2024,Travel,20.50",
        "25-Nov-2024,Food,15.25"
    ]

    # Run the function
    top_expense_category.run(mock_message, mock_bot)

    # Assert the correct message is sent
    assert len(mock_bot.sent_messages) == 1
    chat_id, message_text, _ = mock_bot.sent_messages[0]
    assert chat_id == 123456
    assert "Your top expense category is: **Food**" in message_text
    assert "Total spent: **$26.00**" in message_text


@patch('code.helper.getUserHistory')
def test_top_category_single_record(mock_get_user_history, mock_message, mock_bot):
    """Test the top expense category with a single record."""
    # Mock user history with a single record
    mock_get_user_history.return_value = ["25-Nov-2024,Food,100"]

    # Run the function
    top_expense_category.run(mock_message, mock_bot)

    # Assert the correct message is sent
    assert len(mock_bot.sent_messages) == 1
    chat_id, message_text, _ = mock_bot.sent_messages[0]
    assert chat_id == 123456
    assert "Your top expense category is: **Food**" in message_text
    assert "Total spent: **$100.00**" in message_text
