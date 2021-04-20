from telebot.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from ..data import Company, User, Vacancy
from ..sections.section import Section


def form_company_list_markup():
    # TODO import methos here
    pass


def form_company_description(call) -> tuple:
    company_id = call.data.split(";")[3]
    company = Company.objects.with_id(company_id)

    company_photo = company.photo_id
    company_description = (
        f"<b>Назва: </b> {company.name}\n"
        f"<b>Про компанію: </b> {company.description}\n"
    )
    # TODO add HR field

    return company_id, company_photo, company_description


def form_vacancy_info(vacancy_id) -> str:
    vacancy = Vacancy.objects.with_id(vacancy_id)

    if vacancy.is_active:
        status = "On"
    else:
        status = "Off"

    vacancy_description = (
        f"{vacancy.name}\n"
        f"<b>Статус</b>: {status}\n"
        f"<b>Досвід</b>: {vacancy.experience}\n"
        f"<b>Зарплата</b>: {vacancy.salary}\n"
        f"<b>Робочий день</b>: {vacancy.employment_type}\n"
        f"<b>Опис</b>: \n{vacancy.description}\n"
        f"<b>Вакансія дезактивується через: </b>: {vacancy.active_days_left} днів\n"
        f"<b>Додано</b>: {vacancy.add_date}\n"
        f"<b>Оновлено</b>: {vacancy.last_update_date}\n"
    )

    return vacancy_description