from ..data import User, Data
from ..objects import quiz
from ..sections.section import Section


class JobFair(Section):

    TEXT_BUTTONS = ["", ""]

    def __init__(self, data: Data):
        super().__init__(data)

    def process_text(self, text, user: User):
        pass

    def send_start_menu(self, user: User):
        pass
