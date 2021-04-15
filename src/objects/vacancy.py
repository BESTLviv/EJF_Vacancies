from typing import Iterator


def add_vacancy():

    add_vacancy_steps = [
        input_name,
        input_category,
        input_experience,
        input_work_type,
        input_description,
        finish_add_vacancy,
    ]

    steps_iterator = iter(add_vacancy_steps)


def input_name(next_step: Iterator = None):
    pass


def _process_input_name(message, **kwargs):
    next_step = kwargs["next_step"]

    if next(next_step, None) is not None:
        next_step(next_step)


def input_category(next_step: Iterator = None):
    pass


def _process_input_category(message, **kwargs):
    next_step = kwargs["next_step"]

    if next(next_step, None) is not None:
        next_step(next_step)


def input_experience(next_step: Iterator = None):
    pass


def _process_input_experience(message, **kwargs):
    next_step = kwargs["next_step"]

    if next(next_step, None) is not None:
        next_step(next_step)


def input_work_type(next_step: Iterator = None):
    pass


def _process_input_work_type(message, **kwargs):
    next_step = kwargs["next_step"]

    if next(next_step, None) is not None:
        next_step(next_step)


def input_description(next_step: Iterator = None):
    pass


def _process_input_description(message, **kwargs):
    next_step = kwargs["next_step"]

    if next(next_step, None) is not None:
        next_step(next_step)


def finish_add_vacancy(next_step: Iterator = None):
    pass