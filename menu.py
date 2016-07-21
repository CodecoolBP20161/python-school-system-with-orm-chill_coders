from models import *
from collections import OrderedDict

class Menu():

    @staticmethod
    def administrator_menu_loop():
        '''Administrator menu.'''
        admin_menu = OrderedDict([
            ('1', Mentor.show_closest_school)
        ])
        choice = None
        while choice != 'q':
            print("Press 'q' to exit menu")
            for key, value in admin_menu.items():
                print("{}) {}".format(key, value.__doc__))
            choice = input("Choice: ").lower().strip()

            if choice in admin_menu:
                admin_menu[choice]()

    @staticmethod
    def applicant_menu_loop():
        '''Applicant menu.'''
        Applicant.check_valid_code()
        applicant_menu = OrderedDict([
            ('1', Applicant.display_student_status),
        ])
        choice = None
        while choice != 'q':
            print("Press 'q' to exit menu")
            for key, value in applicant_menu.items():
                print("{}) {}".format(key, value.__doc__))
            choice = input("Choice: ").lower().strip()

            if choice in applicant_menu:
                applicant_menu[choice]()

    @classmethod
    def menu_loop(cls):
        '''Displays menu.'''
        menu = OrderedDict([
            ('1', cls.administrator_menu_loop),
            ('2', cls.applicant_menu_loop)
        ])
        choice = None
        while choice != 'q':
            print("Press 'q' to exit menu")
            for key, value in menu.items():
                print("{}) {}".format(key, value.__doc__))
            choice = input("Choice: ").lower().strip()

            if choice in menu:
                menu[choice]()
