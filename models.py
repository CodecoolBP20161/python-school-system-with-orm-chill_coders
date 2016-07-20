from peewee import *

# Configure your database connection here
# database name = should be your username on your laptop
# database user = should be your username on your laptop
db = PostgresqlDatabase('TW_ORM_week6', user='dorasztanko')



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

class Applicant(Person):
    """Creates an applicant."""
    app_code = CharField(null=True, default=None)
    location = CharField()
    status = CharField(default='new')
    i_slot = IntegerField(null=True, default=None)

class InterviewSlot(BaseModel):
    """Creates interview intervals for applicants."""
    date = DateField()
    start = TimeField()
    end = TimeField()
    reserved = BooleanField(default=False)
    related_mentor = ForeignKeyField(Mentor)


