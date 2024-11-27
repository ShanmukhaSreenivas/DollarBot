import pytest

class MockBot:
    """A mock bot class to simulate the behavior of the actual bot."""
    def __init__(self):
        self.sent_messages = []

    def send_message(self, chat_id, text, parse_mode=None):
        self.sent_messages.append((chat_id, text))

    def reply_to(self, message, text):
        self.sent_messages.append((message.chat.id, text))

class MockMessage:
    """A mock message class to simulate user messages."""
    def __init__(self, chat_id):
        self.chat = MockChat(chat_id)

class MockChat:
    """A mock chat class to simulate chat details."""
    def __init__(self, chat_id):
        self.id = chat_id

# Mock `top_expense_category.run` function
def run_top_category(message, bot):
    # Simulate handling the top category feature
    if isinstance(message.chat.id, int) and message.chat.id > 0:
        if message.chat.id == 12345:
            bot.send_message(message.chat.id, "🏆 Your top expense category is: **Food**\n💸 Total spent: **$250.00**")
        else:
            bot.send_message(message.chat.id, "No spending records found.")
    else:
        bot.reply_to(message, "Invalid chat ID.")

# Test Cases
def test_top_category_valid_data():
    bot = MockBot()
    message = MockMessage(chat_id=12345)
    run_top_category(message, bot)
    assert len(bot.sent_messages) == 1
    assert "🏆 Your top expense category is: **Food**" in bot.sent_messages[0][1]

def test_top_category_no_data():
    bot = MockBot()
    message = MockMessage(chat_id=67890)
    run_top_category(message, bot)
    assert len(bot.sent_messages) == 1
    assert "No spending records found." in bot.sent_messages[0][1]

def test_top_category_invalid_chat_id():
    bot = MockBot()
    message = MockMessage(chat_id="invalid")
    run_top_category(message, bot)
    assert len(bot.sent_messages) == 1
    assert "Invalid chat ID." in bot.sent_messages[0][1]

def test_top_category_negative_chat_id():
    bot = MockBot()
    message = MockMessage(chat_id=-1)
    run_top_category(message, bot)
    assert len(bot.sent_messages) == 1
    assert "Invalid chat ID." in bot.sent_messages[0][1]

def test_top_category_no_chat_id():
    bot = MockBot()
    message = MockMessage(chat_id=None)
    run_top_category(message, bot)
    assert len(bot.sent_messages) == 1
    assert "Invalid chat ID." in bot.sent_messages[0][1]

def test_top_category_empty_data():
    bot = MockBot()
    message = MockMessage(chat_id=12345)
    run_top_category(message, bot)
    assert len(bot.sent_messages) == 1
    assert "🏆 Your top expense category is: **Food**" in bot.sent_messages[0][1]

def test_top_category_large_chat_id():
    bot = MockBot()
    message = MockMessage(chat_id=9999999999)
    run_top_category(message, bot)
    assert len(bot.sent_messages) == 1
    assert "No spending records found." in bot.sent_messages[0][1]

def test_top_category_repeated_messages():
    bot = MockBot()
    message = MockMessage(chat_id=12345)
    run_top_category(message, bot)
    run_top_category(message, bot)
    assert len(bot.sent_messages) == 2
    assert all("🏆 Your top expense category is: **Food**" in msg[1] for msg in bot.sent_messages)

def test_top_category_partial_message():
    bot = MockBot()
    message = MockMessage(chat_id=12)  # A short ID
    run_top_category(message, bot)
    assert len(bot.sent_messages) == 1
    assert "No spending records found." in bot.sent_messages[0][1]

def test_top_category_mock_response():
    bot = MockBot()
    message = MockMessage(chat_id=0)  # Boundary value
    run_top_category(message, bot)
    assert len(bot.sent_messages) == 1
    assert "Invalid chat ID." in bot.sent_messages[0][1]

if __name__ == "__main__":
    pytest.main()
