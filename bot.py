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

# data.add_start_quiz()аа


@bot.message_handler(commands=["start"])
def start_bot(message):
    user = updater.update_user_interaction_time(message)

    # If it is the first start
    if user.additional_info is None:
        send_welcome_message_and_start_quiz(user)

    # If in Job Fair mode
    elif user.last_interaction_date < data.JOB_FAIR_END_TIME:
        job_fair_section.send_start_menu(user)

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

        elif section == "DELETE":
            utils.delete_message(bot=bot, call=call)

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

        elif message_text == data.TEMP_ADMIN_PASSWORD:
            admin_section.send_admin_menu(user=user)

        elif message_text.startswith("ejf__"):
            utils.process_tests_text(bot, user, message_text)

        else:
            pass  # answer user that it was invalid input (in utils.py maybe)

    except Exception as e:
        print(e)


@bot.message_handler(content_types=["document"])
def test_save_cv(message):
    user = updater.update_user_interaction_time(message)
    chat_id = user.chat_id

    file_id = message.document.file_id
    file_name = message.document.file_name
    file_size = message.document.file_size

    if file_size > 1024 ** 2 * 5:
        bot.send_message(chat_id, text="Приймаю тільки файли менше 5 МБ (")

    elif file_name.split(".")[-1] != "pdf":
        bot.send_message(chat_id, text="Приймаю тільки файли формату pdf")

    else:
        user.cv_file_id = file_id
        user.cv_file_name = file_name
        user.save()
        bot.send_message(chat_id, text=f"Дякую {user.name}!")
        print(f"{user.name} загрузив {file_name} розміром {file_size/(1024**2)} МБ")


def send_welcome_message_and_start_quiz(user: User):
    welcome_text = data.get_ejf().content.start_text
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