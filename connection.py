import getpass
import json
import os.path



# configuration settings
class Connection(object):
    """Reads in data for personal connections."""

    def __init__(self):
        self.file_path = 'config.json'

        if os.path.isfile(self.file_path):
            with open(self.file_path, "r") as data_file:
                data = json.load(data_file)

                self.database_user = data["database_user"]
                self.database_name = data["database_name"]
                self.email_address = data["email_address"]
                self.email_password = data["email_password"]

        else:
            try:
                print(False)
                self.database_user = input('Please, add your user name to config.json: ')
                self.database_name = input('Database name: ')
                self.email_address = input('Email address: ')
                self.email_password = getpass.getpass('Email password: ')
                with open(self.file_path, 'w') as data_file:
                    data = {"database_user": self.database_user,
                            "database_name": self.database_name,
                            "email_address": self.email_address,
                            "email_password": self.email_password}
                    json.dump(data, data_file)
            except UnicodeDecodeError:
                print('Invalid inserted letter type. Please, try again!')
                exit()

