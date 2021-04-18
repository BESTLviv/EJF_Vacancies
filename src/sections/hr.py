from telebot.types import CallbackQuery

from ..data import (
    Data,
    User,
    Company
)
from .section import Section
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


class HR(Section):

    def __init__(self, data: Data):
        super().__init__(data=data)

    def process_callback(self, call: CallbackQuery, user: User):
        action = call.data.split(";")[1]

        if action == "VacList":
            self.send_vacancy_list(user)

        elif action == "My_Company":
            self.show_my_company()
        
        elif action == "Sign_out_from_company":
            self.quit_company_status()

    def process_text(self, text):
        pass

    def send_start_menu(self, user: User):
        company = Company.objects.filter()[0]

        # my vacancies
        btn_text1 = "Мої вакансії"
        btn_text2 = "Моя компанія"
        btn_text3 = "Вийти з профілю компанії"

        btn_callback_vaclist = self.form_hr_callback(action="VacList")
        btn_callback_company = self.form_hr_callback(action="My_Company")
        btn_callback_sign_out = self.form_hr_callback(action="Sign_out_from_company")

        btn_my_vacancies = InlineKeyboardButton(btn_text1, btn_callback_vaclist)
        btn_my_company = InlineKeyboardButton(btn_text2, btn_callback_company)
        btn_sign_out_from_company = InlineKeyboardButton(btn_text3, btn_callback_sign_out)

        markup_inline = InlineKeyboardMarkup()
        self.bot.send_photo(user, company.photo_id, company.description)

        markup_inline.add(btn_my_vacancies)
        markup_inline.add(btn_my_company)
        markup_inline.add(btn_sign_out_from_company)

    def send_vacancy_list(self, user: User):
        pass

    def add_vacancy(self):
        pass
    
    def show_vacancy(self):
        pass

    def show_vacancy_stats(self):
        pass

    def show_vacancy_promotion(self):
        pass

    def promote_vacancy(self, to_global=False, to_category=False):
        pass

    def delete_vacancy(self):
        pass

    def change_vacancy_status(self, current_status: int):
        pass

    def show_my_company(self):
        pass

    def quit_company_status(self, chat_id):
        pass