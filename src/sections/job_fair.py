from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from ..data import User, Data, JobFair
from ..objects import quiz
from ..sections.section import Section


class JobFairSection(Section):
    def __init__(self, data: Data):
        super().__init__(data)

        self.TEXT_BUTTONS = self._get_start_button_names()

    def process_text(self, text, user: User):
        self.send_button_content(user, text)

    def send_start_menu(self, user: User):
        ejf = self.data.get_ejf()

        start_message = ejf.content.ejf_start_text
        start_photo = ejf.content.ejf_start_photo
        markup = self._form_markup()

        self.bot.send_photo(
            user.chat_id,
            caption=start_message,
            photo=start_photo,
            reply_markup=markup,
        )

    def send_button_content(self, user: User, btn_text: str):
        ejf = self.data.get_ejf()

        for btn in ejf.start_menu:
            if btn["name"] == btn_text:
                return self.bot.send_photo(
                    chat_id=user.chat_id, photo=btn["photo"], caption=btn["text"]
                )

    def _get_start_button_names(self) -> list:
        ejf = self.data.get_ejf()

        button_names = list()

        for button in ejf.start_menu:
            button_names += [button["name"]]

        return button_names

    def _form_markup(self) -> ReplyKeyboardMarkup:
        def columns_generator(col=2):
            row = []

            for index, btn_name in enumerate(self.TEXT_BUTTONS, 1):
                row += [KeyboardButton(btn_name)]

                if index % col == 0:
                    yield row
                    row = []

            if row:
                yield row

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

        for btn_row in columns_generator():
            keyboard.row(*btn_row)

        return keyboard
