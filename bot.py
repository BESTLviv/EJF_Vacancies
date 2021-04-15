from src.data import Data, User

from src.sections.admin import AdminSection
from src.sections.hr import HRSection
from src.sections.user import UserSection
from src.sections.job_fair import JobFairSection

from src.staff.updates import Updater
from src.staff import utils

from src.objects import quiz

import configparser
from telebot import TeleBot, logger


config = configparser.ConfigParser()
config.read("Settings.ini")

API_TOKEN = config["TG"]["token"]
CONNECTION_STRING = config["Mongo"]["db"]

bot = TeleBot(API_TOKEN, parse_mode="HTML")
data = Data(conn_string=CONNECTION_STRING, bot=bot)

admin_section = AdminSection(data=data)
hr_section = HRSection(data=data)
user_section = UserSection(data=data)
job_fair_section = JobFairSection(data=data)

updater = Updater()

# data.add_start_quiz()


@bot.message_handler(commands=["start"])
def start_bot(message):
    user = updater.update_user_interaction_time(message)

    # If it is the first start
    if user.last_interaction_date == user.registration_date:
        send_welcome_message_and_start_quiz(user)

    # If in Job Fair mode
    elif False:
        pass

    # If user is HR
    elif user.hr_status is True:
        hr_section.send_start_menu(user=user)

    # If user is basic user
    else:
        user_section.send_start_menu(user=user)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    user = updater.update_user_interaction_time(call.message)
    section = call.data.split(";")[0]

    try:
        if section == "User":
            user_section.process_callback(call=call, user=user)

        elif section == "HR":
            hr_section.process_callback(call=call, user=user)

        elif section == "Admin":
            admin_section.process_callback(call=call, user=user)

    except:
        pass


@bot.message_handler(content_types=["text"])
def handle_text_buttons(message):
    user = updater.update_user_interaction_time(message)
    message_text = message.text

    try:

        if message_text in user_section.TEXT_BUTTONS:
            user_section.process_text(message_text, user)

        elif message_text in job_fair_section.TEXT_BUTTONS:
            job_fair_section.process_text(message_text, user)

        else:
            pass  # answer user that it was invalid input (in utils.py maybe)

    except:
        pass


def send_welcome_message_and_start_quiz(user: User):
    welcome_text = "Привіт друже!\nНарешті ярмарок...\nЯк класно..."
    bot.send_photo(user.chat_id, photo=data.TEST_PHOTO, caption=welcome_text)

    # if Job Fair not started
    if True:
        final_func = job_fair_section.send_start_menu

    # if Job Fair ended
    else:
        final_func = user_section.send_start_menu

    quiz.start_starting_quiz(user, bot, final_func)


if __name__ == "__main__":
    bot.polling(none_stop=True)

    updater.start_update_threads()