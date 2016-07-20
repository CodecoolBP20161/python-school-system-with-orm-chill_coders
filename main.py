from models import *
import random
# Write here your console application

app_code_list = [applicant.app_code for applicant in Applicant.select()]

def app_code_generate(appcodelist):
    chars = 'ABCDEFGHIJKLMNOPQRSTVWXYZ123456789'
    done = False
    while not done:
        code = ''
        for i in range(0, 6):
            code += chars[random.randrange(0, len(chars))]
        done = True
        if code in appcodelist:
            done = False
    appcodelist.append(code)
    return code

def add_app_code():

    for applicant in Applicant.select():
        if applicant.app_code is None:
            applicant.app_code = app_code_generate(app_code_list)
            applicant.save()
            print(applicant.first_name + " " + applicant.last_name + " received a new application code: " + applicant.app_code)

add_app_code()