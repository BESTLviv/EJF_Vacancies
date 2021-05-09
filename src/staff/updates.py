from datetime import datetime, timezone
import threading

from telebot.types import Message

from ..data import User, Company, Vacancy
from src.staff import utils


class Updater:
    def __init__(self):
        super().__init__()

    def start_update_threads(self):
        pass

    def update_user_interaction_time(self, message: Message) -> User:
        user_chat_id = message.chat.id
        date = utils.get_now()

        user = User.objects.filter(chat_id=user_chat_id)

        # add user if it does not exist
        if len(user) == 0:
            username = (
                message.chat.username
                if message.chat.username is not None
                else "No Nickname"
            )
            name = (
                message.chat.first_name
                if message.chat.first_name is not None
                else "No Name"
            )
            surname = (
                message.chat.last_name
                if message.chat.last_name is not None
                else "No Surname"
            )
            register_source = (
                message.text.split()[1] if len(message.text.split()) > 1 else "Unknown"
            )

            user = User(
                chat_id=user_chat_id,
                name=name,
                surname=surname,
                username=username,
                register_source=register_source,
                registration_date=date,
                last_update_date=date,
                last_interaction_date=date,
            )

            user.save()

        # update user if exists
        else:
            user = user[0]
            date = utils.get_now()
            user.update(last_interaction_date=date)

        return user
