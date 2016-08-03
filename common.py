from models import *
from prettytable import PrettyTable


class Common(object):
    """ Includes common methods which refer to several different tables. """
    @staticmethod
    def display_pretty_table(table):
        if table == 'applicant':
            headline = PrettyTable(['ID', 'First name', 'Last name', 'Application code', 'LocationID', 'Status'])
            for row in Applicant.select():
                headline.add_row([row.id,
                                  row.first_name,
                                  row.last_name,
                                  row.app_code,
                                  row.location_id,
                                  row.status])
            print(headline)
        if table == 'interviewslot':
            headline = PrettyTable(['ID', 'Date', 'Start', 'End', 'Reserved', 'Related MentorID', 'Related Applicant'])
            for row in InterviewSlot.select():
                headline.add_row([row.id,
                                  row.date,
                                  row.start,
                                  row.end,
                                  row.reserved,
                                  row.related_mentor_id,
                                  row.related_applicant])
            print(headline)
