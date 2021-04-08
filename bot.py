from src.data import Data

from src.sections.admin import Admin
from src.sections.hr import HR
from src.sections.user import User
from src.sections.job_fair import JobFair

from src.staff.updates import Updater
from src.staff import utils

import configparser
from telebot import TeleBot, logger



config = configparser.ConfigParser()
config.read('Settings.ini')

API_TOKEN = config['TG']['token']
CONNECTION_STRING = config['Mongo']['db']

bot = TeleBot(API_TOKEN, parse_mode="HTML")
data = Data(conn_string=CONNECTION_STRING, bot=bot)

admin_section = Admin(data=data)
hr_section = HR(data=data)
user_section = User(data=data)
job_fair_section = JobFair()

updater = Updater()



@bot.message_handler(commands=['start'])
def start_bot(message):
    user = updater.update_user_interaction_time(message)
    #bot.send_message(message.chat.id,  'Привіт ')

    # If in Job Fair mode
    #if False:
        #pass

    # If user is HR
    #elif user.hr_status is True:
        #hr_section.send_start_menu()

    # If user is basic user
    #else:
    user_section.send_start_menu(user)


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

@bot.message_handler(content_types=['text'])
def handle_text_buttons(message):
    user = updater.update_user_interaction_time(message)
    message_text = message.text
    
    try:
        if message_text in user_section.TEXT_BUTTONS:
            user_section.process_text(message_text, user)
        
        elif message_text in job_fair_section.TEXT_BUTTONS:
            job_fair_section.process_text(message_text, user)
    except:
        pass


if __name__ == "__main__":
    bot.polling(none_stop=True)

    updater.start_update_threads()