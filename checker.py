class Check(object):
    """Checks valid incoming data from web"""

    @staticmethod
    def name_check(name):
        return len(name) > 0 and name.isalpha() and not name[0].islower()

    @staticmethod
    def email_check(e_mail):
        email = e_mail.split('@')
        return (len(email) == 2 and
                '.' in email[1] and
                '' not in email[1].split('.') and
                len(email[0]) > 0 and
                ' ' not in e_mail)

    @classmethod
    def checker(cls, first_name, last_name, email):
        checklist = []
        checklist.append(cls.name_check(first_name))
        checklist.append(cls.name_check(last_name))
        checklist.append(cls.email_check(email))
        return checklist
