from telebot.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from ..data import Data, User, JobFair, Company
from .section import Section
from ..objects import form_company_description, form_company_list_markup

from ..staff import utils


class AdminSection(Section):
    def __init__(self, data: Data):
        super().__init__(data=data)

        self.admin_markup = self._form_admin_menu_markup()

    def process_callback(self, call: CallbackQuery, user: User):
        action = call.data.split(";")[1]

        if action == "AdminMenu":
            self.send_admin_menu(user, call=call)

        elif action == "CompanyList":
            self.send_company_list(call, user)

        elif action == "SendMessageMenu":
            self.send_mailing_menu(call, user)

        elif action == "Statistic":
            self.send_statistic(call, user)

        elif action == "CVMenu":
            self.send_cv_menu(call, user)

        elif action == "CVDownloadNew":
            self.bot.answer_callback_query(call.id)
            self.send_cv_archive(call=call, user=user, update=True)

        elif action == "CVDownloadLast":
            self.send_cv_archive(call=call, user=user, update=False)

        else:
            self.answer_in_development(call)

    def process_text(self, text):
        pass

    def send_admin_menu(self, user: User, call: CallbackQuery = None):
        text = "Ну прівєт Адміністратор цього бота!"

        if call is None:
            self.bot.send_message(
                chat_id=user.chat_id, text=text, reply_markup=self.admin_markup
            )
        else:
            self.send_message(call, text=text, reply_markup=self.admin_markup)

    def send_company_list(self, call: CallbackQuery, user: User):
        text = "Оберіть компанію для перегляду детальної інформації."
        markup = form_company_list_markup(user)
        self.bot.edit_message_text(chat_id=user.chat_id, text=text, reply_markup=markup)

    def send_company_info(self, user_id, company_id):
        user = User.objects.filter(user_id=user_id)
        text = form_company_description(company_id=company_id)
        self.bot.send_photo(
            chat_id=user.chat_id,
            photo=company.photo_id,
            caption=text,
            parse_mode="HTML",
        )

    def send_mailing_menu(self, call: CallbackQuery, user: User):
        self.answer_in_development(call)

    def send_statistic(self, call: CallbackQuery, user: User):
        self.answer_in_development(call)

    def send_cv_menu(self, call: CallbackQuery, user: User):
        text = self._form_cv_menu_text()
        markup = self._form_cv_menu_markup()

        self.send_message(call, text=text, reply_markup=markup)

    def send_cv_archive(self, call: CallbackQuery, user: User, update: bool = False):
        ejf = self.data.get_ejf()
        chat_id = user.chat_id

        if update:
            utils.form_and_send_new_cv_archive(bot=self.bot, user=user)

        else:
            last_cv_zip_list = ejf.cv_archive_file_id_list

            if last_cv_zip_list:
                for archive in last_cv_zip_list:
                    self.bot.send_chat_action(chat_id, action="upload_document")
                    self.bot.send_document(chat_id=chat_id, data=archive)

            else:
                self.bot.answer_callback_query(
                    call.id, text="Архів ні разу не оновлювався!"
                )

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

    def _form_cv_menu_text(self) -> str:
        ejf = self.data.get_ejf()

        current_cv_number = self.data.get_cv_count()

        cv_menu_text = (
            f"<b>Загальна кількість загружених CV</b> - {current_cv_number}\n\n"
            f"<b>Останній час оновлення архіву</b> - {ejf.cv_archive_last_update}\n"
            f"<b>Кількість CV</b> - {ejf.cv_archive_size}"
        )

        return cv_menu_text

    def _form_cv_menu_markup(self) -> InlineKeyboardMarkup:
        cv_menu_markup = InlineKeyboardMarkup()

        # download last archive
        btn_text = "Завантажити останній архів CV"
        btn_callback = self.form_admin_callback(action="CVDownloadLast", edit=True)
        cv_last_btn = InlineKeyboardButton(text=btn_text, callback_data=btn_callback)
        cv_menu_markup.add(cv_last_btn)

        # create & download new archive
        btn_text = "Завантажити оновлений архів"
        btn_callback = self.form_admin_callback(action="CVDownloadNew", edit=True)
        cv_new_btn = InlineKeyboardButton(text=btn_text, callback_data=btn_callback)
        cv_menu_markup.add(cv_new_btn)

        # back button
        btn_callback = self.form_admin_callback(action="AdminMenu", edit=True)
        back_btn = self.create_back_button(callback_data=btn_callback)
        cv_menu_markup.add(back_btn)

        return cv_menu_markup
