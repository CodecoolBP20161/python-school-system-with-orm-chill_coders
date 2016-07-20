from models import *
import random
# Write here your console application


def app_code_generate(applicants):
    chars = 'ABCDEFGHIJKLMNOPQRSTVWXYZ123456789'
    done = False
    while not done:
        code = ''
        for i in range(0, 6):
            code += chars[random.randrange(0, len(chars))]
        done = True
        for applicant in applicants:
            if code == applicant.app_code:
                done = False
    return code
