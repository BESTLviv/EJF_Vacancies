from telebot.types import Message, KeyboardButton, CallbackQuery
from telebot import TeleBot

from src.data import User, JobFair, Data


def process_tests_text(bot: TeleBot, user: User, data: Data, text: str):
    test_action = text.split("__")[1]

    if test_action == "help":
        pass

    elif test_action.startswith("edit"):
        btn_number = int(text.split("-")[-1])

    if test_action == "update":
        data.update_ejf_table()
        bot.send_message(user.chat_id, text="EJF table has been updated")
