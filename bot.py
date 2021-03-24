import configparser
from data import Data
from telebot import TeleBot, logger

config = configparser.ConfigParser()
config.read('Settings.ini')

API_TOKEN = config['TG']['token']
DB = config['Mongo']['db']

bot = TeleBot(API_TOKEN, parse_mode="HTML")
data = Data(conn_string=DB)

@bot.message_handler(commands=['start'])
def start_bot(message):
    chat_id = message.chat.id
    username = message.chat.username if message.chat.username is not None else "Безіменний"
    name = message.chat.first_name if message.chat.first_name is not None else "Безіменний"
    surname = message.chat.last_name if message.chat.last_name is not None else "0"
    
    data.add_user(chat_id=chat_id, name=name, surname=surname, username=username)

    

if __name__ == "__main__":
    bot.polling(none_stop=True)