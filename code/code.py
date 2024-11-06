"""
File: code.py
Author: Vyshnavi Adusumelli, Tejaswini Panati, Harshavardhan Bandaru
Date: October 01, 2023
Description: File contains Telegram bot message handlers and their associated functions.

Copyright (c) 2023

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS," WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import telebot
import time
import helper
import edit
import history
import pdf
import display
import estimate
import delete
import add
import budget
import analytics
import predict
import updateCategory
import weekly
import monthly
import sendEmail
import voice
import add_recurring
import currencyconvert
import urllib.parse
assert currencyconvert  # To indicate that it's intentionally imported
from datetime import datetime
from jproperties import Properties
from telebot import types
from telegram_bot_calendar import DetailedTelegramCalendar
from add import cal
from code import pdf  # Adjust the import based on your project structure


configs = Properties()

with open("user.properties", "rb") as read_prop:
    configs.load(read_prop)

api_token = str(configs.get("api_token").data)

bot = telebot.TeleBot(api_token)

telebot.logger.setLevel(logging.INFO)

option = {}
user_list = {}

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# === Documentation of code.py ===

# Define listener for requests by user
def listener(user_requests):
    """
    listener(user_requests): Takes 1 argument user_requests and logs all user
    interaction with the bot including all bot commands run and any other issue logs.
    """
    for req in user_requests:
        if req.content_type == "text":
            print(
                "{} name:{} chat_id:{} \nmessage: {}\n".format(
                    str(datetime.now()),
                    str(req.chat.first_name),
                    str(req.chat.id),
                    str(req.text),
                )
            )

    message = (
        ("Sorry, I can't understand messages yet :/\n"
         "I can only understand commands that start with /. \n\n"
         "Type /faq or /help if you are stuck.")
    )

    try:
        helper.read_json()
        chat_id = user_requests[0].chat.id

        if user_requests[0].text[0] != "/":
            bot.send_message(chat_id, message)
    except Exception:
        pass

bot.set_update_listener(listener)

@bot.message_handler(commands=["help"])
def show_help(m):
    chat_id = m.chat.id
    message = (
        "*Here are the commands you can use:*\n"
        "/add - Add a new expense 💵\n"
        "/history - View your expense history 📜\n"
        "/budget - Check your budget 💳\n"
        "/analytics - View graphical analytics 📊\n"
        "/currency - Convert between different currencies 💱\n"
        "/socialmedia - generates a shareable link to the user's expense summary 📜\n"
        "For more info, type /faq or tap the button below 👇"
        
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("FAQ", callback_data='faq'))
    bot.send_message(chat_id, message, parse_mode='Markdown', reply_markup=keyboard)


@bot.message_handler(commands=["faq"])
def faq(m):

    helper.read_json()
    chat_id = m.chat.id

    faq_message = (
        ('"What does this bot do?"\n'
         ">> DollarBot lets you manage your expenses so you can always stay on top of them! \n\n"
         '"How can I add an epxense?" \n'
         ">> Type /add, then select a category to type the expense. \n\n"
         '"Can I see history of my expenses?" \n'
         ">> Yes! Use /analytics to get a graphical display, or /history to view detailed summary.\n\n"
         '"I added an incorrect expense. How can I edit it?"\n'
         ">> Use /edit command. \n\n"
         '"Can I check if my expenses have exceeded budget?"\n'
         ">> Yes! Use /budget and then select the view category. \n\n")
    )
    bot.send_message(chat_id, faq_message)

# defines how the /start and /help commands have to be handled/processed
@bot.message_handler(commands=["start", "menu"])
def start_and_menu_command(m):
    helper.read_json()
    chat_id = m.chat.id
    text_intro = (
        "*Welcome to the Dollar Bot!* \n"
        "DollarBot can track all your expenses with simple and easy-to-use commands :) \n"
        "Here is the complete menu:\n\n"
    )

    commands = helper.getCommands()
    keyboard = types.InlineKeyboardMarkup()

    for command, _ in commands.items():  # Unpack the tuple to get the command name
        button_text = f"/{command}"
        keyboard.add(types.InlineKeyboardButton(text=button_text, callback_data=command))  # Use `command` as a string

    text_intro += "_Click a command button to use it._"
    bot.send_message(chat_id, text_intro, reply_markup=keyboard, parse_mode='Markdown')
    return True

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """
    Handles button clicks and executes the corresponding command actions.
    """
    command = call.data  # The command from the button clicked
    response_text = ""

    # Check which command was clicked and perform the corresponding action
    if command == "help":
        show_help(call.message)
    elif command == "pdf":
        command_pdf(call.message)
    elif command == "add":
        command_add(call.message)
    elif command == "menu":
        start_and_menu_command(call.message)
    elif command == "add_recurring":
        command_add_recurring(call.messsage)
    elif command == "analytics":
        command_analytics(call.message)
    elif command == "predict":
        command_predict(call.message)
    elif command == "history":
        command_history(call.message)
    elif command == "delete":
        command_delete(call.message)
    elif command == "display":
        command_display(call.message)
    elif command == "edit":
        command_edit(call.message)
    elif command == "budget":
        command_budget(call.message)
    elif command == "updateCategory":
        command_updateCategory(call.message)
    elif command == "weekly":
        command_weekly(call.message)
    elif command == "monthly":
        command_monthly(call.message)
    elif command == "sendEmail":
        command_sendEmail(call.message)
    elif command == "faq":
        faq(call.message)
    elif command == "currency":  
        handle_currencies_command(call.message)   
    elif command == "socialmedia":  # New command added here
        command_socialmedia(call.message)      
    elif DetailedTelegramCalendar.func()(call):  # If it’s a calendar action
        cal(call,bot)
    else:
        response_text = "Command not recognized."

    # Acknowledge the button press
    bot.answer_callback_query(call.id)

     # Check if response_text is empty before sending
    if response_text:
        bot.send_message(call.message.chat.id, response_text, parse_mode='Markdown')
    else:
        logging.warning("Attempted to send an empty message for command: %s", command)
        bot.send_message(call.message.chat.id, "Try using /help or explore other commands to see what I can do for you!")

    bot.send_message(call.message.chat.id, response_text, parse_mode='Markdown')

def generate_response(_data):
    try:
        response = "Your generated response here"  # Replace with actual logic
        return response
    except Exception as e:
        logging.error("Error generating response: %s", e)
        return "⚠️ There was an error generating the response."

# defines how the /add command has to be handled/processed
@bot.message_handler(commands=["add"])
def command_add(message):
    """
    command_add(message) Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls add.py to run to execute
    the add functionality. Commands used to run this: commands=['add']
    """
    add.run(message, bot)

# defines how the /weekly command has to be handled/processed
@bot.message_handler(commands=["weekly"])
def command_weekly(message):
    """
    command_weekly(message) Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls weekly.py to run to execute
    the weekly analysis functionality. Commands used to run this: commands=['weekly']
    """
    weekly.run(message, bot)

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    """
    handle_voice(message) Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls voice.py to run to execute
    voice recognition functionality. Voice invkes this command
    """
    voice.run(message, bot)

# defines how the /monthly command has to be handled/processed
@bot.message_handler(commands=["monthly"])
def command_monthly(message):
    """
    command_monthly(message) Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls monthly.py to run to execute
    the monthly analysis functionality. Commands used to run this: commands=['monthly']
    """
    monthly.run(message, bot)

#handles add_recurring command
@bot.message_handler(commands=['add_recurring'])
def command_add_recurring(message):
    add_recurring.run(message, bot)

# handles pdf command
@bot.message_handler(commands=["pdf"])
def command_pdf(message):
    """
    command_history(message): Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls pdf.py to run to execute
    the add functionality. Commands used to run this: commands=['pdf']
    """
    pdf.run(message, bot)

#handles updateCategory command
@bot.message_handler(commands=["updateCategory"])
def command_updateCategory(message):
    """
    command_updateCategory(message): Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls updateCategory.py to run to execute
    the updateCategory functionality. Commands used to run this: commands=['updateCategory']
    """
    updateCategory.run(message, bot)

# function to fetch expenditure history of the user
@bot.message_handler(commands=["history"])
def command_history(message):
    """
    command_history(message): Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls history.py to run to execute
    the add functionality. Commands used to run this: commands=['history']
    """
    history.run(message, bot)

# function to fetch expenditure history of the user
@bot.message_handler(commands=["sendEmail"])
def command_sendEmail(message):
    """
    command_history(message): Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls sendEmail.py to run to execute
    the sending an email of the expense history. Commands used to run this: commands=['sendEmail']
    """
    sendEmail.run(message, bot)

# function to edit date, category or cost of a transaction
@bot.message_handler(commands=["edit"])
def command_edit(message):
    """
    command_edit(message): Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls edit.py to run to execute
    the add functionality. Commands used to run this: commands=['edit']
    """
    edit.run(message, bot)

# function to display total expenditure
@bot.message_handler(commands=["display"])
def command_display(message):
    """
    command_display(message): Takes 1 argument message which contains the message from the user
    along with the chat ID of the user chat. It then calls display.py to run to execute the add functionality.
    Commands used to run this: commands=['display']
    """
    display.run(message, bot)

# function to estimate future expenditure
@bot.message_handler(commands=["estimate"])
def command_estimate(message):
    """
    command_estimate(message): Takes 1 argument message which contains the message from the user
    along with the chat ID of the user chat. It then calls delete.py to run to execute the add functionality.
    Commands used to run this: commands=['estimate']
    """
    estimate.run(message, bot)

# handles "/delete" command
@bot.message_handler(commands=["delete"])
def command_delete(message):
    """
    command_delete(message): Takes 1 argument message which contains the message from the user
    along with the chat ID of the user chat. It then calls delete.py to run to execute the add functionality.
    Commands used to run this: commands=['display']
    """
    delete.run(message, bot)

# handles budget command
@bot.message_handler(commands=["budget"])
def command_budget(message):
    budget.run(message, bot)

# handles analytics command
@bot.message_handler(commands=["analytics"])
def command_analytics(message):
    """
    command_analytics(message): Take an argument message with content and chat ID. Calls analytics to 
    run analytics. Commands to run this commands=["analytics"]
    """
    analytics.run(message, bot)

# handles predict command
@bot.message_handler(commands=["predict"])
def command_predict(message):
    """
    command_predict(message): Take an argument message with content and chat ID. Calls predict to 
    analyze budget and spending trends and suggest a future budget. Commands to run this commands=["predict"]
    """
    predict.run(message, bot)

@bot.message_handler(commands=["currency"])
def handle_currencies_command(message):
    chat_id = message.chat.id
    user_history = helper.getUserHistory(chat_id)

    if user_history is None:
        bot.send_message(chat_id, "No spending records available!")
        return
    print("Retrieved user history:", user_history)

    # Ask user for target currency with reordered list including new currencies
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("GBP", "CAD", "INR", "CHF", "EUR")
    msg = bot.reply_to(message, "Which currency do you want to convert to?", reply_markup=markup)
    bot.register_next_step_handler(msg, process_currency_selection)

def process_currency_selection(message):
    chat_id = message.chat.id
    currency_code = message.text

    # Verify selected currency
    if currency_code not in ["GBP", "CAD", "INR", "CHF", "EUR"]:
        bot.send_message(chat_id, "Invalid currency selection.")
        return

    # Get spending data in selected currency
    hist= helper.getUserHistory(chat_id)
    query_results = []
    
    # Filter entries based on the current month and format them for the conversion function
    for entry in hist:
        try:
            entry_date = datetime.strptime(entry.split(',')[0], "%d-%b-%Y")
            if entry_date.strftime("%b-%Y") == datetime.now().strftime("%b-%Y"):
                query_results.append(entry)
        except ValueError:
            print("Skipping malformed date entry:", entry)  # Debug for malformed entries
    print("Filtered query results:", query_results)  # Debug output


    if query_results:
        try:
            # Sum the spendings from the current month's entries
            total_spendings = sum(float(entry.split(',')[2]) for entry in query_results)
            print("Total spendings in USD:", total_spendings)  # Debug

            # Convert the total spending to the selected currency
            converted_amount = helper.convert_currency(total_spendings, 'USD', currency_code)

            # Display the result or error message
            if converted_amount is not None:
                bot.send_message(chat_id, f"Your total spendings in {currency_code} is approximately {converted_amount:.2f}.")
            else:
                bot.send_message(chat_id, "Error during currency conversion.")
        except Exception as e:
            print("Error during conversion:", e)  # Log any errors
            bot.send_message(chat_id, "An error occurred while calculating spendings. Please try again.")
    else:
        bot.send_message(chat_id, "No spending history available for the current month.")


@bot.message_handler(commands=["socialmedia"])
def command_socialmedia(message):
    """
    command_socialmedia(message): Generates a shareable link for the user's expense summary 
    that can be posted on social media platforms.
    """
    chat_id = message.chat.id
    
    # Generate or fetch the link to the user's expense summary
    summary_link = generate_shareable_link(chat_id)
    
    if summary_link:
        # URL encode the summary link
        encoded_link = urllib.parse.quote(summary_link)

        # Message with options for social media platforms
        response_message = (
            "🎉 Your shareable link to your expense summary has been generated successfully!\n"
            f"{summary_link}\n\n"
            "Share this link on your favorite social media platforms:\n"
            f"1. Facebook: [Share on Facebook](https://www.facebook.com/sharer/sharer.php?u={encoded_link})\n"
            f"2. Twitter: [Share on Twitter](https://twitter.com/share?url={encoded_link}&text=Check%20out%20my%20expense%20summary!)\n"
            f"3. LinkedIn: [Share on LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url={encoded_link})"
        )
        bot.send_message(chat_id, response_message, parse_mode="Markdown")
    else:
        bot.send_message(chat_id, "❌ Oops! We couldn't generate a shareable link for you. Please try again later.")

def generate_shareable_link(chat_id):
    # Placeholder for link generation logic. Replace with actual implementation.
    return f"https://dollarbot.com/summary/{chat_id}"
      

def main():
    """
    main() The entire bot's execution begins here. It ensure the bot variable begins
    polling and actively listening for requests from telegram.
    """
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.exception(str(e))
        time.sleep(3)
        print("Connection Timeout")

if __name__ == "__main__":
    main() # type: ignore
