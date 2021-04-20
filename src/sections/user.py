from telebot.types import (
    CallbackQuery,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from ..data import Data, User, JobFair, Vacancy
from ..objects import quiz
from .section import Section
from ..objects import interests
from ..objects import vacancy
from random import randint


class UserSection(Section):
    TEXT_BUTTONS = ["Найти вакансію", "Хто ми?", "Профіль"]

    def __init__(self, data: Data):
        super().__init__(data=data)

    def process_callback(self, call: CallbackQuery, user: User):
        action = call.data.split(";")[1]

        if action == "ApplyCV":
            vacancy_id = call.data.split(";")[3]
            self.apply_for_vacancy(user, vacancy_id, cv=True)

        elif action == "Interests":
            self.send_interests(user)

        else:
            self.answer_wrong_action(call)

    def process_text(self, text: str, user: User):

        if text == self.TEXT_BUTTONS[0]:
            self.send_new_vacancy(user)

        elif text == self.TEXT_BUTTONS[1]:
            self.send_about_info(user)

        elif text == self.TEXT_BUTTONS[2]:
            self.send_profile_menu(user)

    def send_start_menu(self, user: User):
        ejf = self.data.get_ejf()

        btn_vacancy = KeyboardButton(text=self.TEXT_BUTTONS[0])
        btn_who = KeyboardButton(text=self.TEXT_BUTTONS[1])
        btn_profile = KeyboardButton(text=self.TEXT_BUTTONS[2])

        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn_vacancy)
        markup.add(btn_who, btn_profile)

        self.bot.send_photo(
            user.chat_id,
            caption=ejf.content.user_start_text,
            photo=ejf.content.user_start_photo,
            reply_markup=markup,
        )

    def send_interests(self, user: User):
        pass

    def begin_start_quiz(self):
        pass

    def send_new_vacancy(self, user: User):
        vacancies_count = len(Vacancy.objects)
        random_number = randint(0, vacancies_count - 1)
        vacancies = list(Vacancy.objects)
        random_vacancy = vacancies[random_number]
        # TODO
        self.send_vacancy_info()

    def send_about_info(self, user: User):
        self.bot.send_message(user.chat_id, text="Test")

    def apply_for_vacancy(
            self, call: CallbackQuery, user: User, vacancy_id, cv=False, basic=False
    ):
        # TODO do apply for vacancy
        pass

    def send_profile_menu(self, user: User):
        self.bot.send_message(user.chat_id, text="Test")

    def change_account_type(self, user: User):
        pass

    def send_vacancy_info(self, user: User, vacancy_id):
        chat_id = user.chat_id
        vacancy_description = vacancy.form_vacancy_info(vacancy_id)
        vacancy_photo = Vacancy.objects.with_id(vacancy_id).company.photo_id
        # apply with CV button
        apply_markup = InlineKeyboardMarkup()
        btn_text = "Податися за допомогою CV"
        btn_callback = self.form_user_callback(
            action="ApplyCV", user_id=chat_id, vacancy_id=vacancy_id, edit=True
        )
        btn = InlineKeyboardButton(text=btn_text, callback_data=btn_callback)
        apply_markup.add(btn)

        # previous vacancy button
        apply_markup = InlineKeyboardMarkup()
        btn_text = "Попередня вакансія"
        btn_callback = self.form_user_callback(
            action="PreviousVacancy", user_id=chat_id, vacancy_id=vacancy_id, edit=True
        )
        btn = InlineKeyboardButton(text=btn_text, callback_data=btn_callback)
        apply_markup.add(btn)

        # next vacancy button
        apply_markup = InlineKeyboardMarkup()
        btn_text = "Наступна вакансія"
        btn_callback = self.form_user_callback(
            action="NextVacancy", user_id=chat_id, vacancy_id=vacancy_id, edit=True
        )
        btn = InlineKeyboardButton(text=btn_text, callback_data=btn_callback)
        apply_markup.add(btn)

        self.bot.send_photo(
            chat_id=user.chat_id,
            photo=vacancy_photo,
            caption=vacancy_description,
            reply_markup=apply_markup,
        )
