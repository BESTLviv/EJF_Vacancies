from ..data import Data, User, Quiz, Question
from telebot import TeleBot
from telebot.types import Message, KeyboardButton, ReplyKeyboardMarkup

from typing import Iterator, Callable
from time import sleep

import re

# start_quiz = {
#    "name_surname": {
#        "message": "Ім'я та прізвище",
#        "photo": None,
#        "buttons": None,
#        "input_type": "text",
#    },
# }


class InputException(Exception):
    pass


def start_starting_quiz(user: User, bot: TeleBot, final_func: Callable):
    start_quiz = Quiz.objects.filter(name="StartQuiz")[0]
    start_quiz_questions = start_quiz.questions

    quiz_iterator = iter(start_quiz_questions)
    question = next(quiz_iterator)

    sleep(1)

    send_question(
        user,
        bot,
        question,
        quiz_iterator,
        save_func=_save_answers_to_user,
        final_func=final_func,
        container={},
    )


def send_question(
    user: User,
    bot: TeleBot,
    question: Question,
    quiz_iterator: Iterator,
    save_func: Callable = None,
    final_func: Callable = None,
    container=None,
):
    chat_id = user.chat_id
    text = question.message

    # form markup
    answer_markup = _create_answer_markup(question)

    bot.send_message(chat_id, text, reply_markup=answer_markup)
    bot.register_next_step_handler_by_chat_id(
        chat_id,
        process_message,
        user=user,
        bot=bot,
        question=question,
        quiz_iterator=quiz_iterator,
        save_func=save_func,
        final_func=final_func,
        container=container,
    )


def process_message(message: Message, **kwargs):
    """
    :params user: User object.
    """
    user = kwargs["user"]
    bot = kwargs["bot"]
    question = kwargs["question"]
    quiz_iterator = kwargs["quiz_iterator"]
    save_func = kwargs["save_func"]
    final_func = kwargs["final_func"]
    container = kwargs["container"]

    content_type = message.content_type

    try:
        if content_type == question.input_type:

            if content_type == "text":

                input_text = message.text

                if question.allow_user_input:
                    # if there is a specific text input
                    if question.regex:
                        pattern = re.compile(question.regex)
                        if not pattern.search(input_text):
                            raise InputException

                    # if everything is all right -> save it to temp container
                    container[question.name] = input_text

                # if text input allowed only from keyboard
                else:
                    if input_text not in question.buttons:
                        raise InputException

                    container[question.name] = input_text

            elif content_type == "contact":
                contact = message.contact

                phone = contact.phone_number
                user_id = contact.user_id

                container["phone"] = phone
                container["user_id"] = user_id

            else:
                raise InputException

            question = next(quiz_iterator, None)

        # Wrong input type
        else:
            raise InputException

    except InputException:
        print("ex")
        bot.send_message(user.chat_id, text=question.wrong_answer_message)

    # do the next step
    if question:
        send_question(
            user=user,
            bot=bot,
            question=question,
            quiz_iterator=quiz_iterator,
            save_func=save_func,
            final_func=final_func,
            container=container,
        )
    # if questions ended
    else:
        # save data if needed
        if save_func:
            save_func(user, container)

        # send step after finish
        if final_func:
            final_func(user)


def _create_answer_markup(question: Question) -> ReplyKeyboardMarkup:
    answer_markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

    if question.input_type == "text":
        for button in question.buttons:
            answer_btn = KeyboardButton(text=button)
            answer_markup.add(answer_btn)

    elif question.input_type == "contact":
        answer_btn = KeyboardButton(text=question.buttons[0], request_contact=True)
        answer_markup.add(answer_btn)

    elif question.input_type == "location":
        answer_btn = KeyboardButton(text=question.buttons[0], request_location=True)
        answer_markup.add(answer_btn)

    return answer_markup


def _handle_commands(message: Message, command_text: str):

    if command_text == "\start":
        pass


def _save_answers_to_user(user: User, container):
    user.additional_info = container
    user.save()
