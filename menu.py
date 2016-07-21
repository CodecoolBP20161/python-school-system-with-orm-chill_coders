from models import *
from collections import OrderedDict

class Menu():

    @staticmethod
    def menu_loop():
        '''Displays menu.'''
        menu = OrderedDict([
            ('1', Applicant.show_closest_school)
            ('2', Applicant.display_student_status)
        ])
        choice = None
        while choice != 'q':
            print("Press 'q' to exit menu")
            for key, value in menu.items():
                print("{}) {}".format(key, value.__doc__))
            choice = input("Choice: ").lower().strip()

            if choice in menu:
                menu[choice]()
