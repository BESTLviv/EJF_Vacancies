from telebot.types import ReplyKeyboardMarkup
from ..data import User, Data
from ..objects import quiz
from ..sections.section import Section
from telebot import types


class JobFairSection(Section):

    TEXT_BUTTONS = ["ІЯК 🦋", "Формат 💻", "Компанії 💼", "Розклад ⏰", "Зв'язок з нами ☎️"]

    BUTTONS_DICT = [
        {"name": "ІЯК 🦋",
         "text": "Інженерний Ярмарок Кар’єри - це знайомство студентів із провідними компаніями, які прагнуть почати свій кар'єрний шлях або змінити його напрям.",
         "photo": "https://cont.ws/uploads/pic/2019/3/regnum_picture_14956618541757852_big.png"},
        {"name": "Формат 💻",
         "text": "ІЯК проходитиме ОНЛАЙН.\n19-20 травня🙌🏻\n\nНадіємось ви раді почути таку новину🔥\n\nДавайте виокремимо переваги онлайн-події:\n ✔️поспілкуватись з представниками компаній;\n ✔️познайомитись з цікавими людьми;\n ✔️отримаєте досвід написаня CV;\n ✔️не буде жодних вірусів довкола;\n\nМи потурбувались, щоб вам було комфортно. Ви зможете провести час з користю, не виходячи з дому☺️",
         "photo": "https://cont.ws/uploads/pic/2019/3/regnum_picture_14956618541757852_big.png"},
        {"name": "Компанії 💼",
         "text": "КомпаніїКомпаніїКомпанії",
         "photo": "https://cont.ws/uploads/pic/2019/3/regnum_picture_14956618541757852_big.png"},
        {"name": "Розклад ⏰",
         "text": "РозкладРозкладРозклад",
         "photo": "https://cont.ws/uploads/pic/2019/3/regnum_picture_14956618541757852_big.png"},
        {"name": "Зв'язок з нами ☎️",
         "text":  "Головний організатор:\nЯрослав Когуч\n+380 50 621 96 74\nYaroslavkoguch1@gmail.com\n\nВідповідальні за корпоративні зв'язки:\nНазар Тутин\n+380 73 327 62 01\nNazar.tutyn@gmail.com\n\nАнна Погиба\n+380 97 044 55 28\nAnna.pohyba@gmail.com",
         "photo": "https://cont.ws/uploads/pic/2019/3/regnum_picture_14956618541757852_big.png"}
    ]

    def __init__(self, data: Data):
        super().__init__(data)

    def process_text(self, text, user: User):
        self.send_button_content(user, text)
        self.send_start_menu(user)
        return

    def send_start_menu(self, user: User):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        for btn in self.BUTTONS_DICT:
            button = types.KeyboardButton(btn["name"])
            keyboard.row(button)

        self.bot.send_message(user.chat_id, text="Викличте /start щоб пройти повторно", reply_markup=keyboard)

    def send_button_content(self, user: User, btn_text: str):
        for btn in self.BUTTONS_DICT:
            if btn["name"] == btn_text:
                return self.bot.send_photo(chat_id=user.chat_id, photo=btn["photo"], caption=btn["text"])

