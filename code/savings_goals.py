import json
import os

GOALS_FILE = os.path.join('data', 'savings_goals.json')

def load_goals():
    if os.path.exists(GOALS_FILE):
        with open(GOALS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_goals(goals):
    with open(GOALS_FILE, 'w') as f:
        json.dump(goals, f, indent=4)

def save_goal_handler(bot, message):
    """
    Handles the process of setting a savings goal.
    """

    bot.reply_to(message, "Enter your savings goal amount (e.g., 500):")

    # Nested function to handle user input for savings goal
    def process_set_goal(msg):
        print(f"Received user input: {msg.text}")  # Debugging
        try:
            amount = float(msg.text.strip())  # Parse user input
            user_id = str(msg.chat.id)

            # Load and update the user's goals
            goals = load_goals()
            goals[user_id] = {"goal": amount, "saved": 0}
            save_goals(goals)

            bot.reply_to(msg, f"Savings goal set to ${amount:.2f}!")
        except ValueError:
            bot.reply_to(msg, "Invalid amount. Please enter a valid number.")

    # Register the next step handler
    bot.register_next_step_handler(message, process_set_goal)


def check_savings_goal(bot, message):
    goals = load_goals()  # Initialize goals
    user_id = str(message.chat.id)

    if user_id in goals:
        goal = goals[user_id]['goal']
        saved = goals[user_id]['saved']
        progress = (saved / goal) * 100

        reply = f"🎯 Your Savings Goal: ${goal:.2f}\n💰 Saved So Far: ${saved:.2f}\n📊 Progress: {progress:.2f}%"
        bot.reply_to(message, reply)
    else:
        bot.reply_to(message, "You haven't set a savings goal yet! Use /setgoal to set one.")

def update_savings_goal(bot, message):
    bot.reply_to(message, "Enter the amount you saved recently (e.g., 120):")
    bot.register_next_step_handler(message, lambda msg: process_update_goal(bot, msg))

def process_update_goal(bot, message):
    try:
        saved_amount = float(message.text.strip())
        user_id = str(message.chat.id)

        goals = load_goals()
        if user_id in goals:
            goals[user_id]['saved'] += saved_amount
            save_goals(goals)

            bot.reply_to(message, f"Added ${saved_amount:.2f} to your savings! Please use /checkgoal to see progress.")
        else:
            bot.reply_to(message, "You haven't set a savings goal yet! Please use /setgoal to set one.")
    except ValueError:
        bot.reply_to(message, "Invalid amount. Please enter a valid number.")


def reset_savings_goal(bot, message):
    goals = load_goals()  # Initialize goals
    user_id = str(message.chat.id)

    if user_id in goals:
        del goals[user_id]
        save_goals(goals)
        bot.reply_to(message, "Your savings goal has been reset!")
    else:
        bot.reply_to(message, "You don't have a savings goal set yet.")

def savings_summary(bot, message):
    goals = load_goals()  # Initialize goals
    user_id = str(message.chat.id)

    if user_id in goals:
        goal = goals[user_id]['goal']
        saved = goals[user_id]['saved']
        progress = (saved / goal) * 100
        remaining = goal - saved if saved < goal else 0

        reply = (
            f"🎯 Savings Goal: ${goal:.2f}\n"
            f"💰 Saved So Far: ${saved:.2f}\n"
            f"📊 Progress: {progress:.2f}%\n"
            f"🔜 Remaining to Goal: ${remaining:.2f}"
        )
        bot.reply_to(message, reply)
    else:
        bot.reply_to(message, "You haven't set a savings goal yet! Use /setgoal to set one.")

def notify_milestones(bot, message, user_id, saved, goal):
    goals = load_goals()  # Initialize goals
    milestones = [50, 100]
    progress = (saved / goal) * 100

    for milestone in milestones:
        if progress >= milestone and f"{milestone}%" not in goals[user_id].get("notified", []):
            bot.reply_to(message, f"🎉 Congratulations! You've reached {milestone}% of your savings goal!")
            goals[user_id].setdefault("notified", []).append(f"{milestone}%")
            save_goals(goals)
