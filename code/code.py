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
import top_expense_category
import check_and_remind_expenses
import urllib.parse
import dropbox  # Assuming helper functions are defined here as per the user’s original structure.
import matplotlib.pyplot as plt
from fpdf import FPDF
import os

import schedule
import threading

assert currencyconvert  # To indicate that it's intentionally imported
from datetime import datetime
from jproperties import Properties
from telebot import types
from telegram_bot_calendar import DetailedTelegramCalendar
from add import cal
from code import pdf  # Adjust the import based on your project structure
from savings_goals import save_goal_handler, check_savings_goal, update_savings_goal, reset_savings_goal, savings_summary

DROPBOX_ACCESS_TOKEN = ""


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
def show_help(message):
    chat_id = message.chat.id
    message_text = (
        "Here are the commands you can use:\n"
        "/add - Add a new expense 💵\n"
        "/history - View your expense history 📜\n"
        "/budget - Check your budget 💳\n"
        "/analytics - View graphical analytics 📊\n"
        "/currency - Convert between different currencies 💱\n"
        "/setgoal - Set a savings goal 🎯\n"
        "/checkgoal - Check your savings goal progress 📈\n"
        "/updategoal - Update your savings progress 💰\n"
        "/resetgoal - Reset your savings goal 🔄\n"
        "/summary - View a summary of your savings progress 📜\n"
        "For more info, type /faq or tap the button below 👇"
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("FAQ", callback_data="faq"))
    bot.send_message(chat_id, message_text, parse_mode="Markdown", reply_markup=keyboard)


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
    elif command == "top_category": 
        command_top_category(call.message)
    elif command == "savings":  # Add this condition
        command_savings(call.message)    
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
        # bot.send_message(call.message.chat.id, "Try using /help or explore other commands to see what I can do for you!")

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
    Generates, hosts a PDF on Dropbox, and provides social media links for sharing.
    """
    chat_id = message.chat.id
    
    # Path to the PDF file and Dropbox destination
    pdf_file_path = "expense_report.pdf"  # Ensure this is the generated PDF path
    dropbox_path = "/Shared/%s" % pdf_file_path  # Dropbox destination path
    
    # Upload PDF to Dropbox
    dropbox_link = upload_to_dropbox(pdf_file_path, dropbox_path)
    
    if dropbox_link:
        # Generate social media sharing links
        social_media_links = generate_social_media_links(dropbox_link)
        
        # Compose response message
        response_message = (
            "🎉 Your PDF is ready and hosted successfully!\n"
            "%s\n\n"
            "Share this link on social media:\n"
            "1. Facebook: [Share on Facebook](%s)\n"
            "2. Twitter: [Share on Twitter](%s)\n"
            "3. LinkedIn: [Share on LinkedIn](%s)"
        ) % (dropbox_link, social_media_links['Facebook'], social_media_links['Twitter'], social_media_links['LinkedIn'])
        bot.send_message(chat_id, response_message, parse_mode="Markdown")
    else:
        bot.send_message(chat_id, "❌ Oops! PDF is already generated")

def display_savings_progress(chat_id):
    savings_goal, savings = helper.calculate_savings_progress(chat_id)
    if savings_goal is None:
        bot.send_message(chat_id, "No savings goal set. Use 'Set Goal' to add one.")
    else:
        progress_message = (
            f"Savings Goal: ${savings_goal}\n"
            f"Spent This Month: ${savings_goal - savings}\n"
            f"Remaining Savings: ${savings if savings >= 0 else 0}\n"
            f"Goal Status: {'On Track!' if savings > 0 else 'Goal Exceeded!'}"
        )
        bot.send_message(chat_id, progress_message)

def set_savings_goal(message):
    try:
        chat_id = message.chat.id
        goal = float(message.text)
        helper.set_savings_goal(chat_id, goal)
        bot.send_message(chat_id, f"Savings goal of ${goal} set successfully!")
    except ValueError:
        bot.send_message(chat_id, "Invalid input. Please enter a numeric value.")


def handle_savings_options(message):
    chat_id = message.chat.id
    option = message.text

    if option == "Set Goal":
        msg = bot.send_message(chat_id, "Enter your monthly savings goal (in $):")
        bot.register_next_step_handler(msg, set_savings_goal)
    elif option == "View Progress":
        display_savings_progress(chat_id)
    elif option == "Back to Menu":
        start_and_menu_command(message)  # Redirect to the main menu
    else:
        bot.send_message(chat_id, "Invalid option. Please try again.")


@bot.message_handler(commands=["savings"])
def command_savings(message):
    """
    Handles the /savings command for users to set and track savings goals.
    """
    chat_id = message.chat.id
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("Set Goal", "View Progress", "Back to Menu")
    msg = bot.send_message(chat_id, "Choose an option:", reply_markup=markup)
    bot.register_next_step_handler(msg, handle_savings_options)


def generate_social_media_links(dropbox_link):
    """
    Generates social media links to share the Dropbox file link.
    """
    encoded_link = urllib.parse.quote(dropbox_link)
    facebook_url = "https://www.facebook.com/sharer/sharer.php?u=%s" % encoded_link
    twitter_url = "https://twitter.com/intent/tweet?url=%s&text=Check%%20out%%20this%%20expense%%20report!" % encoded_link
    linkedin_url = "https://www.linkedin.com/sharing/share-offsite/?url=%s" % encoded_link
    
    return {
        "Facebook": facebook_url,
        "LinkedIn": linkedin_url,
        "Twitter": twitter_url,
        
    }

def upload_to_dropbox(file_path, dropbox_path):
    """
    Uploads a file to Dropbox and returns the shared link.
    """
    try:
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
        with open(file_path, "rb") as file:
            dbx.files_upload(file.read(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)
        
        # Create a shareable link for the uploaded file
        shared_link_metadata = dbx.sharing_create_shared_link_with_settings(dropbox_path)
        return shared_link_metadata.url.replace("?dl=0", "?dl=1")  # Direct download link
    except Exception as e:
        logging.exception("Error uploading file to Dropbox: %s", e)
        return None

def run(message, bot_instance):
    """
    run(message, bot_instance): This is the main function used to implement the PDF save feature and share it on social media.
    """
    try:
        helper.read_json()
        chat_id = message.chat.id
        user_history = helper.getUserHistory(chat_id)
        msg = "Alright. Creating a PDF of your expense history!"
        bot_instance.send_message(chat_id, msg)

        # Generate and save the expense history figure
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        top = 0.8
        if len(user_history) == 0:
            plt.text(0.1, top, "No record found!", horizontalalignment="left", verticalalignment="center", transform=ax.transAxes, fontsize=20)
        for rec in user_history:
            date, category, amount = rec.split(",")
            rec_str = f"{amount}$ {category} expense on {date}"
            plt.text(0, top, rec_str, horizontalalignment="left", verticalalignment="center", transform=ax.transAxes, fontsize=14, bbox=dict(facecolor="red", alpha=0.3))
            top -= 0.15
        plt.axis("off")
        plt.savefig("expense_history.png")
        plt.close()

        # Create a PDF from generated images
        pdf_report = FPDF()  # Renamed from `pdf` to `pdf_report` to avoid conflict
        pdf_report.add_page()
        pdf_report.image("expense_history.png", x=10, y=10, w=180)
        pdf_report.output("expense_report.pdf", "F")

        # Upload to Dropbox and generate shareable link
        dropbox_link = upload_to_dropbox("expense_report.pdf", "/Shared/expense_report.pdf")
        
        if dropbox_link:
            # Generate social media links
            social_media_links = generate_social_media_links(dropbox_link)

            # Message with social media links
            response_message = (
                "🎉 Your expense report PDF is ready and hosted successfully!\n"
                f"{dropbox_link}\n\n"
                "Share this link on social media:\n"
                f"1. Facebook: [Share on Facebook]({social_media_links['Facebook']})\n"
                f"2. Twitter: [Share on Twitter]({social_media_links['Twitter']})\n"
                f"3. LinkedIn: [Share on LinkedIn]({social_media_links['LinkedIn']})"
            )
            bot_instance.send_message(chat_id, response_message, parse_mode="Markdown")
        else:
            bot_instance.send_message(chat_id, "❌ Oops! Couldn't upload the PDF. Please try again later.")

        # Clean up temporary files
        os.remove("expense_history.png")
        os.remove("expense_report.pdf")

    except Exception as e:
        logging.exception(str(e))
        bot_instance.reply_to(message, "Oops! " + str(e))
      

@bot.message_handler(commands=['top_category'])
def command_top_category(message):
    top_expense_category.run(message,bot)

# Schedule the reminder to run daily at 8 PM
schedule.every().day.at("20:00").do(lambda: check_and_remind_expenses.run(bot))

# schedule.every(1).minutes.do(lambda: check_and_remind_expenses.run(bot))

def run_scheduler():
    """
    Runs the schedule in a loop alongside the bot.
    """
    while True:
        schedule.run_pending()
        time.sleep(1)

@bot.message_handler(commands=["checkgoal"])
def command_checkgoal(message):
    """
    Handles the /checkgoal command to check savings progress.
    """
    try:
        check_savings_goal(bot, message)
    except Exception as e:
        logging.error(f"Error in /checkgoal command: {e}")
        bot.reply_to(message, "An error occurred while checking your savings goal.")
@bot.message_handler(commands=["updategoal"])
def command_updategoal(message):
    """
    Handles the /updategoal command to update savings progress.
    """
    try:
        update_savings_goal(bot, message)
    except Exception as e:
        logging.error(f"Error in /updategoal command: {e}")
        bot.reply_to(message, "An error occurred while updating your savings goal.")
@bot.message_handler(commands=["resetgoal"])
def command_resetgoal(message):
    """
    Handles the /resetgoal command to reset the savings goal.
    """
    try:
        reset_savings_goal(bot, message)
    except Exception as e:
        logging.error(f"Error in /resetgoal command: {e}")
        bot.reply_to(message, "An error occurred while resetting your savings goal.")


@bot.message_handler(commands=["summary"])
def command_summary(message):
    """
    Handles the /summary command to show a savings summary.
    """
    try:
        savings_summary(bot, message)
    except Exception as e:
        logging.error(f"Error in /summary command: {e}")
        bot.reply_to(message, "An error occurred while showing your savings summary.")

from savings_goals import save_goal_handler

@bot.message_handler(commands=["setgoal"])
def command_setgoal(message):
    """
    Handles the /setgoal command to set a savings goal.
    """
    try:
        save_goal_handler(bot, message)
    except Exception as e:
        logging.error(f"Error in /setgoal command: {str(e)}")
        bot.reply_to(message, "An error occurred while setting your savings goal. Please try again.")

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
    # Start the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True  # Ensures the thread closes when the main program exits
    scheduler_thread.start()

    # Start the bot
    bot.polling(none_stop=True)

