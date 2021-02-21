import configparser
from telebot import Telebot

config = configparser.ConfigParser()
config.read('Settings.ini')

API_TOKEN = config['TG']['token']

if __name__ == "__main__":
    bot.polling(none_stop=True)