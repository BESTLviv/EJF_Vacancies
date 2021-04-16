from telebot.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from ..data import Data, User, Company
from .section import Section


class AdminSection(Section):
    def __init__(self, data: Data):
        super().__init__(data=data)

        self.admin_markup = self._form_admin_menu_markup()

    def process_callback(self, call: CallbackQuery, user: User):
        action = call.data.split(";")[1]

        if action == "CompanyList":
            self.send_company_list(call, user)

        elif action == "SendMessageMenu":
            self.send_mailing_menu(call, user)

        elif action == "Statistic":
            self.send_statistic(call, user)

        elif action == "CVMenu":
            self.send_cv_menu(call, user)

        else:
            self.answer_in_development(call)

    def process_text(self, text):
        pass

    def send_admin_menu(self, user: User):
        text = "Ну прівєт Адміністратор цього бота!"

        self.bot.send_message(
            chat_id=user.chat_id, text=text, reply_markup=self.admin_markup
        )

    def send_company_list(self, call: CallbackQuery, user: User) -> InlineKeyboardMarkup:
        chat_id = user.chat_id

        text = "Оберіть компанію для перегляду детальної інформації."
        markup = InlineKeyboardMarkup()

        for company in Company.objects:
            btn_text = company.name
            btn_callback = form_admin_callback(action="CompanyDetails", user_id=chat_id, company_id=company.name)
            btn = InlineKeyboardButton(btn_text, callback_data=btn_callback)
            markup.add(btn)

        self.bot.edit_message_text(chat_id=chat_id, text=text, reply_markup=markup)

    def send_company_info(self, chat_id="", company_name=""):
        company = Company.objects(tags=company_name)
        HR = company.HR
        text = (f"<b>Назва: </b> {company.name}\n"
                f"<b>Про компанію: </b> {company.description}\n"
                f"<b>HR: </b> {HR.name} {HR.surname}, {HR.username}\n")

        self.bot.send_photo(chat_id=chat_id, photo=company.photo_id, caption=text, parse_mode="HTML")

    def send_mailing_menu(self, call: CallbackQuery, user: User):
        self.answer_in_development(call)

    def send_statistic(self, call: CallbackQuery, uset: User):
        self.answer_in_development(call)

    def send_cv_menu(self, call: CallbackQuery, uset: User):
        self.answer_in_development(call)

    def _form_admin_menu_markup(self) -> InlineKeyboardMarkup:

        admin_markup = InlineKeyboardMarkup()

        # company button
        btn_text = "Компанії"
        btn_callback = self.form_admin_callback(action="CompanyList", edit=True)
        company_btn = InlineKeyboardButton(text=btn_text, callback_data=btn_callback)
        admin_markup.add(company_btn)

        # mailing button
        btn_text = "Розсилка"
        btn_callback = self.form_admin_callback(action="SendMessageMenu", edit=True)
        mailing_btn = InlineKeyboardButton(text=btn_text, callback_data=btn_callback)
        admin_markup.add(mailing_btn)

        # statistic button
        btn_text = "Статистика"
        btn_callback = self.form_admin_callback(action="Statistic", edit=True)
        statistic_btn = InlineKeyboardButton(text=btn_text, callback_data=btn_callback)
        admin_markup.add(statistic_btn)

        # cv button
        btn_text = "CV"
        btn_callback = self.form_admin_callback(action="CVMenu", edit=True)
        cv_btn = InlineKeyboardButton(text=btn_text, callback_data=btn_callback)
        admin_markup.add(cv_btn)

        return admin_markup

