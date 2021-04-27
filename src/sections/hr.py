from telebot.types import CallbackQuery

from ..data import Data, User, Company, Vacancy
from .section import Section
from ..objects import vacancy
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


class HRSection(Section):
    def __init__(self, data: Data):
        super().__init__(data=data)

    def process_callback(self, call: CallbackQuery, user: User):
        action = call.data.split(";")[1]

        if action == "StartMenu":
            self.send_start_menu(user, call)

        elif action == "VacList":
            self.send_vacancy_list(user, call)

        elif action == "CompanyInfo":
            pass

        elif action == "QuitHR":
            pass

        elif action == "VacInfo":
            pass

        else:
            pass

    def process_text(self, text):
        pass

    def register_hr(self, user: User):
        pass

    def send_start_menu(self, user: User, call: CallbackQuery = None):
        company = Company.objects.filter(HR=user).first()

        text = "Привіт HR!"
        photo = company.photo_id
        start_markup = self._form_start_markup(user)

        if call is None:
            self.bot.send_photo(
                chat_id=user.chat_id,
                caption=text,
                photo=photo,
                reply_markup=start_markup,
            )
        else:
            self.send_message(call, text=text, photo=photo, reply_markup=start_markup)

    def send_vacancy_list(self, user: User, call: CallbackQuery):
        company = Company.objects.filter(HR=user).first()

        vac_text = "Вакансії"
        company_photo = company.photo_id
        vac_list_markup = self._form_vac_list_markup(user, company)

        self.send_message(
            call, vac_text, photo=company_photo, reply_markup=vac_list_markup
        )

    def _form_start_markup(self, user: User) -> InlineKeyboardMarkup:
        start_markup = InlineKeyboardMarkup()

        # my vacancies
        btn_text1 = "Мої вакансії"
        btn_callback_vaclist = self.form_hr_callback(action="VacList", edit=True)
        btn_my_vacancies = InlineKeyboardButton(
            btn_text1, callback_data=btn_callback_vaclist
        )
        start_markup.add(btn_my_vacancies)

        # my company
        btn_text2 = "Моя компанія"
        btn_callback_company = self.form_hr_callback(action="CompanyInfo", edit=True)
        btn_my_company = InlineKeyboardButton(
            btn_text2, callback_data=btn_callback_company
        )
        start_markup.add(btn_my_company)

        # quit hr
        btn_text3 = "Вийти з профілю компанії"
        btn_callback_sign_out = self.form_hr_callback(action="QuitHR", edit=True)
        btn_sign_out_from_company = InlineKeyboardButton(
            btn_text3, callback_data=btn_callback_sign_out
        )
        start_markup.add(btn_sign_out_from_company)

        return start_markup

    def _form_vac_list_markup(
        self, user: User, company: Company
    ) -> InlineKeyboardMarkup:
        vac_list_markup = InlineKeyboardMarkup()

        vacancy_list = Vacancy.objects.filter(company=company)

        # Every vacancy list
        for vacancy in vacancy_list:
            button_text = vacancy.name
            callback = self.form_hr_callback(
                action="VacInfo", vacancy_id=vacancy.id, new=True
            )
            vacancy_button = InlineKeyboardButton(button_text, callback_data=callback)
            vac_list_markup.add(vacancy_button)

        # Add new vacancy btn
        btn_text = "Добавити нову"
        btn_callback = self.form_hr_callback(action="AddVacancy", edit=True)
        btn_new_vacancy = InlineKeyboardButton(btn_text, callback_data=btn_callback)
        vac_list_markup.add(btn_new_vacancy)

        # Back button
        btn_callback = self.form_hr_callback(action="StartMenu", edit=True)
        btn_back = self.create_back_button(btn_callback)
        vac_list_markup.add(btn_back)

        return vac_list_markup
