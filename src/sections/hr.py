from telebot.types import CallbackQuery

from ..data import Data, User, Company, Vacancy
from .section import Section
from ..objects import vacancy, quiz
from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
)


class HRSection(Section):
    def __init__(self, data: Data):
        super().__init__(data=data)

    def process_callback(self, call: CallbackQuery, user: User):
        action = call.data.split(";")[1]

        # check if user is HR
        if user.hr_status is False:
            self.bot.answer_callback_query(call.id, text="Ти наразі не HR :(")
            return

        if action == "StartMenu":
            self.send_start_menu(user, call)

        elif action == "VacList":
            self.send_vacancy_list(user, call)

        elif action == "CompanyInfo":
            pass

        elif action == "QuitHR":
            self.exit_hr(user, call)

        elif action == "VacInfo":
            pass

        elif action == "AddVacancy":
            self.add_new_vacancy(user)

        else:
            pass

    def process_text(self, text):
        pass

    def register_hr(self, user: User, login_str: str):
        company_key = login_str.split("_")[-1]

        company = Company.objects.filter(token=company_key).first()

        # check if company with such key exists
        if company is None:
            self.bot.send_message(
                user.chat_id, text="Компанії з таким ключем не існує :("
            )
            return

        # check if there is no HR in company
        if company.HR is not None:
            if company.HR.chat_id != user.chat_id:
                self.bot.send_message(
                    user.chat_id,
                    text=f"Упс!\nЗа компанією {company.name} вже закріплений користувач {user.name} @{user.username}",
                )
            else:
                self.send_start_menu(user)
            return

        # check if user is not HR yet
        if user.hr_status:
            self.bot.send_message(
                user.chat_id,
                text=f"Упс!\nТи вже належиш до іншої компанії :)",
            )
            return

        # connect hr to company is everything is all right
        company.HR = user
        company.save()

        user.hr_status = True
        user.save()

        # remove user keyboard
        del_message = self.bot.send_message(
            user.chat_id, text="Login suceeded", reply_markup=ReplyKeyboardRemove()
        )
        self.bot.delete_message(user.chat_id, del_message.message_id)

        self.send_start_menu(user)

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

    def send_vacancy_list(self, user: User, call: CallbackQuery = None):
        company = Company.objects.filter(HR=user).first()

        vac_text = "Вакансії"
        company_photo = company.photo_id
        vac_list_markup = self._form_vac_list_markup(user, company)

        if call is None:
            self.bot.send_photo(
                chat_id=user.chat_id,
                caption=vac_text,
                photo=company_photo,
                reply_markup=vac_list_markup,
            )
        else:
            self.send_message(
                call, vac_text, photo=company_photo, reply_markup=vac_list_markup
            )

    def add_new_vacancy(self, user: User):
        vacancy.start_add_vacancy_quiz(
            user, bot=self.bot, next_step=self.send_vacancy_list
        )

    def exit_hr(self, user: User, call: CallbackQuery):
        company = Company.objects.filter(HR=user).first()

        company.HR = None
        company.save()

        user.hr_status = False
        user.save()

        text = f"Ти успішно вийшов з компанії {company.name}!\n"
        self.send_message(call, text=text)

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
        btn_callback_sign_out = self.form_hr_callback(action="QuitHR", delete=True)
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
        btn_text = "➕Добавити нову➕"
        btn_callback = self.form_hr_callback(action="AddVacancy", edit=True)
        btn_new_vacancy = InlineKeyboardButton(btn_text, callback_data=btn_callback)

        # Back button
        btn_callback = self.form_hr_callback(action="StartMenu", edit=True)
        btn_back = self.create_back_button(btn_callback)

        vac_list_markup.add(btn_back, btn_new_vacancy)

        return vac_list_markup
