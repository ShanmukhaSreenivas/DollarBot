import pytest

class MockBot:
    """A mock bot class to simulate the behavior of the actual bot."""
    def __init__(self):
        self.sent_messages = []

    def send_message(self, chat_id, text, parse_mode=None):
        self.sent_messages.append((chat_id, text))

    def reply_to(self, message, text):
        self.sent_messages.append((message.chat.id, text))

    def register_next_step_handler(self, message, handler):
        # Simulate the behavior of registering a step handler
        handler(message)

class MockMessage:
    """A mock message class to simulate user messages."""
    def __init__(self, chat_id, text):
        self.chat = MockChat(chat_id)
        self.text = text

class MockChat:
    """A mock chat class to simulate chat details."""
    def __init__(self, chat_id):
        self.id = chat_id

# Mock helper functions
class MockHelper:
    """A mock helper class to simulate helper functions."""
    def __init__(self):
        self.savings_data = {}

    def set_savings_goal(self, chat_id, goal):
        self.savings_data[chat_id] = {"goal": goal, "spent": 0}

# Pytest fixtures
@pytest.fixture
def mock_bot():
    """Fixture to provide a fresh MockBot instance for each test."""
    return MockBot()

@pytest.fixture
def mock_helper():
    """Fixture to provide a fresh MockHelper instance for each test."""
    return MockHelper()

# Mock feature functions
def set_savings_goal(message, bot, helper):
    """Mock implementation of setting a savings goal."""
    chat_id = message.chat.id
    goal = float(message.text)
    helper.set_savings_goal(chat_id, goal)
    bot.send_message(chat_id, f"Savings goal of ${goal} set successfully!")

# Test Cases
def test_set_savings_goal_case_1(mock_bot, mock_helper):
    """Test case 1: Valid goal setting."""
    message = MockMessage(chat_id=12345, text="100")
    set_savings_goal(message, mock_bot, mock_helper)
    assert len(mock_bot.sent_messages) == 1
    assert "Savings goal of $100.0 set successfully!" in mock_bot.sent_messages[0][1]

def test_set_savings_goal_case_2(mock_bot, mock_helper):
    """Test case 2: Valid goal setting."""
    message = MockMessage(chat_id=12346, text="200")
    set_savings_goal(message, mock_bot, mock_helper)
    assert len(mock_bot.sent_messages) == 1
    assert "Savings goal of $200.0 set successfully!" in mock_bot.sent_messages[0][1]

def test_set_savings_goal_case_3(mock_bot, mock_helper):
    """Test case 3: Valid goal setting."""
    message = MockMessage(chat_id=12347, text="300")
    set_savings_goal(message, mock_bot, mock_helper)
    assert len(mock_bot.sent_messages) == 1
    assert "Savings goal of $300.0 set successfully!" in mock_bot.sent_messages[0][1]

def test_set_savings_goal_case_4(mock_bot, mock_helper):
    """Test case 4: Valid goal setting."""
    message = MockMessage(chat_id=12348, text="400")
    set_savings_goal(message, mock_bot, mock_helper)
    assert len(mock_bot.sent_messages) == 1
    assert "Savings goal of $400.0 set successfully!" in mock_bot.sent_messages[0][1]

def test_set_savings_goal_case_5(mock_bot, mock_helper):
    """Test case 5: Valid goal setting."""
    message = MockMessage(chat_id=12349, text="500")
    set_savings_goal(message, mock_bot, mock_helper)
    assert len(mock_bot.sent_messages) == 1
    assert "Savings goal of $500.0 set successfully!" in mock_bot.sent_messages[0][1]

def test_set_savings_goal_case_6(mock_bot, mock_helper):
    """Test case 6: Valid goal setting."""
    message = MockMessage(chat_id=12350, text="600")
    set_savings_goal(message, mock_bot, mock_helper)
    assert len(mock_bot.sent_messages) == 1
    assert "Savings goal of $600.0 set successfully!" in mock_bot.sent_messages[0][1]

def test_set_savings_goal_case_7(mock_bot, mock_helper):
    """Test case 7: Valid goal setting."""
    message = MockMessage(chat_id=12351, text="700")
    set_savings_goal(message, mock_bot, mock_helper)
    assert len(mock_bot.sent_messages) == 1
    assert "Savings goal of $700.0 set successfully!" in mock_bot.sent_messages[0][1]

def test_set_savings_goal_case_8(mock_bot, mock_helper):
    """Test case 8: Valid goal setting."""
    message = MockMessage(chat_id=12352, text="800")
    set_savings_goal(message, mock_bot, mock_helper)
    assert len(mock_bot.sent_messages) == 1
    assert "Savings goal of $800.0 set successfully!" in mock_bot.sent_messages[0][1]

def test_set_savings_goal_case_9(mock_bot, mock_helper):
    """Test case 9: Valid goal setting."""
    message = MockMessage(chat_id=12353, text="900")
    set_savings_goal(message, mock_bot, mock_helper)
    assert len(mock_bot.sent_messages) == 1
    assert "Savings goal of $900.0 set successfully!" in mock_bot.sent_messages[0][1]

def test_set_savings_goal_case_10(mock_bot, mock_helper):
    """Test case 10: Valid goal setting."""
    message = MockMessage(chat_id=12354, text="1000")
    set_savings_goal(message, mock_bot, mock_helper)
    assert len(mock_bot.sent_messages) == 1
    assert "Savings goal of $1000.0 set successfully!" in mock_bot.sent_messages[0][1]

if __name__ == "__main__":
    pytest.main()