from peewee import *
import random
from dbconnection import DbConnection

user_data = DbConnection.open_file('db_config.txt')
db = PostgresqlDatabase(user_data[0].strip('\n'), user=user_data[1])


class BaseModel(Model):
    """A base model that will use our Postgresql database"""
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

    # for creating unique e-mail aliases
    DIFF_NUM = 1


    @classmethod
    def email_generator(cls):
        # email_address = 'joe.tester4321@gmail.com'

        for person in cls.select():
            if person.email is not None:
                pass
            else:
                person.email = 'joe.tester4321+' + str(cls.DIFF_NUM) + '@gmail.com'
                person.save()
                cls.DIFF_NUM += 1


class Mentor(Person):
    """Creates a Mentor."""
    school = ForeignKeyField(School)


class Applicant(Person):
    """Creates an applicant."""
    app_code = CharField(unique=True, null=True)
    location = ForeignKeyField(City)
    status = CharField(default='new')

    application_code = None

    @classmethod
    def check_valid_code(cls):
        application_code = input("Please enter your application code: ").upper().strip()

        if application_code in cls.app_code_list():
            print("Valid application code.")
            cls.application_code = application_code
        else:
            print('Invalid application code.')
            exit()

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
        """Reserves an interview slot for new applicants"""
        applicants_without_interview = []
        for applicant in cls.select():
            found = False
            if applicant.status == 'new':
                possible_mentors = Mentor.select().join(School).where(School.location == applicant.location.loc_school)
                for iview in InterviewSlot.select():
                    if (not iview.reserved) and (Mentor.get(Mentor.id == iview.related_mentor) in possible_mentors):
                        applicant.status = "In progress"
                        applicant.save()
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


class InterviewSlot(BaseModel):
    """Creates interview intervals for applicants."""
    date = DateField()
    start = TimeField()
    end = TimeField()
    reserved = BooleanField(default=False)
    related_mentor = ForeignKeyField(Mentor)
    related_applicant = CharField(null=True, default=None)
