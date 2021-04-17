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

        main_info = EJF.objects[0]
        self.all_interests, self.all_experience, self.all_employment = (
            main_info.filters_interest,
            main_info.filters_experience,
            main_info.filters_employment,
        )

    def process_callback(self, call: CallbackQuery, user: data.User):
        (
            action,
            is_selected,
            interest_index,
            experience_index,
            employment_index,
        ) = call.data.split(";")[1:6]

        if action == "ApplyCV":
            vacancy_id = call.data.split(";")[3]
            self.apply_for_vacancy(user, vacancy_id, cv=True)

        elif action == "VacInfo":
            vacancy_id = call.data.split(";")[3]
            vac, vacancy_index = self._get_vac_index(vacancy_id)
            self.send_vacancy_info(user, vac, vacancy_index, call)

        elif action == "Interests_menu":
            self.send_interests(user)

        elif action == "Experience_menu":
            self.send_experience(user)

        elif action == "Employment_menu":
            self.send_employment(user)

        elif action == "change_interest":
            self.send_interests(user, previous_message_id=call.message.message_id)

        elif action == "change_experience":
            if is_selected == "0":
                user.experience = self.all_experience[int(experience_index)]
                user.save()
                self.send_experience(user, previous_message_id=call.message.message_id)

        elif action == "change_employment":
            if is_selected == "0":
                user.employment = self.all_employment[int(employment_index)]
                user.save()
                self.send_employment(user, previous_message_id=call.message.message_id)

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

    def send_interests(self, call: CallbackQuery, user: User):
        all_interests = self.data.get_ejf().filters_interest
        interests.update_interest(call, user, all_interests)

        current_interests = user.interests
        interest_markup = interests.create_interests_markup(current_interests)
        if previous_message_id:
            self.data.bot.edit_message_reply_markup(
                user.chat_id,
                message_id=previous_message_id,
                reply_markup=interest_markup,
            )
        else:
            self.data.bot.send_message(
                user.chat_id, reply_markup=interest_markup, text="Hello"
            )

    def send_experience(self, user: data.User, previous_message_id=None):
        current_experience = user.experience
        experience_markup = interests.create_experience_markup(current_experience)
        if previous_message_id:
            self.data.bot.edit_message_reply_markup(
                user.chat_id,
                message_id=previous_message_id,
                reply_markup=experience_markup,
            )
        else:
            self.data.bot.send_message(
                user.chat_id, reply_markup=experience_markup, text="woooooow"
            )
        pass

    def send_employment(self, user: data.User, previous_message_id=None):
        current_employment = user.employment
        employment_markup = interests.create_employment_markup(current_employment)
        if previous_message_id:
            self.data.bot.edit_message_reply_markup(
                user.chat_id,
                message_id=previous_message_id,
                reply_markup=employment_markup,
            )
        else:
            self.data.bot.send_message(
                user.chat_id, reply_markup=employment_markup, text="wooooooooow"
            )

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
        # TODO do apply for vacancy
        pass

    def send_profile_menu(self, user: data.User):
        text_message = """
            Налаштуй критерії, сучка 😈.
            
            Резюме не закинув, тому вакансій для тебе немає, дОпобАчення!
            Підеш в Глово)
        """

        criteria_markup = InlineKeyboardMarkup()
        interest_but = InlineKeyboardButton(
            text="Інтереси",
            callback_data=interests.form_user_interests_callback(
                action="Interests_menu"
            ),
        )
        experience_but = InlineKeyboardButton(
            text="Досвід",
            callback_data=interests.form_user_interests_callback(
                action="Experience_menu"
            ),
        )
        employ_but = InlineKeyboardButton(
            text="Занятість",
            callback_data=interests.form_user_interests_callback(
                action="Employment_menu"
            ),
        )
        cv_but = InlineKeyboardButton(
            text="Резюме",
            callback_data=interests.form_user_interests_callback(action="cv"),
        )

        criteria_markup.add(interest_but)
        criteria_markup.add(experience_but)
        criteria_markup.add(employ_but)
        criteria_markup.add(cv_but)

        self.data.bot.send_message(
            user.chat_id, text=text_message, reply_markup=criteria_markup
        )

    def change_account_type(self, user: User):
        pass

    def send_vacancy_info(
        self, user: User, vac: Vacancy, cur_vac_index: int, call: CallbackQuery = None
    ):
        chat_id = user.chat_id
        vacancy_id = vac.id
        vacancy_description = vacancy.form_vacancy_info(vacancy=vac, status=False)
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
