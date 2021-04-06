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
            self.send_vacany_list(user)

        elif action == "":
            pass
        
        else:
            pass

    def process_text(self, text):
        pass

    
    def send_start_menu(self, user: User):
        company = Company.objects.filter()[0]
        
        # my vacancies
        btn_text = "Мої"
        btn_callback = self.form_hr_callback(action="VacList")
        btn_my_vacancies = InlineKeyboardButton(btn_text, btn_callback)


        self.bot.send_photo()


    

    def send_vacany_list(self, user: User):
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




    def quit_company_status(self, chat_id):
        pass