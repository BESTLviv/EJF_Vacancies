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

        elif action == "VacInfo":
            vacancy_id = call.data.split(";")[3]
            vac, vacancy_index = self._get_vac_index(vacancy_id)
            self.send_vacancy_info(user, vac, vacancy_index, call)

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
        self.send_vacancy_info(user, random_vacancy, random_number)

    def send_about_info(self, user: User):
        self.bot.send_message(user.chat_id, text="Test")

    def apply_for_vacancy(
        self, call: CallbackQuery, user: User, vacancy_id, cv=False, basic=False
    ):
        # TODO do apply for vacancy(LOGS for checking if the user already applied)
        
        self.bot.send_message(user.chat_id, text="Заявку надіслано.")

        chat_id = Vacancy.objects.with_id(vacancy_id).company.HR.chat_id
        vacancy_name = Vacancy.objects.with_id(vacancy_id).name

        detail_markup = InlineKeyboardMarkup()
        detail_text = "Побачити деталі..."
        detail_callback = self.form_hr_callback(
            action="aplication_details", user_id=chat_id, edit=True
        )
        detail = InlineKeyboardButton(text=detail_text, callback_data=detail_callback)
        detail_markup.add(detail)

        user.apply_counter= user.apply_counter-1
        user.save()

        self.bot.send_message(chat_id,text = "Нова заявка на {vacancy_name}!".format(vacancy_name), reply_markup= detail_markup)
        


    def send_profile_menu(self, user: User):
        self.bot.send_message(user.chat_id, text="Test")

    def change_account_type(self, user: User):
        pass

    def send_vacancy_info(
        self, user: User, vac: Vacancy, cur_vac_index: int, call: CallbackQuery = None
    ):
        chat_id = user.chat_id
        vacancy_id = vac.id
        vacancy_description = vacancy.form_vacancy_info(vac)
        company_photo = vac.company.photo_id
        vacancies_list = list(Vacancy.objects)
        vacancy_info_menu_markup = self._form_vacancy_info_menu_markup(
            vac, vacancies_list, cur_vac_index
        )

        if call:
            self.send_message(
                call, vacancy_description, company_photo, vacancy_info_menu_markup
            )
        else:
            self.bot.send_photo(
                chat_id=user.chat_id,
                photo=company_photo,
                caption=vacancy_description,
                reply_markup=vacancy_info_menu_markup,
            )

    def _get_vac_index(self, vacancy_id) -> (Vacancy, int):
        vac = Vacancy.objects.with_id(vacancy_id)
        vacancies = list(Vacancy.objects)
        vacancy_index = vacancies.index(vac)
        return vac, vacancy_index

    def _form_vacancy_info_menu_markup(
        self, vac: Vacancy, vacancies_list: list, cur_vac_index: int
    ) -> InlineKeyboardMarkup:

        next_vac_index = int()

        if cur_vac_index == len(vacancies_list) - 1:
            next_vac_index = 0
        else:
            next_vac_index = cur_vac_index + 1

        prev_vac_index = cur_vac_index - 1

        prev_vac = vacancies_list[prev_vac_index]
        next_vac = vacancies_list[next_vac_index]

        # apply with CV button
        apply_markup = InlineKeyboardMarkup()
        btn_text = "Податися за допомогою CV"
        btn_callback = self.form_user_callback(
            action="ApplyCV", vacancy_id=vac.id, edit=True
        )
        btn_cv = InlineKeyboardButton(text=btn_text, callback_data=btn_callback)

        # previous vacancy button
        btn_text = "Попередня вакансія"
        btn_callback = self.form_user_callback(
            action="VacInfo", vacancy_id=prev_vac.id, edit=True
        )
        btn_prev = InlineKeyboardButton(text=btn_text, callback_data=btn_callback)

        # next vacancy button
        btn_text = "Наступна вакансія"
        btn_callback = self.form_user_callback(
            action="VacInfo", vacancy_id=next_vac.id, edit=True
        )
        btn_next = InlineKeyboardButton(text=btn_text, callback_data=btn_callback)

        apply_markup.add(btn_cv)
        apply_markup.add(btn_prev, btn_next)

        return apply_markup
