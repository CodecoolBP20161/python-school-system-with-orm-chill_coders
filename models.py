from peewee import *
import random

# Configure your database connection here
# database name = should be your username on your laptop
# database user = should be your username on your laptop
db = PostgresqlDatabase('sltw6', user='turbek')


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


class Mentor(Person):
    """Creates a Mentor."""
    school = ForeignKeyField(School)

    @staticmethod
    def show_closest_school():
        """Show specific (app_code) or all the applicants and their interview locations."""

        argv = input("Add an application code: ").upper().strip()

        if len(argv) == 6:
            try:
                spec_applicant = Applicant.get(Applicant.app_code == argv)
                print('According to the given application code, {0} {1}\'s interview location is: {2} '.format(
                    spec_applicant.first_name,
                    spec_applicant.last_name,
                    spec_applicant.location.loc_school)
                )
            except:
                print('Application code is not found.')
        elif len(argv) == 0:
            for applicant in Applicant.select():
                print('{0} {1}\'s interview location is: {2} '.format(applicant.first_name,
                                                                      applicant.last_name,
                                                                      applicant.location.loc_school)
                      )
        else:
            print('Invalid application code.')


class Applicant(Person):
    """Creates an applicant."""
    app_code = CharField(null=True, default=None)
    location = ForeignKeyField(City)
    status = CharField(default='new')
    i_slot = IntegerField(null=True, default=None)

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
        """Prints status belongs to the specific applicant."""
        spec_applicant = cls.get(cls.app_code == cls.application_code)
        print('According to the given application code, your status is: {2} '.format(
            spec_applicant.first_name,
            spec_applicant.last_name,
            spec_applicant.status)
        )

    @classmethod
    def display_school_name(cls):
        """Shows the name of school belongs to the specific applicant."""
        obj = (School.select()
               .join(City, on=School.location == City.loc_school)
               .join(Applicant)
               .where(cls.app_code == cls.application_code)
               .get())
        print("School that you'll be visiting: {}, {}".format(obj.location, obj.name))

    @classmethod
    def reserve_interview(cls):
        """Reserve an interview slot for new applicants"""
        applicants_without_islot = []
        for applicant in cls.select():
            found = False
            if applicant.i_slot is None:
                possible_mentors = Mentor.select().join(School).where(School.location == applicant.location.loc_school)
                for iview in InterviewSlot.select():
                    if (not iview.reserved) and (Mentor.get(Mentor.id == iview.related_mentor) in possible_mentors):
                        applicant.i_slot = iview.id
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
                applicants_without_islot.append(applicant)
        if len(applicants_without_islot) > 0:
            print("The following applicants could not get an interview due to the lack of slots:")
            for applicant in applicants_without_islot:
                print(applicant.first_name + " " + applicant.last_name + " " + applicant.app_code)


class InterviewSlot(BaseModel):
    """Creates interview intervals for applicants."""
    date = DateField()
    start = TimeField()
    end = TimeField()
    reserved = BooleanField(default=False)
    related_mentor = ForeignKeyField(Mentor)
    related_applicant = CharField(null=True, default=None)
