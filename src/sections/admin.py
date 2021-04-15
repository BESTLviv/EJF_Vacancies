from telebot.types import CallbackQuery

from ..data import Data, User
from .section import Section


class AdminSection(Section):
    def __init__(self, data: Data):
        super().__init__(data=data)

    def process_callback(self, call: CallbackQuery, user: User):
        action = call.data.split(";")[1]

    def process_text(self, text):
        pass