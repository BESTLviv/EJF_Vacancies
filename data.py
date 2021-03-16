import telebot
import mongoengine as me

me.connect()


class User(me.Document):
    chat_id = me.IntField(required=True) #
    name = me.StringField(required=True)
    surname = me.StringField(required=True)
    username = me.StringField(required=True)
    interests = me.ListField(required=True) #
    experience = me.StringField(required=True) #
    employment = me.StringField(required=True) #
    # CV = me.StringField(required=True)
    apply_counter = me.IntField(required=True) #
    registration_date = me.DateField(required=True) #
    last_update_date = me.DateField(required=True)
    last_interaction_date = me.DateField(required=True)
    hr_status = me.StringField(required=True)


class Vacancy(me.EmbeddedDocument):
    name = me.StringField(required=True)
    tag = me.StringField(required=True)
    experience = me.StringField(required=True)
    employment_type = me.StringField(required=True)
    description = me.StringField(required=True)
    post_date = me.StringField(required=True)
    last_update_date = me.StringField(required=True)
    active_days_left = me.StringField(required=True)
    status = me.StringField(required=True)


class Company(me.Document):
    name = me.StringField(required=True)
    photo_id = me.StringField(required=True)
    description = me.StringField(required=True)
    vacancy_counter = me.IntField(required=True)
    HR_chat_id = me.StringField(required=True)
    token = me.StringField(required=True)
    registration_date = me.DateField(required=True)
    vacancy_list = me.ListField(me.EmbeddedDocumentField, Vacancy, required=True)


class VacancyPreviewLog(me.Document):
    """
    Class for logging user viewing of vacancy.
    """
    vacancy_id = me.StringField(required=True)
    time = me.StringField(required=True)
    user_id = me.StringField(required=True)


class VacancyApplyLog(me.Document):
    """
    Class for logging any applying for a job.
    """
    vacancy_id = me.StringField(required=True)
    user_id = me.StringField(required=True)
    cv = me.StringField(required=True)
    time = me.StringField(required=True)


class VacancyPromotionLog(me.Document):
    """
    Class for logging every logging.
    """
    time = me.StringField(required=True)
    vacancy_id = me.StringField(required=True)
    auditory_tag = me.StringField(required=True)


if __name__ == '__main__':
    table1 = User().save()  # insert new user in table

    vac1 = Vacancy()
    vac2 = Vacancy()
    vacancies = [vac1, vac2]
    table2 = Company(name='Salam', photo_id='1', description='fff', vacancy_counter='5', HR_chat_id='1',
                     token='urhfhsf1', registration_date='2012-02-02', vacancy_list=vacancies).save()
    table4 = VacancyPreviewLog().save()
    table5 = VacancyApplyLog().save()
    table6 = VacancyPromotionLog().save()
