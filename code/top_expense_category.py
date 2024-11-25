import helper
import logging
from datetime import datetime
from exception import InvalidAmountError, InvalidCategoryError

def top_expense_category(message, bot):
    """
    Provides the user's top expense category based on recorded data.
    
    Args:
        message: Telegram message object.
        bot: Telegram bot object.

    Returns:
        Sends a message to the user with the top expense category and the total amount.
    """
    try:
        # Fetch user's expense history
        chat_id = message.chat.id
        user_history = helper.getUserHistory(chat_id)
        
        if not user_history or len(user_history) == 0:
            bot.send_message(chat_id, "No spending records found. Start adding expenses to track your spending!")
            return

        # Aggregate expenses by category
        category_totals = {}
        for record in user_history:
            date, category, amount = record.split(',')
            amount = float(amount.strip())
            category_totals[category] = category_totals.get(category, 0) + amount

        # Find the top expense category
        top_category = max(category_totals, key=category_totals.get)
        top_amount = category_totals[top_category]

        # Respond to the user
        bot.send_message(
            chat_id,
            f"Your top expense category is '{top_category}' with a total spending of ${top_amount:.2f}."
        )

    except Exception as e:
        logging.exception(f"Error in top_expense_category: {str(e)}")
        bot.send_message(chat_id, f"An error occurred while fetching your top expense category: {str(e)}")

# This function can now be added to the bot's command handlers for deployment.

