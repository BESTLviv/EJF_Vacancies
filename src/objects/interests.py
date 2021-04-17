from ..data import (
    User, EJF
)
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def update_interest(call, user: User, all_interests):
    action, is_selected, interest_index = call.data.split(';')[1:4]

    user_db = User.objects(chat_id=user.chat_id)[0]
    current_interests = list(user_db.interests)
    for index, interest in enumerate(all_interests):
        if interest_index == str(index):
            if is_selected == '0':  # not yet exists
                current_interests.append(interest)
            else:
                current_interests.remove(interest)
            break
    user_db.interests = current_interests
    user_db.save()


def update_items_list(current_items, right_index, is_selected, all):
    for index, interest in enumerate(all):
        if right_index == str(index):
            if is_selected == '0':  # not yet exists
                current_items.append(interest)
            else:
                current_items.remove(interest)
            return current_items


def create_interests_markup(current_interests):
    ROW_SIZE = 2
    all_interests = EJF.objects[0].filters_interest
    interest_markup = InlineKeyboardMarkup()

    number_count = 0
    interest_row = []
    for index, interest in enumerate(all_interests):
        interest_edited = interest + '✅' if interest in current_interests else interest
        is_selected = '1' if interest in current_interests else '0'

        callback = form_user_interests_callback(action='change_interest', is_selected=is_selected, interest_index=str(index))
        interest_but = InlineKeyboardButton(text=interest_edited, callback_data=callback)
        interest_row.append(interest_but)

        number_count += 1
        if number_count == ROW_SIZE:
            number_count = 0
            interest_markup.add(*interest_row)
            interest_row = []
    return interest_markup


def create_experience_markup(current_experience):
    ROW_SIZE = 3
    all_experience = EJF.objects[0].filters_experience
    experience_markup = InlineKeyboardMarkup()

    number_count = 0
    experience_row = []
    for index, experience in enumerate(all_experience):
        experience_edited = experience + '✅' if experience == current_experience else experience
        is_selected = '1' if experience in current_experience else '0'

        callback = form_user_interests_callback(action='change_experience', is_selected=is_selected, experience_index=str(index))
        experience_but = InlineKeyboardButton(text=experience_edited, callback_data=callback)
        experience_row.append(experience_but)

        number_count += 1
        if number_count == ROW_SIZE:
            number_count = 0
            experience_markup.add(*experience_row)
            experience_row = []
    return experience_markup


def create_employment_markup(current_employment):
    ROW_SIZE = 2
    all_employment = EJF.objects[0].filters_employment
    employment_markup = InlineKeyboardMarkup()

    number_count = 0
    employment_row = []
    for index, employment in enumerate(all_employment):
        employment_edited = employment + '✅' if employment == current_employment else employment
        is_selected = '1' if employment in current_employment else '0'

        callback = form_user_interests_callback(action='change_employment', is_selected=is_selected, employment_index=str(index))
        employment_but = InlineKeyboardButton(text=employment_edited, callback_data=callback)
        employment_row.append(employment_but)

        number_count += 1
        if number_count == ROW_SIZE:
            number_count = 0
            employment_markup.add(*employment_row)
            employment_row = []
    return employment_markup




def form_user_interests_callback(action, is_selected="", interest_index="", experience_index="", employment_index="", user_id="", prev_msg_action=None):
    return f"User;{action};{is_selected};{interest_index};{experience_index};{employment_index};{user_id};{prev_msg_action}"
