from telebot import TeleBot
import mongoengine as me
from datetime import datetime

import string
import random
from datetime import datetime


class Data:

    TEST_PHOTO = "https://i.ibb.co/0Gv4JyW/photo-2021-04-16-12-48-15.jpg"

    TEMP_ADMIN_PASSWORD = "admin"
    JOB_FAIR_END_TIME = datetime(2021, 5, 20, 20, 0, 0)

    def __init__(self, conn_string: str, bot: TeleBot):
        self.bot = bot

        me.connect(host=conn_string)
        print("connection success ")

        self.reinit_ejf_table()
        print("ejf and content tables have been reinitialized")

        # remove later
        self.add_start_quiz()

        # for user in User.objects:
        #    user.additional_info = None
        #    user.save()

    def add_test_company_with_vacancies(self, vacancies_number=2):

        # company
        name = self._generate_string()
        photo_id = self.TEST_PHOTO
        description = self._generate_string(long=True)
        vacancy_counter = 20  # ?
        HR = None
        token = self._generate_string()
        registration_date = datetime.now()

        test_company = Company(
            name=name,
            photo_id=photo_id,
            description=description,
            vacancy_counter=vacancy_counter,
            HR=HR,
            token=token,
            registration_date=registration_date,
        )
        test_company.save()

        # vacancies
        for i in range(vacancies_number):
            company = test_company
            name = self._generate_string()
            tag = self._generate_string()
            salary = f"{random.randint(1000, 5000)}$"
            experience = self._generate_string()
            employment_type = self._generate_string()
            description = self._generate_string(long=True)
            add_date = datetime.now()
            last_update_date = datetime.now()
            active_days_left = 14
            is_active = True

            Vacancy(
                company=company,
                name=name,
                tag=tag,
                salary=salary,
                experience=experience,
                employment_type=employment_type,
                description=description,
                add_date=add_date,
                last_update_date=last_update_date,
                active_days_left=active_days_left,
                is_active=is_active,
            ).save()

    def add_start_quiz(self):
        # delete collections
        Quiz.objects.delete()

        quiz = Quiz(name="StartQuiz", is_required=True)

        q_name_surname = Question(
            name="name_surname",
            message="Як мені до тебе звертатися?",
            correct_answer_message="Гарно звучить 🥰",
            wrong_answer_message="Введи ім’я текстом 🤡",
        )

        q_age = Question(
            name="age",
            message="Скільки тобі років?",
            regex="[1-9][0-9]",
            correct_answer_message="Ого, ми однолітки 🥰",
            wrong_answer_message="Вкажи свій справжній вік 🤡",
        )

        q_school = Question(
            name="school",
            message="Де вчишся? Вибери або введи.",
            buttons=[
                "НУЛП",
                "ЛНУ",
                "УКУ",
                "КПІ",
                "КНУ",
                "Ще в школі",
                "Вже закінчив(-ла)",
            ],
            correct_answer_message="Клас 🥰",
            wrong_answer_message="Введи назву текстом 🤡",
        )

        q_study_term = Question(
            name="study_term",
            message="Який ти курс?",
            buttons=[
                "Перший",
                "Другий",
                "Третій",
                "Четвертий",
                "На магістартурі",
                "Нічого з переліченого",
            ],
            allow_user_input=False,
            correct_answer_message="Ідеальний час, щоб будувати кар'єру 🥰",
            wrong_answer_message="Вибери, будь ласка, один з варіантів 🤡",
        )

        ##############
        q_city = Question(
            name="city",
            message="Звідки ти? Вибери зі списку або введи назву.",
            buttons=["Львів", "Київ", "Новояворівськ", "Донецьк", "Стамбул"],
            correct_answer_message="Був-був там!",
            wrong_answer_message="Введи назву текстом :)",
        )

        q_contact = Question(
            name="contact",
            message="Обміняємося контактами?",
            buttons=["Тримай!"],
            input_type="contact",
            correct_answer_message="Дякую. А я залишаю тобі контакт головного організатора: @Slavkoooo 🥰",
            wrong_answer_message="Надішли, будь ласка, свій контакт 🤡",
        )

        q_email = Question(
            name="email",
            message="Наостанок, вкажи адресу своєї поштової скриньки.",
            regex="^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$",
            correct_answer_message="Дякую 🥰",
            wrong_answer_message="Введи, будь ласка, електронну адресу 🤡",
        )

        q_agree = Question(
            name="user_agreements",
            message="Залишилося тільки дати згоду на обробку даних.",
            buttons=["Я погоджуюсь."],
            allow_user_input=False,
        )

        q_register_end = Question(
            name="end_register",
            message="Хух, усі формальності позаду!\n\nЯ зареєстрував тебе на ІЯК. Далі нас очікують два дні пригод.\n\n<b>Поонлайнимо?</b> 🤓",
            buttons=[
                "Прийду подивитися 👀",
                "Прийду шукати роботу 🤑",
                "Прийду дізнатися щось нове 🧐",
                "Візьму участь у воркшопах✍️",
                "Все разом 🤹",
            ],
            allow_user_input=False,
        )

        quiz.questions = [
            q_name_surname,
            q_age,
            q_school,
            q_study_term,
            # q_city,
            q_contact,
            q_email,
            q_agree,
            q_register_end,
        ]

        quiz.save()

    def reinit_ejf_table(self):
        # delete collections
        JobFair.objects.delete()
        Content.objects.delete()

        # create content table
        content = Content()
        content.start_text = (
            "Хей, друзі! Теж помітили, що останнім часом зникли запахи і їжа якось не так смакує? Усе ясно: життя без ІЯКу втратило смак… 😔\n\n"
            "Нам пощастило, що до 19 травня залишилося зовсім трохи. А що там 19 травня? Там повернення легендарного Інженерного ярмарку кар’єри — ІЯКу від BEST Lviv!"
            "Але мусимо зробити камінг-аут: у 2021 році ІЯК став віртуалом. 😳 Немає часу пояснювати. Ти, головне, реєструйся. Далі — більше."
        )

        content.user_start_text = """Хей, друзі! Теж помітили, що останнім часом зникли запахи і їжа якось не так смакує? Усе ясно: життя без ІЯКу втратило смак… 😔

Нам пощастило, що до 19 травня залишилося зовсім трохи. А що там 19 травня? Там повернення легендарного Інженерного ярмарку кар’єри — ІЯКу від BEST Lviv! Але мусимо зробити камінг-аут: у 2021 році ІЯК став віртуалом. 😳 Немає часу пояснювати. Ти, головне, реєструйся. Далі — більше.
"""
        content.user_start_photo = self.TEST_PHOTO
        content.ejf_start_text = "Я знаю, друже, що до 19 травня ще є трохи часу, тому приготував для тебе кілька корисних штук. Заходь у меню, читай, слідкуй за оновленнями. Почувай себе, як вдома. "
        content.ejf_start_photo = self.TEST_PHOTO
        content.save()

        # create ejf table
        ejf = JobFair()
        ejf.filters_interest = ["Full Stack", "Front End", "Data Science"]
        ejf.filters_experience = ["1 рік", "3+ років"]
        ejf.filters_employment = ["Full time", "Part time"]
        ejf.admin_password = self.TEMP_ADMIN_PASSWORD
        ejf.cv_archive_file_id_list = []
        ejf.cv_archive_last_update = None
        ejf.cv_archive_size = 0
        ejf.start_menu = [
            {
                "name": "ЩО❔",
                "text": """Інженерний ярмарок кар’єри — коротко ІЯК — це must-visit подія для кожного студента. Не лякайся слова “інженерний”, бо наш Ярмарок уже давно вийшов за будь-які рамки і навіть претендує називатися наймасштабнішим у Львові. У нас для цього є все:

🔸Топ-компанії, які зацікавлені в студентах. Чекни розділ “Компанії”.
🔸Класний контент, який за два дні допоможе тобі нарешті відповісти на питання, ким ти хочеш стати. Ознайомся з усіма видами інтерактиву в розділі “Розклад”.
🔸Можливість знайти роботу безпосередньо через бота, тобто через мене! Після 20 травня я оновлю меню і ти все зрозумієш :)
🔸Найкращі учасники. Угу, такі як ти!

Останні штрихи і ІЯК 2021 стає реальністю. Ще й не простою, а віртуальною. Зустрінемося на Hopin! Па!
""",
                "photo": self.TEST_PHOTO,
            },
            {
                "name": "ДЕ і ЯК❔",
                "text": """Пам’ятаєш, ще на початку я казав, що ІЯК став віртуалом. Так-от, я мав на увазі, що цього року у Львівській політехніці звичного квітневого свята, тобто нашого Ярмарку, не буде. Не буде довгих черг, великих скупчень і хаосу. Ми переїжджаємо в кращі санітарні умови — в онлайн простір. 👩‍💻

ІЯК відбудеться на платформі Hopin. Ти майже не відчуєш різниці між спілкуванням наживо і онлайн. На Hopin усе організовано так, як ми звикли: віртуальні стенди з компаніями, окрема кімната для презентацій та воркшопів. Є навіть сцена! Переходь за посиланням у запрошенні і побач усе на власні очі.
""",
                "photo": self.TEST_PHOTO,
            },
            {
                "name": "КОМПАНІЇ🎯",
                "text": "КомпаніїКомпаніїКомпанії",
                "photo": self.TEST_PHOTO,
            },
            {
                "name": "РОЗКЛАД 📌",
                "text": "РозкладРозкладРозклад",
                "photo": self.TEST_PHOTO,
            },
            {
                "name": "ЗВ’ЯЗОК З НАМИ ✍️",
                "text": "Головний організатор:\nЯрослав Когуч\n+380 50 621 96 74\nYaroslavkoguch1@gmail.com\n\nВідповідальні за корпоративні зв'язки:\nНазар Тутин\n+380 73 327 62 01\nNazar.tutyn@gmail.com\n\nАнна Погиба\n+380 97 044 55 28\nAnna.pohyba@gmail.com",
                "photo": self.TEST_PHOTO,
            },
        ]
        ejf.content = content
        ejf.start_datetime = datetime(2021, 5, 19, 10, 0, 0)
        ejf.end_datetime = self.JOB_FAIR_END_TIME
        ejf.save()

    def get_ejf(self):
        return JobFair.objects.first()

    def get_cv_count(self) -> int:
        return User.objects.filter(cv_file_id__ne=None).count()

    # HZ CHI TREBA
    def _add_test_user(
        self,
        chat_id,
        name,
        surname,
        username,
        interests=[],
        experience="",
        employment="",
        apply_counter=0,
        registration_date=None,
        last_update_date=None,
        last_interaction_date=None,
        hr_status=False,
    ):

        registration_date = datetime.now()
        last_interaction_date = registration_date
        last_update_date = registration_date

        User(
            chat_id=chat_id,
            name=name,
            surname=surname,
            username=username,
            interests=interests,
            experience=experience,
            employment=employment,
            apply_counter=apply_counter,
            registration_date=registration_date,
            last_update_date=last_update_date,
            last_interaction_date=last_interaction_date,
            hr_status=hr_status,
        ).save()

    def _generate_string(self, long=False):
        letters = string.ascii_letters
        if long is False:
            length = random.randint(10, 30)
        else:
            length = random.randint(300, 500)

        return "".join(random.choice(letters) for i in range(length))


class Content(me.Document):
    start_text = me.StringField()
    user_start_text = me.StringField()
    user_start_photo = me.StringField()
    ejf_start_text = me.StringField()
    ejf_start_photo = me.StringField()


class JobFair(me.Document):
    filters_interest = me.ListField(default=list())
    filters_experience = me.ListField(default=list())
    filters_employment = me.ListField(default=list())
    admin_password = me.StringField()
    cv_archive_file_id_list = me.ListField(default=None)
    cv_archive_last_update = me.DateTimeField(default=None)
    cv_archive_size = me.IntField(default=0)
    start_menu = me.ListField(default=list())
    content = me.ReferenceField(Content)
    start_datetime = me.DateTimeField()
    end_datetime = me.DateTimeField()


class User(me.Document):
    chat_id = me.IntField(required=True, unique=True)
    name = me.StringField(required=True)
    surname = me.StringField(required=True)
    username = me.StringField(required=True)
    interests = me.ListField(default=list())
    experience = me.StringField(default="")
    employment = me.StringField(default="")
    cv_file_id = me.StringField(default=None)
    cv_file_name = me.StringField(default=None)
    apply_counter = me.IntField(default=20)
    additional_info = me.DictField(default=None)
    registration_date = me.DateTimeField(required=True)
    last_update_date = me.DateTimeField(required=True)
    last_interaction_date = me.DateTimeField(required=True)
    hr_status = me.BooleanField(default=False)


class Company(me.Document):
    name = me.StringField(required=True, unique=True)
    photo_id = me.StringField(required=True)
    description = me.StringField(required=True)
    vacancy_counter = me.IntField(default=20)  # ?
    HR = me.ReferenceField(User, required=False)
    token = me.StringField(required=True)
    registration_date = me.DateTimeField(required=True)
    # vacancy_list = me.ListField(me.EmbeddedDocumentField, Vacancy, required=False)


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


class Question(me.EmbeddedDocument):
    name = me.StringField(required=True)
    message = me.StringField(required=True)
    # photo = me.StringField(default=None)
    buttons = me.ListField(default=list())
    input_type = me.StringField(choices=["text", "contact"], default="text")
    allow_user_input = me.BooleanField(default=True)
    regex = me.StringField(default=None)
    correct_answer_message = me.StringField(defaul=None)
    wrong_answer_message = me.StringField(default="Неправильний формат!")


class Answer(me.EmbeddedDocument):
    pass


class Quiz(me.Document):
    name = me.StringField(required=True)
    questions = me.ListField(me.EmbeddedDocumentField(Question), default=list())
    is_required = me.BooleanField(default=False)


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
    cv_file_id = me.IntField(required=True)
    log_datetime = me.DateTimeField(required=True)


class VacancyPromotionLog(me.Document):
    """
    Class for logging every promotion.
    """

    vacancy = me.ReferenceField(Vacancy, required=True)
    auditory_tag = me.StringField(required=True)
    log_datetime = me.DateField(required=True)


# from datetime import datetime
#
# if __name__ == '__main__':
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
# 4+ years of experience in Python development;Experience in Django, Postgre, SQL,;Build REST API for Database CRUD Operations;Understanding Python deployment flow (django, wsgi, nginx, heroku etc.);Experience with Linux, bash scripting;Experience with CI/CD pipelines and devops practices for Python developments;Ability unit/integration tests.Experience with Swagger and Git Hub
#
# Duties:
#
# Development of projects from scratch
# Development of project modules.
# Writing an API.
# Supporting of ready projects
# Terms:
#
# Basic communication in Telegram (you need to be in touch with some of our distant workers).
# Working in a team of programmers.
# Using Trello task manager
# Git Hub
# Additional info:
#
# Please be ready to do testing task before the interview"""
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
