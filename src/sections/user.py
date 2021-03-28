from ..data import Data
from ..objects.quiz import Quiz
from .section import Section

class User(Section):

    BUTTONS = ["Найти вакансію", "Хто ми?", "Профіль"]

    def __init__(self, data: Data):
        super().__init__(data=data)
        
    def process_callback(self, call):
        pass

    def process_text(self, text):
        pass



    def begin_start_quiz(self):
        Quiz.start_starting_quiz(data=self.data)



    def send_new_vacancy(self):
        pass

    def apply_for_vacancy(self, chat_id, cv=False, basic=False):
        pass



    def send_profile_menu(self):
        pass



    def change_account_type(self, chat_id):
        pass


