from peewee import *
import random
from dbconnection import DbConnection
from prettytable import PrettyTable
from emailsender import *

user_data = DbConnection.open_file('db_config.txt')
db = PostgresqlDatabase(user_data[0].strip('\n'), user=user_data[1])


class BaseModel(Model):
    """A base model that will use our Postgresql database."""
    class Meta:
        database = db


class School(BaseModel):
    """Represents a newly generated class."""
    name = CharField(unique=True)
    location = CharField(unique=True)


class City(BaseModel):
    """Matches cities with possible interview locations."""
    loc_examples = CharField(unique=True)
    loc_school = CharField()


class Person(BaseModel):
    """Creates a person."""
    first_name = CharField()
    last_name = CharField()
    email = CharField(null=True, default=None)

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    # for creating unique e-mail aliases
    DIFF_NUM = 1

    @classmethod
    def email_generator(cls):
        """Generates random e-mail addresses for default applicants."""
        # email_address = 'testerzh1234@gmail.com'

        for person in cls.select():
            if person.email is not None:
                pass
            else:
                person.email = 'testerzh1234+' + str(cls.DIFF_NUM) + '@gmail.com'
                person.save()
                cls.DIFF_NUM += 1


class Mentor(Person):
    """Creates a Mentor."""
    school = ForeignKeyField(School)

    mentor_name = None
    mentor = None

    @classmethod
    def check_valid_mentor(cls):
        print("Press 'q' to exit!")
        mentor_name = input("Enter name: ")
        av_mentors = {}
        i = 0
        for name in cls.mentor_name_list():
            if mentor_name.lower() in name.lower():
                i += 1
                av_mentors[i] = name

        if mentor_name == 'q':
            quit()

        if len(av_mentors) > 1:
            print("There are more available results")
            for key, value in av_mentors.items():
                print("{}) {}".format(key, value))
            a = input("Choice: ")
            if a == 'q':
                exit()
            cls.mentor_name = av_mentors[int(a)]

        elif len(av_mentors) == 1:
            cls.mentor_name = av_mentors[i]

        namesplit = cls.mentor_name.split(" ")
        cls.mentor = cls.get(cls.first_name == namesplit[0])
        print("Hi, " + namesplit[0] + "!")

    @staticmethod
    def mentor_name_list():
        mentor_name_list = [mentor.first_name + " " + mentor.last_name for mentor in Mentor.select()]
        return mentor_name_list

    @classmethod
    def display_mentor_interviews(cls):
        """Display interviews."""
        try:
            Mentor.display_pretty_table_mentor_interview()

            a = None
            while a != 'q':
                print("Press 'q' to exit menu.\nFilter by:")
                print("1) Date    2) Start    3) End   4) Application code   5) Name")
                a = input("Choice:")
                if a == '1':
                    try:
                        b = input("yyyy-mm-dd: ")
                        Mentor.display_pretty_table_mentor_interview(InterviewSlot.date == b)
                    except (DataError, InternalError):
                        print('Invalid input.')
                elif a == '2':
                    try:
                        b = input("hh:mm: ")
                        Mentor.display_pretty_table_mentor_interview(InterviewSlot.start == b)
                    except (DataError, InternalError):
                        print('Invalid input.')
                elif a == '3':
                    try:
                        b = input("hh:mm: ")
                        Mentor.display_pretty_table_mentor_interview(InterviewSlot.end == b)
                    except (DataError, InternalError):
                        print("Invalid input.")
                elif a == '4':
                    try:
                        b = input("Application code: ")
                        Mentor.display_pretty_table_mentor_interview(InterviewSlot.related_applicant.contains(b))
                    except (DataError, InternalError):
                        print("Invalid input.")
                elif a == '5':
                    try:
                        b = input("Name: ")
                        Mentor.display_pretty_table_mentor_interview(Applicant.first_name.contains(b) |
                                                                     Applicant.last_name.contains(b))
                    except (DataError, InternalError):
                        print("Invalid input.")
        except Applicant.DoesNotExist:
            print("No scheduled interview.")

    @classmethod
    def display_pretty_table_mentor_interview(cls, filters=None):
        """displays interview table"""
        headline = PrettyTable(['Date',
                                'Start',
                                'End',
                                'Application code',
                                'Applicant'
                                ])

        if filters is None:
            basic = InterviewSlot.select(InterviewSlot.date,
                                         InterviewSlot.start,
                                         InterviewSlot.end,
                                         InterviewSlot.related_applicant,
                                         Applicant.first_name.concat(" ").concat(Applicant.last_name))\
                .join(Applicant, on=InterviewSlot.related_applicant == Applicant.app_code)\
                .where(InterviewSlot.related_mentor == cls.mentor.id, InterviewSlot.related_applicant != None)\
                .tuples()

        if filters is not None:
            basic = InterviewSlot.select(InterviewSlot.date,
                                         InterviewSlot.start,
                                         InterviewSlot.end,
                                         InterviewSlot.related_applicant,
                                         Applicant.first_name.concat(" ").concat(Applicant.last_name)) \
                .join(Applicant, on=InterviewSlot.related_applicant == Applicant.app_code) \
                .where(InterviewSlot.related_mentor == cls.mentor.id, InterviewSlot.related_applicant != None, filters)\
                .tuples()

        for row in basic:
            headline.add_row(row)
        print(headline)


class Applicant(Person):
    """Creates an applicant."""
    app_code = CharField(unique=True, null=True)
    location = ForeignKeyField(City)
    status = CharField(default='new')

    application_code = None

    @classmethod
    def check_valid_code(cls):
        print("Press 'q' to exit")
        application_code = input("Please enter your application code: ").upper().strip()

        if application_code == 'Q':
            exit()

        elif application_code in cls.app_code_list():
            cls.application_code = application_code
            applicant = Applicant.select().where(cls.app_code == cls.application_code).get()
            print("Hi, " + applicant.first_name + "!")
        else:
            print('Invalid application code.')
            cls.check_valid_code()

    @staticmethod
    def app_code_list():
        app_code_list = [applicant.app_code for applicant in Applicant.select()]
        return app_code_list

    @classmethod
    def app_code_generate(cls, appcodelist):
        """Randomly generates unique application codes."""
        chars = 'ABCDEFGHIJKLMNOPQRSTVWXYZ123456789'
        done = False
        while not done:
            code = ''
            for i in range(0, 6):
                code += chars[random.randrange(0, len(chars))]
            done = True
            if code in appcodelist:
                done = False
        cls.app_code_list().append(code)
        return code

    @classmethod
    def add_app_code(cls):
        """Adds previously generated application codes if it is necessary."""
        for applicant in cls.select():
            if applicant.app_code is None:
                applicant.app_code = cls.app_code_generate(cls.app_code_list())
                applicant.save()
                print("{} {} received a new application code: {}".format(applicant.first_name,
                                                                         applicant.last_name,
                                                                         applicant.app_code))
                message = """
Dear {0}!

We gladly received your application. First of all, we have generated a personal application code for you. Here it is:
{1}.

If everything goes fine with your application process, you're going to be informed about your interview's details soon.
One thing for sure, it is probably going to be held in {2}.

We're looking forward to meeting with you!

Yours sincerely,
CC Staff
""".format(applicant.full_name, applicant.app_code, applicant.location.loc_school)
                emailsender = EmailSender(email_receiver=applicant.email, text=message)
                emailsender.sending()
            else:
                pass


    @classmethod
    def display_student_status(cls):
        """Displays the status of the given applicant."""
        spec_applicant = cls.get(cls.app_code == cls.application_code)
        print('According to the given application code, your status is: {2} '.format(
            spec_applicant.first_name,
            spec_applicant.last_name,
            spec_applicant.status)
        )

    @classmethod
    def display_school_name(cls):
        """Displays the name of the school of the certain applicant."""
        obj = (School.select()
               .join(City, on=School.location == City.loc_school)
               .join(Applicant)
               .where(cls.app_code == cls.application_code)
               .get())
        print("School that you'll be visiting: {}, {}".format(obj.location, obj.name))

    @classmethod
    def reserve_interview(cls):
        """Reserves an interview slot for new applicants."""
        applicants_without_interview = []
        for applicant in cls.select():
            found = False
            if applicant.status == 'new':
                possible_mentors = Mentor.select().join(School).where(School.location == applicant.location.loc_school)
                for iview in InterviewSlot.select():
                    if (not iview.reserved) and (Mentor.get(Mentor.id == iview.related_mentor) in possible_mentors):
                        applicant.status = "In progress"
                        applicant.save()

                        message = """
                        Dear {0}!

                        The next step in your Codecool application process is just on your doorstep!
                        We have scheduled an interview slot for your.

                        Details:

                        Location: {1}
                        Related mentor's name: {2}
                        Date: {3}
                        Time/start: {4}
                        Time/end: {5}

                        We're really looking forward to meeting with you!

                        Yours sincerely,
                        CC Staff
                        """.format(applicant.full_name,
                                   applicant.location.loc_school,
                                   'kiscica',
                                   "2",
                                   "3",
                                   "4")
                        emailsender = EmailSender(email_receiver=applicant.email, text=message)
                        emailsender.sending()

                        iview.reserved = True
                        iview.related_applicant = applicant.app_code
                        iview.save()
                        found = True
                        break
            else:
                found = True
            if not found:
                applicants_without_interview.append(applicant)
        if len(applicants_without_interview) > 0:
            print("The following applicants could not get an interview due to the lack of slots:")
            for applicant in applicants_without_interview:
                print(applicant.first_name + " " + applicant.last_name + " " + applicant.app_code)

    @classmethod
    def show_interview_details(cls):
        """Displays specific interview information."""
        spec_applicant = cls.get(cls.app_code == cls.application_code)
        obj_interview = (InterviewSlot.select()
                                      .join(Applicant, on=InterviewSlot.related_applicant == Applicant.app_code)
                                      .where(InterviewSlot.related_applicant == spec_applicant.app_code)
                                      .get())
        obj_school = (School.select()
                            .join(City, on=School.location == City.loc_school)
                            .join(Applicant)
                            .where(cls.app_code == cls.application_code)
                            .get())
        obj_mentor = Mentor.get(Mentor.id == obj_interview.related_mentor)
        print('Date: {}, {}-{}\nSchool: {}\nMentor: {} {}'.format(obj_interview.date,
                                                                  obj_interview.start,
                                                                  obj_interview.end,
                                                                  obj_school.name,
                                                                  obj_mentor.first_name,
                                                                  obj_mentor.last_name))

    @staticmethod
    def display_applicants():
        """Display applicants."""
        Applicant.display_pretty_table_applicants()
        a = None
        while a != 'q':
            print("Press 'q' to exit menu.\nFilter by:")
            print("1) Status    2) Time    3) Location   4) Full name   5) Email   6) School   7) Mentor")
            a = input("Choice:")
            if a == '1':
                b = input("1) new\n2) In progress\n3) rejected\nChoice: ")
                try:
                    if b == '1':
                        c = "new"
                    elif b == '2':
                        c = "In progress"
                    elif b == '3':
                        c = "rejected"
                    Applicant.display_pretty_table_applicants(Applicant.status == c)
                except (DataError, InternalError):
                    print("Invalid input.")
            elif a == '2':
                try:
                    b = input("yyyy-mm-dd: ")
                    Applicant.display_pretty_table_applicants(InterviewSlot.date == b)
                except (DataError, InternalError):
                    print('Invalid input.')
            elif a == '3':
                b = input("1) Budapest   2) Miskolc   3) Krakow\nChoice: ")
                try:
                    if b == '1':
                        c = "Budapest"
                    elif b == '2':
                        c = "Miskolc"
                    elif b == '3':
                        c = "Krakow"
                    Applicant.display_pretty_table_applicants(School.location == c)
                except (DataError, InternalError):
                    print("Invalid input.")
            elif a == '4':
                b = input("Full name: ")
                Applicant.display_pretty_table_applicants(Applicant.first_name.contains(b) |
                                                          Applicant.last_name.contains(b))
            elif a == '5':
                b = input("Enter email: ")
                Applicant.display_pretty_table_applicants(Applicant.email.contains(b))
            elif a == '6':
                b = input("1) CC_BP   2) CC_M   3) CC_K\nChoice:")
                try:
                    if b == '1':
                        c = "CC_BP"
                    elif b == '2':
                        c = "CC_M"
                    elif b == '3':
                        c = "CC_K"
                    Applicant.display_pretty_table_applicants(School.name == c)
                except (DataError, InternalError):
                    print("Invalid input.")
            elif a == '7':
                b = input("Mentor's name:")
                Applicant.display_pretty_table_applicants(Mentor.first_name.contains(b) |
                                                          Mentor.last_name.contains(b))
            else:
                print("Invalid input.")

    @staticmethod
    def display_pretty_table_applicants(filters=None):
        headline = PrettyTable(['Status', 'Time', 'Location', 'First name', 'Last name', 'Email', 'School'])

        basic = Applicant.select(Applicant.status, InterviewSlot.date, School.location, Applicant.first_name,
                                 Applicant.last_name, Applicant.email, School.name)\
            .join(InterviewSlot, JOIN.LEFT_OUTER, on=InterviewSlot.related_applicant == Applicant.app_code)\
            .join(Mentor, JOIN.LEFT_OUTER, on=InterviewSlot.related_mentor == Mentor.id)\
            .join(School, JOIN.LEFT_OUTER)\
            .where(filters)\
            .tuples()
        for row in basic:
            headline.add_row(row)
        print(headline)


class InterviewSlot(BaseModel):
    """Creates interview intervals for applicants."""
    date = DateField()
    start = TimeField()
    end = TimeField()
    reserved = BooleanField(default=False)
    related_mentor = ForeignKeyField(Mentor)
    related_applicant = CharField(null=True, default=None)

    @staticmethod
    def display_interviews():
        """Display interviews."""
        InterviewSlot.display_pretty_table_interview()
        a = None
        while a != 'q':
            print("Press 'q' to exit menu.\nFilter by:")
            print("1) School    2) Application code    3) Mentor   4) Date")
            a = input("Choice:")
            if a == '1':
                b = input("1) CC_BP\n2) CC_M\n3) CC_K\nChoice: ")
                try:
                    if b == '1':
                        c = "CC_BP"
                    elif b == '2':
                        c = "CC_M"
                    elif b == '3':
                        c = "CC_K"
                    else:
                        print("No option: {}".format(b))
                        break
                    InterviewSlot.display_pretty_table_interview(School.name == c)
                except (DataError, InternalError):
                    print("Invalid input.")
            elif a == '2':
                b = input("Application code: ")
                InterviewSlot.display_pretty_table_interview(InterviewSlot.related_applicant.contains(b))
            elif a == '3':
                b = input("Mentor: ")
                InterviewSlot.display_pretty_table_interview(Mentor.first_name.contains(b) |
                                                             Mentor.last_name.contains(b))
            elif a == '4':
                try:
                    b = input("yyyy-mm-dd: ")
                    InterviewSlot.display_pretty_table_interview(InterviewSlot.date == b)
                except (DataError, InternalError):
                    print('Invalid input.')
            else:
                print("Invalid input.")

    @staticmethod
    def display_pretty_table_interview(filters=None):
        """displays interview table"""
        headline = PrettyTable(['School', 'Application code', 'Mentor', 'Date'])

        if filters is None:
            basic = InterviewSlot.select(School.name,
                                         InterviewSlot.related_applicant,
                                         Mentor.first_name.concat(" ").concat(Mentor.last_name),
                                         InterviewSlot.date).join(Mentor).join(School)\
                                        .where(InterviewSlot.related_applicant != None).tuples()
        elif filters is not None:
            basic = InterviewSlot.select(School.name,
                                         InterviewSlot.related_applicant,
                                         Mentor.first_name.concat(" ").concat(Mentor.last_name),
                                         InterviewSlot.date).join(Mentor).join(School)\
                                        .where(InterviewSlot.related_applicant != None, filters).tuples()
        for row in basic:
            headline.add_row(row)
        print(headline)