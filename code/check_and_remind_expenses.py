import helper
import logging
from datetime import datetime


def run(bot):
    """
    Checks if a user has logged any expenses for the day and sends a reminder if none are found.
    """
    try:
        # Replace this with actual logic to retrieve user IDs
        user_ids = helper.get_all_user_ids()  # Example function to get all bot users

        for chat_id in user_ids:
            # Fetch user history
            user_history = helper.getUserHistory(chat_id)

            # Filter today's expenses
            today = datetime.now().strftime('%d-%b-%Y')
            today_expenses = [
                record for record in user_history
                if record.split(',')[0] == today
            ]

            # If no expenses for today, send a reminder
            if not today_expenses:
                bot.send_message(chat_id, "Don't forget to log your expenses today! 📝")

    except Exception as e:
        logging.exception(f"Error in expense reminder: {str(e)}")