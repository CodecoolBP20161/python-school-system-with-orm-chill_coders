from models import *
import random
from collections import OrderedDict

# Write here your console application

app_code_list = [applicant.app_code for applicant in Applicant.select()]


def app_code_generate(appcodelist):
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
    app_code_list.append(code)
    return code


def add_app_code():
    """Adds previously generated application codes if it is necessary."""
    for applicant in Applicant.select():
        if applicant.app_code is None:
            applicant.app_code = app_code_generate(app_code_list)
            applicant.save()
            print(applicant.first_name + " " + applicant.last_name + " received a new application code: "
                  + applicant.app_code)



def show_closest_school(*argv):
    """Show specific (app_code) or all the applicants and their interview locations."""
    if len(argv) >= 1:
        try:
            spec_applicant = Applicant.get(Applicant.app_code == argv)
            print('According to the given application code, {0} {1}\'s interview location is: {2} '.format(
                spec_applicant.first_name,
                spec_applicant.last_name,
                spec_applicant.location.loc_school)
            )
        except:
            print('Application code is not found.')
    else:
        for applicant in Applicant.select():
            print('{0} {1}\'s interview location is: {2} '.format(applicant.first_name,
                                                              applicant.last_name,
                                                              applicant.location.loc_school)
              )

def menu():
    '''displays menu'''
    menu = OrderedDict([
        ('1', show_closest_school),
        ('2', add_app_code)
    ])
    choice = None
    while choice != 'q':
        print("Press 'q' to exit menu")
        for key, value in menu.items():
            print("{}) {}".format(key, value.__doc__))
        choice = input("Choice: ").lower().strip()

        if choice in menu:
            menu[choice]()


add_app_code()
menu()

