from ..data import User, Data
from ..objects import quiz
from ..sections.section import Section


class JobFairSection(Section):

    TEXT_BUTTONS = ["Компанії", "Папап"]

    BUTTONS_DICT = [
        {"name": "Компанії", "text": "афафіафіа", "photo": "wrgewgewf"},
        {"name": "Папап", "text": "афафіафіа", "photo": "wrgewgewf"},
    ]

    def __init__(self, data: Data):
        super().__init__(data)

    def process_text(self, text, user: User):
        pass

    def send_start_menu(self, user: User):

        markup
        for btn in self.BUTTONS_DICT:
            button(text=btn["name"])
            markup.add(button)

        self.bot.send_message(
            user.chat_id,
            text="Кінець.\nТут будуть кнопки ярмарку\n\n/start щоб пройти повторно",
        )

    def send_button_content(self, user: User, btn_text: str):
        for btn in self.BUTTONS_DICT:
            if btn["name"] == btn_text:
                self.bot.send_photo()
                return
