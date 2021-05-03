from telebot.types import Message, KeyboardButton, CallbackQuery
from telebot import TeleBot

from typing import Callable

from src.data import User, JobFair, Data


help_msg = (
    "TEST COMMANDS HELP\n\n"
    "<b>ejf__help</b> - for help message\n"
    "<b>ejf__update</b> - for updating content from Database\n"
    "<b>ejf__resetquiz</b> - full start of bot (with start message and quiz)\n"
    "<b>ejf__user</b> - user start menu"
)


def process_tests_text(
    bot: TeleBot, user: User, data: Data, text: str, user_func: Callable
):
    test_action = text.split("__")[1]

    if test_action == "help":
        bot.send_message(user.chat_id, help_msg)

    elif test_action.startswith("edit"):
        btn_number = int(text.split("-")[-1])

    elif test_action == "update":
        data.update_ejf_table()
        bot.send_message(user.chat_id, text="EJF table has been updated")

    elif test_action == "resetquiz":
        user.additional_info = None
        user.save()
        bot.send_message(
            user.chat_id, text="You can now click /start and take a quiz again."
        )

    elif test_action == "user":
        user_func(user)
