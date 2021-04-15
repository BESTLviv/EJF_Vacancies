from telebot.types import InlineKeyboardButton, CallbackQuery, InputMediaPhoto

from ..data import Data, User


class Section:
    def __init__(self, data: Data):
        self.data = data
        self.bot = data.bot

    def process_callback(self, call: CallbackQuery, user: User):
        pass

    def process_text(self, call: CallbackQuery, user: User):
        pass

    ################
    # Form Callbacks
    ################

    def form_admin_callback(
        self, action, user_id="", company_id="", vacancy_id="", edit=False, delete=False
    ):
        assert edit is not delete
        prev_msg_action = "Delete" if delete else "Edit"
        return f"Admin;{action};{user_id};{company_id};{vacancy_id};{prev_msg_action}"

    def form_hr_callback(
        self, action, user_id="", company_id="", vacancy_id="", edit=False, delete=False
    ):
        assert edit is not delete
        prev_msg_action = "Delete" if delete else "Edit"
        return f"HR;{action};{user_id};{company_id};{vacancy_id};{prev_msg_action}"

    def form_user_callback(self, action, user_id="", edit=False, delete=False):
        assert edit is not delete
        prev_msg_action = "Delete" if delete else "Edit"
        return f"User;{action};{user_id};{prev_msg_action}"

    #########
    # Buttons
    #########

    def create_delete_button(self):
        return InlineKeyboardButton(text="❌", callback_data="DELETE")

    def create_back_button(self, callback_data):
        text = "Назад"
        return InlineKeyboardButton(text=text, callback_data=callback_data)

    ##################
    # Answer Callbacks
    ##################

    def answer_in_development(self, call: CallbackQuery):
        in_development_text = "В розробці"
        self.bot.answer_callback_query(call.id, text=in_development_text)

    def answer_wrong_action(self, call: CallbackQuery):
        wrong_action_text = "Неправильний action в callback.data"
        self.bot.answer_callback_query(call.id, text=wrong_action_text)

    #######
    # Utils
    #######

    def send_message(
        self, call: CallbackQuery, text=None, photo=None, reply_markup=None
    ):
        """Send next message doing something with the previous message.\n
        Every callback_data must have parameter (the last one)
        that says what to do with previous message:
            "Delete" or "Edit"
        """
        chat_id = call.message.chat.id
        message_id = call.message.message_id
        prev_msg_action = call.data.split(";")[-1]

        # Do Smth with previous message (if needed)
        if prev_msg_action == "Delete":
            self.bot.delete_message(chat_id, message_id)

        elif (
            prev_msg_action == "Edit"
        ):  # TODO - add edit message caption (if it possible)
            try:
                if photo is None:
                    if call.message.text != text:
                        self.bot.edit_message_text(
                            chat_id=chat_id,
                            message_id=message_id,
                            text=text,
                            reply_markup=reply_markup,
                        )
                    else:
                        self.bot.edit_message_reply_markup(
                            chat_id=chat_id,
                            message_id=message_id,
                            reply_markup=reply_markup,
                        )
                # edit caption + photo
                else:
                    # if photo was edited
                    if call.message.photo[0].file_id == photo:
                        self.bot.edit_message_media(
                            chat_id=chat_id,
                            message_id=message_id,
                            media=InputMediaPhoto(photo, caption=text),
                            reply_markup=reply_markup,
                        )
                    # if text was edited
                    elif call.message.text != text:
                        self.bot.edit_message_caption(
                            chat_id=chat_id,
                            caption=text,
                            photo=photo,
                            reply_markup=reply_markup,
                        )
                    # if markup was edited
                    else:
                        self.bot.edit_message_reply_markup(
                            chat_id=chat_id,
                            message_id=message_id,
                            reply_markup=reply_markup,
                        )

                return
            except Exception:
                return

        # Send new message
        if photo is None:
            self.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
        else:
            try:
                self.bot.send_photo(
                    chat_id=chat_id,
                    caption=text,
                    photo=photo,
                    reply_markup=reply_markup,
                )
            except Exception:
                self.bot.send_message(
                    chat_id=chat_id, text=text, reply_markup=reply_markup
                )
