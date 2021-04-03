from telebot import TeleBot
import mongoengine as me
from datetime import datetime

class Data:

    def __init__(self, conn_string: str, bot: TeleBot):
        self.bot = bot
        
        me.connect(host=conn_string)
        print("connection success ")

    # HZ CHI TREBA
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


class CV(me.Document):
    cv_file = me.FileField(required=True)
    last_update_date = me.DateTimeField(required=True)
    add_date = me.DateTimeField(required=True)


class User(me.Document):
    chat_id = me.IntField(required=True, unique=True) #
    name = me.StringField(required=True)
    surname = me.StringField(required=True)
    username = me.StringField(required=True)
    interests = me.ListField(default=list()) #
    experience = me.StringField(default="") #
    employment = me.StringField(default="") #
    cv = me.ReferenceField(CV, default=None)
    apply_counter = me.IntField(default=20) #
    registration_date = me.DateTimeField(required=True) #
    last_update_date = me.DateTimeField(required=True)
    last_interaction_date = me.DateTimeField(required=True)
    hr_status = me.BooleanField(default=False)


class Company(me.Document):
    name = me.StringField(required=True, unique=True)
    photo_id = me.StringField(required=True)
    description = me.StringField(required=True)
    vacancy_counter = me.IntField(default=20)                 ##############?
    HR = me.ReferenceField(User, required=False)
    token = me.StringField(required=True)
    registration_date = me.DateTimeField(required=True)
    #vacancy_list = me.ListField(me.EmbeddedDocumentField, Vacancy, required=False)


class Vacancy(me.Document):
    company = me.ReferenceField(Company, required=True)
    name = me.StringField(required=True)           
    tag = me.StringField(required=True)
    salary = me.StringField(required=True)
    experience = me.StringField(required=True)
    employment_type = me.StringField(required=True)
    description = me.StringField(required=True)
    add_date = me.DateTimeField(required=True)
    last_update_date = me.DateTimeField(required=True)
    active_days_left = me.IntField(default=14)
    is_active = me.BooleanField(default=False)


class Question(me.EmbeddedDocument):                        ########### Not ready yet
    question_text = me.StringField(required=True)
    answers_list = me.ListField(me.StringField)


class Quiz(me.Document):                                    ########### Not ready yet
    name = me.StringField(required=True)
    questions = me.ListField(me.EmbeddedDocumentField(Question))


class VacancyPreviewLog(me.Document):
    """
    Class for logging user viewing of vacancy.
    """
    vacancy = me.ReferenceField(Vacancy, required=True)
    user = me.ReferenceField(User, required=True)
    log_datetime = me.DateTimeField(required=True)


class VacancyApplyLog(me.Document):
    """
    Class for logging any applying for a job.
    """
    vacancy = me.ReferenceField(Vacancy, required=True)
    user = me.ReferenceField(User, required=True)
    cv = me.ReferenceField(CV, required=True)
    log_datetime = me.DateTimeField(required=True)


class VacancyPromotionLog(me.Document):
    """
    Class for logging every promotion.
    """
    vacancy = me.ReferenceField(Vacancy, required=True)
    auditory_tag = me.StringField(required=True)
    log_datetime = me.DateField(required=True)

#from datetime import datetime
#
#if __name__ == '__main__':
#    #table1 = User().save()  # insert new user in table
#
#    me.connect(host="mongodb+srv://HYaroslav:4486@ejfcluster.jdquq.mongodb.net/ejf_vacancy_bot?retryWrites=true&w=majority")
#
#    now = datetime.now()
#
#    user = User()
#    user.chat_id = 12312
#    user.name = "Yaroslav"
#    user.surname = "Horodyskyi"
#    user.username = "@Yaroslav_Horodyskyi"
#    user.registration_date = now
#    user.last_update_date = now
#    user.last_interaction_date = now
#    try:
#        user.save()
#    except:
#        pass
#
#    company = Company()
#    company.name = "SoftServe"
#    company.photo_id = "afadfasdf"
#    company.description = "hahaaahahha"
#    company.token = "afafe13f23f3"
#    company.registration_date = now
#    try:
#        company.save()
#    except:
#        pass
#
#    vacancy = Vacancy()
#    vacancy.company = Company.objects.filter(name="SoftServe")[0]
#    vacancy.name = "Strong Middle Python developer"
#    vacancy.tag = "python"
#    vacancy.salary = "1000-2000$"
#    vacancy.experience = "10 років"
#    vacancy.employment_type = "Full Time"
#    vacancy.description = """Requirements:
#
#4+ years of experience in Python development;Experience in Django, Postgre, SQL,;Build REST API for Database CRUD Operations;Understanding Python deployment flow (django, wsgi, nginx, heroku etc.);Experience with Linux, bash scripting;Experience with CI/CD pipelines and devops practices for Python developments;Ability unit/integration tests.Experience with Swagger and Git Hub
#
#Duties:
#
#Development of projects from scratch
#Development of project modules.
#Writing an API.
#Supporting of ready projects
#Terms:
#
#Basic communication in Telegram (you need to be in touch with some of our distant workers).
#Working in a team of programmers.
#Using Trello task manager
#Git Hub
#Additional info:
#
#Please be ready to do testing task before the interview"""
#    vacancy.add_date = now
#    vacancy.last_update_date = now
#    #vacancy.save()
#    try:
#        pass
#        #vacancy.save()
#    except:
#        pass
#
#    #cv = CV()
#    #cv.cv_file = open("cv.pdf", "rb")
#    #cv.add_date = now
#    #cv.last_update_date = now
#    #cv.save()
##
#    #user = User.objects.with_id("605fae402abdd4962ae12c20")
##
#    #user.cv = cv
#    #user.save()
#
#
#    log = VacancyApplyLog()
#    log.vacancy = Vacancy.objects.with_id("605fbd8a7e6e123aa296f234")
#    log.user = User.objects.with_id("605fae402abdd4962ae12c20")
#    log.cv = CV.objects.with_id("605fbee7d2484091d578464f")
#    log.log_datetime = now
#    log.save()
#
#
#
#
#
#
#    #for u in User.objects:
#    #    print(len(str(u.id)))
#
#
#    #vac1 = Vacancy()
#    #vac2 = Vacancy()
#    #vacancies = [vac1, vac2]
#    #table2 = Company(name='Salam', photo_id='1', description='fff', vacancy_counter='5', HR_chat_id='1',
#    #                 token='urhfhsf1', registration_date='2012-02-02', vacancy_list=vacancies).save()
#    #table4 = VacancyPreviewLog().save()
#    #table5 = VacancyApplyLog().save()
#    #table6 = VacancyPromotionLog().save()
#