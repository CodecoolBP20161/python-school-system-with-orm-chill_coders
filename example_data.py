# This script can generate example data for "City" and "InterviewSlot" models.

from models import *
import datetime
from random import randint


schools_data = [
    ['CC_BP', 'Budapest'],
    ['CC_M', 'Miskolc'],
    ['CC_K', 'Krakow']
]

mentors_data = [
    ['Attila', 'Molnár', 2],
    ['Pál', 'Monoczki', 2],
    ['Sándor', 'Szodoray', 2],
    ['Dániel', 'Salamon', 1],
    ['Miklós', 'Beöthy', 1],
    ['Tamás', 'Tompa', 1],
    ['Mateusz', 'Ostafil', 3]
]

applicants_data = [
    ['Dominique', 'Williams', 8],
    ['Jemima', 'Foreman', 9],
    ['Zeph', 'Massey', 1],
    ['Joseph', 'Crawford', 2],
    ['Ifeoma', 'Bird', 3],
    ['Arsenio', 'Matthews', 4],
    ['Jemima', 'Cantu', 5],
    ['Carol', 'Arnold', 8],
    ['Jane', 'Forbes', 6],
    ['Ursa', 'William', 7]
]


city_data = [
    ['Gödöllő', 'Budapest'],
    ['Buenos Aires', 'Budapest'],
    ['Varsó', 'Krakow'],
    ['Zakopane', 'Krakow'],
    ['Pécs', 'Budapest'],
    ['Szeged', 'Miskolc'],
    ['Siófok', 'Budapest'],
    ['Budapest', 'Budapest'],
    ['Miskolc', 'Miskolc'],
    ['Krakow', 'Krakow']
]


# for data in schools_data:
#     School.create(name=data[0], location=data[1])
for data in city_data:
    City.create(loc_examples=data[0], loc_school=data[1])
for data in mentors_data:
    Mentor.create(first_name=data[0], last_name=data[1], school=data[2])
for data in applicants_data:
    Applicant.create(first_name=data[0], last_name=data[1], location=data[2])
# change the datetime.date according how many days you want, i made 4
a = 7
for i in range(0, 14):
    a += 1
    b = randint(1, 7)
    InterviewSlot.create(date=datetime.date(2016, 8, 1), start=datetime.time(a, 0), end=datetime.time(a+1), related_mentor=b)
