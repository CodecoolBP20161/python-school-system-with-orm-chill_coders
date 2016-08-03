from models import *
from collections import OrderedDict

class Menu():

    @staticmethod
    def administrator_menu_loop():
        '''Administrator menu.'''
        print("---ADMINISTRATOR MENU---")
        administrator_menu = OrderedDict([
            ('1', Applicant.display_applicants)
        ])
        choice = None
        while choice != 'q':
            print("Press 'q' to exit menu")
            for key, value in administrator_menu.items():
                print("{}) {}".format(key, value.__doc__))
            choice = input("Choice: ").lower().strip()

            if choice in administrator_menu:
                administrator_menu[choice]()

    @staticmethod
    def applicant_menu_loop():
        '''Applicant menu.'''
        print("---APPLICANT MENU---")
        Applicant.check_valid_code()
        applicant_menu = OrderedDict([
            ('1', Applicant.display_student_status),
            ('2', Applicant.display_school_name),
            ('3', Applicant.show_interview_details)
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
            ('1', cls.applicant_menu_loop),
            ('2', cls.administrator_menu_loop)
        ])
        choice = None
        while choice != 'q':
            print("Press 'q' to exit menu")
            for key, value in menu.items():
                print("{}) {}".format(key, value.__doc__))
            choice = input("Choice: ").lower().strip()

            if choice in menu:
                menu[choice]()
