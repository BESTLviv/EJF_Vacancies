from telebot.types import CallbackQuery

from ..data import Data, User
from ..objects import quiz
from .section import Section
from ..objects import interests


class User(Section):

    TEXT_BUTTONS = ["Найти вакансію", "Хто ми?", "Профіль"]

    def __init__(self, data: Data):
        super().__init__(data=data)

    def process_callback(self, call: CallbackQuery, user: User):
        action = call.data.split(";")[1]

        if action == "ApplyCV":
            self.apply_for_vacancy(user, cv=True)

        elif action == "Apply":
            self.apply_for_vacancy(user, basic=True)

        elif action == "Interests":
            self.send_interests(user)

        else:
            self.answer_wrong_action(call)

    def process_text(self, text: str, user: User):

        if text == self.TEXT_BUTTONS[0]:
            self.send_new_vacancy(user)

        elif text == self.TEXT_BUTTONS[1]:
            pass

        elif text == self.TEXT_BUTTONS[2]:
            self.send_profile_menu(user)

    def send_start_menu(self):
        pass

    def send_interests(self, user: User):
        # interests.send_interests(user)
        pass

    def begin_start_quiz(self):
        # quiz.start_starting_quiz(bot=self.bot)
        pass

    def send_new_vacancy(self, user: User):
        pass

    def apply_for_vacancy(self, user: User, cv=False, basic=False):
        pass

    def send_profile_menu(self, user: User):
        pass

    def change_account_type(self, user: User):
        pass
