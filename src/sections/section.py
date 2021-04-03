from telebot.types import InlineKeyboardButton

from ..data import (
    Data,
    User
)


class Section:

    def __init__(self, data: Data):
        self.data = data
        self.bot = data.bot

    def process_callback(self, call, user: User):
        pass

    ################
    # Form Callbacks
    ################

    def form_admin_callback(self, action, prev_msg_action=None):
        return f"Admin;{action};{prev_msg_action}"

    def form_hr_callback(self, action, prev_msg_action=None):
        return f"HR;{action};{prev_msg_action}"

    def form_user_callback(self, action, prev_msg_action=None):
        return f"User;{action};{prev_msg_action}"


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

    def in_development(self, call):
        in_development_text = self.data.message.under_development
        self.bot.answer_callback_query(call.id, text=in_development_text)

    #######
    # Utils
    #######

    def send_message(self, call, text=None, photo=None, reply_markup=None):
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

        elif prev_msg_action == "Edit":
            try:
                self.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, 
                                           reply_markup=reply_markup, parse_mode="HTML")
                return
            except:
                try:
                    self.bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, 
                                                       reply_markup=reply_markup, parse_mode="HTML")
                except:
                    return
                return
        
        # Send new message
        if photo is None:
            self.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup, parse_mode="HTML")
        else:
            try:
                self.bot.send_photo(chat_id=chat_id, caption=text, photo=photo, 
                                    reply_markup=reply_markup, parse_mode="HTML")
            except:
                self.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup, parse_mode="HTML")