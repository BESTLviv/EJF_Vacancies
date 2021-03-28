from datetime import datetime
import threading

from telebot.types import Message


class Updater:

    def __init__(self):
        super().__init__()

    def start_update_threads(self):
        pass


    def update_user_interaction_time(self, message: Message):
        username = message.chat.username if message.chat.username is not None else "No Nickname"
        name = message.chat.first_name if message.chat.first_name is not None else "No Name"
        surname = message.chat.last_name if message.chat.last_name is not None else "No Surname"
        user_chat_id = message.chat.id
        date = datetime.now()

        #adding user if it does not exist

        #updating
            