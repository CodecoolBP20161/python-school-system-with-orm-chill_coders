# New applicants arrive into your project database by this script.
# You can run it anytime to generate new data!

from models import *

Applicant.create(first_name='András', last_name='Dóra', location=1)