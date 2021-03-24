import telebot
import mongoengine as me
from datetime import datetime

#me.connect()

class Data:

    def __init__(self, conn_string):
        me.connect(host=conn_string)
        print("connection success ")

    def add_user(self, chat_id, name, surname, username, interests=[], experience="", 
                 employment="", apply_counter=0, registration_date=None, last_update_date=None, 
                 last_interaction_date=None, hr_status=False):

        registration_date = datetime.now()
        last_interaction_date = registration_date
        last_update_date = registration_date

        User(chat_id=chat_id, name=name, surname=surname, username=username,
             interests=interests, experience=experience, employment=employment,
             apply_counter=apply_counter, registration_date=registration_date,
             last_update_date=last_update_date, last_interaction_date=last_interaction_date,
             hr_status=hr_status).save()


class User(me.Document):
    chat_id = me.IntField(required=True) #
    name = me.StringField(required=True)
    surname = me.StringField(required=True)
    username = me.StringField(required=True)
    interests = me.ListField(required=False) #
    experience = me.StringField(required=True) #
    employment = me.StringField(required=True) #
    # CV = me.StringField(required=True)
    apply_counter = me.IntField(required=True) #
    registration_date = me.DateField(required=True) #
    last_update_date = me.DateField(required=True)
    last_interaction_date = me.DateField(required=True)
    hr_status = me.BooleanField(required=True)

class Vacancy(me.EmbeddedDocument):
    name = me.StringField(required=True)
    tag = me.StringField(required=True)
    experience = me.StringField(required=True)
    employment_type = me.StringField(required=True)
    description = me.StringField(required=True)
    post_date = me.StringField(required=True)
    last_update_date = me.DateField(required=True)
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
    vacancy_id = me.ReferenceField(Vacancy, required=True)
    user_id = me.StringField(required=True)
    log_datetime = me.DateField(required=True)

class VacancyApplyLog(me.Document):
    """
    Class for logging any applying for a job.
    """
    vacancy_id = me.ReferenceField(Vacancy, required=True)
    user_id = me.StringField(required=True)
    cv = me.StringField(required=True)
    log_datetime = me.DateField(required=True)

class VacancyPromotionLog(me.Document):
    """
    Class for logging every promotion.
    """
    vacancy_id = me.ReferenceField(Vacancy, required=True)
    auditory_tag = me.StringField(required=True)
    log_datetime = me.DateField(required=True)


if __name__ == '__main__':
    #table1 = User().save()  # insert new user in table

    vac1 = Vacancy()
    vac2 = Vacancy()
    vacancies = [vac1, vac2]
    table2 = Company(name='Salam', photo_id='1', description='fff', vacancy_counter='5', HR_chat_id='1',
                     token='urhfhsf1', registration_date='2012-02-02', vacancy_list=vacancies).save()
    #table4 = VacancyPreviewLog().save()
    #table5 = VacancyApplyLog().save()
    #table6 = VacancyPromotionLog().save()
