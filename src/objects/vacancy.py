from typing import Iterator
from ..data import User, Vacancy, Data


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


def form_vacancy_info(vacancy: Vacancy) -> str:

    vacancy_description = (
        f"{vacancy.name}\n"
        f"<b>Досвід - </b>: {vacancy.experience}\n"
        f"<b>Опис</b>: \n{vacancy.description}\n"
        f"<b>Вакансія дезактивується через: </b>: {vacancy.active_days_left} днів\n"
    )

    return vacancy_description


def delete_vacancy(call) -> str:
    vacancy_id = call.data.split(";")[4]
    vacancy = Vacancy.objects.with_id(vacancy_id)

    vacancy_company = vacancy.company

    try:
        vacancy.delete()
        result = "Вакансію успішно видалено!"
        vacancy_company.vacancy_counter -= 1
    except:
        result = "Щось пішло не так :("

    return result


def change_vacancy_status(call) -> str:
    vacancy_id = call.data.split(";")[4]
    vacancy = Vacancy.objects.with_id(vacancy_id)

    if vacancy.is_active == True:
        vacancy.is_active = False
        result = "Вакансію вимкнено."

    elif vacancy.is_active == False:
        vacancy.is_active = True
        result = "Вакансію увімкнено."

    vacancy.save()

    return result