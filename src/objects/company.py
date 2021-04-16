from telebot.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from ..data import Company, User

def form_company_list_markup(user: User) -> InlineKeyboardMarkup:
    company_list_markup = InlineKeyboardMarkup()
        for company in Company.objects:
            btn_text = company.name
            btn_callback = self.form_admin_callback(action="CompanyDetails", user_id=user.id, company_id=company.id, edit=True)
            btn = InlineKeyboardButton(btn_text, callback_data=btn_callback)
            company_list_markup.add(btn)

    return company_list_markup
    

def form_company_description(company_id) -> str:
        company = Company.objects.with_id(company_id)
        HR = company.HR
        company_description = (f"<b>Назва: </b> {company.name}\n"
                               f"<b>Про компанію: </b> {company.description}\n"
                               f"<b>HR: </b> {HR.name} {HR.surname}, {HR.username}\n")
    return company_description
