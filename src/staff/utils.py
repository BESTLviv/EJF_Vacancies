from telebot.types import Message

from ..data import (
    User
)


def get_user_type(message: Message):
    chat_id = message.chat.id