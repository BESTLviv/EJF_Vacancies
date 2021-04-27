from src.objects import vacancy
from telebot.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from telebot import logger

from ..data import Data, User, JobFair, Company, Vacancy
from .section import Section
from ..objects import company, vacancy

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

        elif action == "MailAll":
            self.mail_all(user)

        elif action == "MailMe":
            self.mail_me_test(user)

        elif action == "Statistic":
            self.send_statistic(call, user)

        elif action == "CVMenu":
            self.send_cv_menu(call, user)

        elif action == "CVDownloadNew":
            self.bot.answer_callback_query(call.id)
            self.send_cv_archive(call=call, user=user, update=True)

        elif action == "CVDownloadLast":
            self.send_cv_archive(call=call, user=user, update=False)

        elif action == "CompanyDetails":
            self.send_company_info(call, user)

        elif action == "VacancyList":
            self.send_vacancy_list(call, user)

        elif action == "CompanyKey":
            self.send_company_key(call, user)

        elif action == "VacancyInfo":
            self.send_vacancy_info(call, user)

        elif action == "DeleteVacancy":
            self.delete_vacancy(call, user)

        elif action == "ChangeVacancyStatus":
            self.change_vacancy_status(call, user)

        elif action == "VacancyStatistics":
            self.send_vacancy_statistics(call, user)

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

        company_list_markup = InlineKeyboardMarkup()
        for company in Company.objects:
            btn_text = company.name
            btn_callback = self.form_admin_callback(
                action="CompanyDetails", company_id=company.id, new=True
            )
            btn = InlineKeyboardButton(text=btn_text, callback_data=btn_callback)
            company_list_markup.add(btn)

        self.send_message(call, text, reply_markup=company_list_markup)

    def send_company_info(self, call: CallbackQuery, user: User):
        (
            company_id,
            company_photo,
            company_description,
        ) = company.form_company_description(call)
        markup = self._form_company_menu_markup(company_id=company_id)

        self.send_message(
            call, company_description, photo=company_photo, reply_markup=markup
        )

    def send_vacancy_list(self, call: CallbackQuery, user: User):
        text = "Вакансії"
        company_id = call.data.split(";")[3]
        company = Company.objects.with_id(company_id)

        vacancy_list_markup = InlineKeyboardMarkup()
        vacancy_list = Vacancy.objects.filter(company=company)
        for vacancy in vacancy_list:
            vacancy_text = vacancy.name
            vacancy_callback = self.form_admin_callback(
                action="VacancyInfo", vacancy_id=vacancy.id, new=True
            )
            vacancy_button = InlineKeyboardButton(
                text=vacancy_text, callback_data=vacancy_callback
            )
            vacancy_list_markup.add(vacancy_button)

        self.send_message(call, text=text, reply_markup=vacancy_list_markup)

    def send_vacancy_info(self, call: CallbackQuery, user: User):
        vacancy_id = call.data.split(";")[4]
        vacancy_description = company.form_vacancy_info(vacancy_id)
        markup = self._form_vacancy_menu_markup(vacancy_id)

        self.send_message(call, vacancy_description, reply_markup=markup)

    def delete_vacancy(self, call: CallbackQuery, user: User):
        result = vacancy.delete_vacancy(call)
        self.send_message(call, result)

    def change_vacancy_status(self, call: CallbackQuery, user: User):
        result = vacancy.change_vacancy_status(call)
        self.send_message(call, result)

    def send_vacancy_statistics(self, call: CallbackQuery, user: User):
        # TODO
        self.answer_in_development(call)

    def send_mailing_menu(self, call: CallbackQuery, user: User):
        chat_id = user.chat_id

        # form text
        user_count = User.objects.count()
        user_registered_count = User.objects.filter(additional_info__ne=None).count()
        user_not_blocked_count = User.objects.filter(is_blocked=False).count()
        text = (
            f"Всього стартануло бот - <b>{user_count}</b>\n"
            f"Пройшло реєстрацію - <b>{user_registered_count}</b>\n"
            f"Всього не заблокованих користувачів - <b>{user_not_blocked_count}</b>"
        )

        markup = self._form_mailing_markup()

        self.send_message(call, text, reply_markup=markup)

    def send_company_key(self, call: CallbackQuery, user: User):
        company_id = call.data.split(";")[3]
        company_key = Company.objects.with_id(company_id).token
        self.send_message(call, text=company_key)

    def send_mailing_menu(self, call: CallbackQuery, user: User):
        chat_id = user.chat_id

        # form text
        user_count = User.objects.count()
        user_registered_count = User.objects.filter(additional_info__ne=None).count()
        user_not_blocked_count = User.objects.filter(is_blocked=False).count()
        text = (
            f"Всього стартануло бот - <b>{user_count}</b>\n"
            f"Пройшло реєстрацію - <b>{user_registered_count}</b>\n"
            f"Всього не заблокованих користувачів - <b>{user_not_blocked_count}</b>"
        )

        markup = self._form_mailing_markup()

        self.send_message(call, text, reply_markup=markup)

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
                    self.bot.answer_callback_query(call.id)

            else:
                self.bot.answer_callback_query(
                    call.id, text="Архів ні разу не оновлювався!"
                )

    def mail_all(self, user: User):
        text = (
            "Надішли повідомлення яке потрібно розіслати всім\n\n"
            "Якщо потрібно вставити кнопку-посилання, то в останньому рядку тексту напиши посилання формату <b>https... ->btn_name</b>"
        )

        self.bot.send_message(user.chat_id, text=text)
        self.bot.register_next_step_handler_by_chat_id(
            user.chat_id, self._process_mail_users, auditory="all", user=user
        )

    def mail_me_test(self, user):
        text = (
            "Надішли повідомлення для тесту і я надішлю тобі його кінцевий вигляд\n\n"
            "Якщо потрібно вставити кнопку-посилання, то в останньому рядку тексту напиши посилання формату <b>https... ->btn_name</b>"
        )

        self.bot.send_message(user.chat_id, text=text)
        self.bot.register_next_step_handler_by_chat_id(
            user.chat_id, self._process_mail_users, auditory="me", user=user
        )

    def send_message_to_auditory(
        self,
        admin_chat_id,
        text: str,
        photo: str,
        markup: InlineKeyboardMarkup,
        user: User,
        auditory="all",
    ):
        def send_message(receiver: User, text=None, photo=None, markup=None):
            try:
                if photo:
                    self.bot.send_photo(
                        receiver.chat_id, caption=text, photo=photo, reply_markup=markup
                    )
                else:
                    self.bot.send_message(receiver.chat_id, text, reply_markup=markup)
                return True
            except Exception as e:
                err_text = f"User {receiver.username} {receiver.chat_id} didn't receive message - {e}"
                logger.error(err_text)
                self.bot.send_message(chat_id=admin_chat_id, text=err_text)
                receiver.is_blocked = True
                receiver.save()

        if auditory == "all":
            users = User.objects.filter(additional_info__ne=None)

            counter = 0

            for registered_user in users:
                if send_message(registered_user, text, photo, markup):
                    counter += 1

            success_text = f"Повідомлення відправлено {counter} користувачам"
            self.bot.send_message(chat_id=admin_chat_id, text=success_text)

        elif auditory == "me":
            send_message(user, text, photo, markup)

        self.send_admin_menu(user)

    def _process_mail_users(self, message, **kwargs):
        """
        :param auditory: "all" to mail all, else set it to one of auditory type from ejf_table
        :param user: user object from db
        """
        auditory = kwargs["auditory"]
        user = kwargs["user"]

        text = str()
        photo = str()
        url = str()
        markup = InlineKeyboardMarkup()

        if message.content_type == "text":
            text = message.text

        elif message.content_type == "photo":
            text = message.caption
            photo = message.photo[0].file_id

        else:
            self.mail_all(user)
            return

        # find if there is link in text and form markup
        try:
            if text:
                text_splitted = text.split("\n")
                last_row = text_splitted[-1]
                if "https" in last_row and "->" in last_row:
                    text = "\n".join(text_splitted[:-1])

                    # form button
                    url, btn_text = last_row.split("->")
                    btn = InlineKeyboardButton(text=btn_text, url=url)
                    markup.add(btn)
        except Exception as e:
            print(f"{e} during mailing")
            self.bot.send_message(
                message.chat.id, text=f"Щось пішло не так з посиланням - {e}"
            )

        self.send_message_to_auditory(
            admin_chat_id=message.chat.id,
            text=text,
            photo=photo,
            markup=markup,
            user=user,
            auditory=auditory,
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

    def _form_company_menu_markup(self, company_id) -> InlineKeyboardMarkup:

        company_menu_markup = InlineKeyboardMarkup()

        # company vacancies button
        btn_text = "Список вакансій"
        btn_callback = self.form_admin_callback(
            action="VacancyList", company_id=company_id, new=True
        )
        vacancy_list_btn = InlineKeyboardButton(
            text=btn_text, callback_data=btn_callback
        )
        company_menu_markup.add(vacancy_list_btn)

        # company key button
        btn_text = "Отримати ключ"
        btn_callback = self.form_admin_callback(
            action="CompanyKey", company_id=company_id, new=True
        )
        company_key_btn = InlineKeyboardButton(
            text=btn_text, callback_data=btn_callback
        )
        company_menu_markup.add(company_key_btn)

        return company_menu_markup

    def _form_vacancy_menu_markup(self, vacancy_id) -> InlineKeyboardMarkup:

        vacancy_menu_markup = InlineKeyboardMarkup()

        # delete vacancy
        btn_text = "Видалити вакансію"
        btn_callback = self.form_admin_callback(
            action="DeleteVacancy", vacancy_id=vacancy_id, new=True
        )
        delete_vacancy_btn = InlineKeyboardButton(
            text=btn_text, callback_data=btn_callback
        )
        vacancy_menu_markup.add(delete_vacancy_btn)

        # on\off
        btn_text = "On\Off"
        btn_callback = self.form_admin_callback(
            action="ChangeVacancyStatus", vacancy_id=vacancy_id, new=True
        )
        on_off_btn = InlineKeyboardButton(text=btn_text, callback_data=btn_callback)
        vacancy_menu_markup.add(on_off_btn)

        # send statistics
        btn_text = "Статистика"
        btn_callback = self.form_admin_callback(
            action="VacancyStatistics", vacancy_id=vacancy_id, new=True
        )
        vacancy_statistics_btn = InlineKeyboardButton(
            text=btn_text, callback_data=btn_callback
        )
        vacancy_menu_markup.add(vacancy_statistics_btn)

        return vacancy_menu_markup

    def _form_mailing_markup(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        # Mail all auditory
        btn_text = "Розсилка на всю аудиторію"
        btn_callback = self.form_admin_callback(action="MailAll", edit=True)
        btn_mail_all = InlineKeyboardButton(btn_text, callback_data=btn_callback)
        markup.add(btn_mail_all)

        # Mail me test
        btn_text = "Перевірити кінцеве повідомлення"
        btn_callback = self.form_admin_callback(action="MailMe", edit=True)
        btn_mail_me_test = InlineKeyboardButton(btn_text, callback_data=btn_callback)
        markup.add(btn_mail_me_test)

        # Back button
        btn_callback = self.form_admin_callback(action="AdminMenu", edit=True)
        back_btn = self.create_back_button(btn_callback)
        markup.add(back_btn)

        return markup
