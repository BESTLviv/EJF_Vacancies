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
    
    return company_id, company_photo, company_description
