# This script can generate example data for "City" and "InterviewSlot" models.

from models import *


schools_data = [
    ['CC_BP', 'Budapest'],
    ['CC_M', 'Miskolc'],
    ['CC_K', 'Krakow']
]

mentors_data = [
    ['Attila', 'Molnár', 2],
    ['Pál', 'Monoczki', 2],
    [ 'Sándor', 'Szodoray', 2],
    [ 'Dániel', 'Salamon', 1],
    [ 'Miklós', 'Beöthy', 1],
    [ 'Tamás', 'Tompa', 1],
    [ 'Mateusz', 'Ostafil', 3]
]

applicants_data = [
    ['Dominique', 'Williams', 'Budapest'],
    ['Jemima', 'Foreman', 'Miskolc'],
    ['Zeph', 'Massey', 'Gödöllő'],
    ['Joseph', 'Crawford', 'Buenos Aires'],
    ['Ifeoma', 'Bird', 'Varsó'],
    ['Arsenio', 'Matthews', 'Zakopane'],
    ['Jemima', 'Cantu', 'Pécs'],
    ['Carol', 'Arnold', 'Budapest'],
    ['Jane', 'Forbes', 'Szeged'],
    ['Ursa', 'William', 'Siófok']
]


city_data = [
    ['Gödöllő', 'Budapest'],
    ['Buenos Aires', 'Budapest'],
    ['Varsó', 'Krakow'],
    ['Zakopane', 'Krakow'],
    ['Pécs', 'Budapest'],
    ['Szeged', 'Miskolc'],
    ['Siófok', 'Budapest']]

for data in schools_data:
    School.create(name=data[0], location=data[1])
for data in mentors_data:
    Mentor.create(first_name=data[0], last_name=data[1], school=data[2])
for data in applicants_data:
    Applicant.create(first_name=data[0], last_name=data[1], location=data[2])
for data in city_data:
    City.create(loc_examples=data[0], loc_school=data[1])
