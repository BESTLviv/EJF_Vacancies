from ..data import (
    User
)


def process_callback(call, user: User):
    pass

def create_interests_markup():
    pass


def create_experience_markup():
    pass


def create_work_time_markup():
    pass


def form_user_interests_callback(self, action, is_on, interest_index="", experience_index="", employment_index="", user_id="", prev_msg_action=None):
    return f"User;{action};{is_on};{interest_index};{experience_index};{employment_index};{user_id};{prev_msg_action}"