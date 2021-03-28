from ..data import Data
from .section import Section

class HR(Section):

    def __init__(self, data: Data):
        super().__init__(data=data)

    def process_callback(self, call):
        pass

    def process_text(self, text):
        pass

    

    def show_vacany_list(self):
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