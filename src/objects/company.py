from telebot.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from ..data import Company, User
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
    
    return company_photo, company_description

def form_vacancy_description(call) -> str:
    vacancy_id = call.data.split(";")[4]
    vacancy = Vacancy.objects.with_id(vacancy_id)

    vacancy_description = (
        f"<b>Тег: <\b> {vacancy.tag}\n"
        f"<b>Назва: <\b> {vacancy.name}\n"
        f"<b>Компанія: <\b> {vacancy.company}\n"
        f"<b>Досвід: <\b> {vacancy.experience}\n"
        f"<b>Зарплата: <\b> {vacancy.salary}\n"
        f"<b>Робочий день: <\b> {vacancy.employment_type}\n"
        f"<b>Опис: <\b>\n {vacancy.description}\n"
    )

    return vacancy_description