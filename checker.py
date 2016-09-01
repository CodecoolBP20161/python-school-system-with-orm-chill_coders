class Check:

    @staticmethod
    def namecheck(name):
        check = name.isalpha()
        if name[0].islower():
            check = False
        return check

    @staticmethod
    def emailcheck(e_mail):
        email = e_mail.split('@')
        return (len(email) == 2 and
                '.' in email[1] and
                '' not in email[1].split('.') and
                len(email[0]) > 0 and
                ' ' not in e_mail)

    @classmethod
    def checker(cls, first_name, last_name, email):
        checklist = []
        checklist.append(cls.namecheck(first_name))
        checklist.append(cls.namecheck(last_name))
        checklist.append(cls.emailcheck(email))
        return checklist
