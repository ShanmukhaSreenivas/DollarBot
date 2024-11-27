import helper
import logging
from datetime import datetime
from exception import InvalidAmountError, InvalidCategoryError

def run(message, bot):
    """
    Provides the user's top expense category based on recorded data.
    
    Args:
        message: Telegram message object.
        bot: Telegram bot object.

    Returns:
        Sends a message to the user with the top expense category and the total amount.
    """
    try:
        # Read the JSON data
        helper.read_json()
        chat_id = message.chat.id
        user_history = helper.getUserHistory(chat_id)

        # Check if user history exists
        if not user_history or len(user_history) == 0:
            bot.send_message(chat_id, "No spending records found. Start adding expenses to track your spending!")
            return

        # Aggregate expenses by category
        category_totals = {}
        for record in user_history:
            _, category, amount = record.split(',')
            amount = float(amount.strip())
            category_totals[category] = category_totals.get(category, 0) + amount

        # Find the top expense category
        top_category = max(category_totals, key=category_totals.get)
        top_amount = category_totals[top_category]

        # Create and send the response message
        response_message = (
            f"🏆 Your top expense category is: **{top_category}**\n"
            f"💸 Total spent: **${top_amount:.2f}**\n\n"
            "Keep tracking your expenses to achieve your financial goals!"
        )
        bot.send_message(chat_id, response_message, parse_mode="Markdown")

    except Exception as e:
        logging.exception(f"Error in run function for Top Expense Category Insight: {str(e)}")
        bot.reply_to(message, f"An error occurred: {str(e)}")

# This function can now be added to the bot's command handlers for deployment.