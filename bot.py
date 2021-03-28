from src.data import Data

from src.sections.admin import Admin
from src.sections.hr import HR
from src.sections.user import User

from src.staff.updates import Updater

import configparser
from telebot import TeleBot, logger

config = configparser.ConfigParser()
config.read('Settings.ini')

API_TOKEN = config['TG']['token']
CONNECTION_STRING = config['Mongo']['db']

bot = TeleBot(API_TOKEN, parse_mode="HTML")
data = Data(conn_string=CONNECTION_STRING, bot=bot)

admin = Admin(data=data)
hr = HR(data=data)
user = User(data=data)

updater = Updater()



@bot.message_handler(commands=['start'])
def start_bot(message):
    chat_id = message.chat.id
    username = message.chat.username if message.chat.username is not None else "Безіменний"
    name = message.chat.first_name if message.chat.first_name is not None else "Безіменний"
    surname = message.chat.last_name if message.chat.last_name is not None else "0"
    
    data.add_user(chat_id=chat_id, name=name, surname=surname, username=username)



@bot.callback_query_handler(func=lambda call: "User" == call.data.split(";")[0])
def handle_user_query(call):
    
    try:
        user.process_callback(call=call)
    except:
        pass

@bot.callback_query_handler(func=lambda call: "HR" == call.data.split(";")[0])
def handle_hr_query(call):
    
    try:
        hr.process_callback(call=call)
    except:
        pass

@bot.callback_query_handler(func=lambda call: "Admin" == call.data.split(";")[0])
def handle_admin_query(call):
    
    try:
        admin.process_callback(call=call)
    except:
        pass

    

if __name__ == "__main__":
    bot.polling(none_stop=True)

    updater.start_update_threads()