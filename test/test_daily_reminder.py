import pytest

class MockBot:
    """A mock bot class to simulate the behavior of the actual bot."""
    def __init__(self):
        self.sent_messages = []

    def send_message(self, chat_id, text, parse_mode=None):
        self.sent_messages.append((chat_id, text))

    def reply_to(self, message, text):
        self.sent_messages.append((message.chat.id, text))

# Mock implementation of `run_daily_reminder`
def run_daily_reminder(bot):
    """Simulate the daily reminder feature."""
    users = [12345, 67890, 0, -1]  # Mock user IDs
    for user_id in users:
        if user_id > 0:
            bot.send_message(user_id, "Don't forget to log your expenses today! 📝")
        else:
            bot.send_message(user_id, "Invalid user ID.")

# Test Cases for `daily_reminder`
def test_daily_reminder_valid_users():
    """Test the daily reminder for valid users."""
    bot = MockBot()
    run_daily_reminder(bot)
    assert len(bot.sent_messages) >= 2
    assert "Don't forget to log your expenses today! 📝" in bot.sent_messages[0][1]

def test_daily_reminder_invalid_user():
    """Test the daily reminder with an invalid user."""
    bot = MockBot()
    run_daily_reminder(bot)
    assert any("Invalid user ID." in msg[1] for msg in bot.sent_messages)

def test_daily_reminder_no_users():
    """Test the daily reminder when there are no users."""
    bot = MockBot()
    users = []  # Simulate no users
    for user_id in users:
        if user_id > 0:
            bot.send_message(user_id, "Don't forget to log your expenses today! 📝")
    assert len(bot.sent_messages) == 0

def test_daily_reminder_large_user_id():
    """Test the daily reminder with a large user ID."""
    bot = MockBot()
    users = [9999999999]  # Large user ID
    for user_id in users:
        if user_id > 0:
            bot.send_message(user_id, "Don't forget to log your expenses today! 📝")
    assert len(bot.sent_messages) == 1
    assert "Don't forget to log your expenses today! 📝" in bot.sent_messages[0][1]

def test_daily_reminder_boundary_user_id():
    """Test the daily reminder with a boundary user ID."""
    bot = MockBot()
    users = [0]  # Boundary case
    for user_id in users:
        if user_id > 0:
            bot.send_message(user_id, "Don't forget to log your expenses today! 📝")
        else:
            bot.send_message(user_id, "Invalid user ID.")
    assert len(bot.sent_messages) == 1
    assert "Invalid user ID." in bot.sent_messages[0][1]

def test_daily_reminder_duplicate_users():
    """Test the daily reminder for duplicate users."""
    bot = MockBot()
    users = [12345, 12345]  # Duplicate users
    for user_id in users:
        if user_id > 0:
            bot.send_message(user_id, "Don't forget to log your expenses today! 📝")
    assert len(bot.sent_messages) == 2
    assert all("Don't forget to log your expenses today! 📝" in msg[1] for msg in bot.sent_messages)

def test_daily_reminder_negative_user_id():
    """Test the daily reminder with a negative user ID."""
    bot = MockBot()
    users = [-1]  # Negative user ID
    for user_id in users:
        if user_id > 0:
            bot.send_message(user_id, "Don't forget to log your expenses today! 📝")
        else:
            bot.send_message(user_id, "Invalid user ID.")
    assert len(bot.sent_messages) == 1
    assert "Invalid user ID." in bot.sent_messages[0][1]

def test_daily_reminder_empty_user_id():
    """Test the daily reminder with an empty user ID."""
    bot = MockBot()
    users = [None]  # Empty user ID
    for user_id in users:
        if user_id:
            bot.send_message(user_id, "Don't forget to log your expenses today! 📝")
        else:
            bot.send_message(user_id, "Invalid user ID.")
    assert len(bot.sent_messages) == 1
    assert "Invalid user ID." in bot.sent_messages[0][1]

def test_daily_reminder_partial_users():
    """Test the daily reminder with a mix of valid and invalid user IDs."""
    bot = MockBot()
    users = [123, -1, 67890, 0]  # Mixed IDs
    for user_id in users:
        if user_id > 0:
            bot.send_message(user_id, "Don't forget to log your expenses today! 📝")
        else:
            bot.send_message(user_id, "Invalid user ID.")
    assert len(bot.sent_messages) == len(users)
    assert "Don't forget to log your expenses today! 📝" in bot.sent_messages[0][1]

def test_daily_reminder_complex_users():
    """Test the daily reminder with complex user inputs."""
    bot = MockBot()
    users = [12345, "invalid", 67890, -1]  # Mixed valid and invalid IDs
    for user_id in users:
        if isinstance(user_id, int) and user_id > 0:
            bot.send_message(user_id, "Don't forget to log your expenses today! 📝")
        else:
            bot.send_message(user_id, "Invalid user ID.")
    assert len(bot.sent_messages) == len(users)
    assert any("Invalid user ID." in msg[1] for msg in bot.sent_messages)

if __name__ == "__main__":
    pytest.main()
