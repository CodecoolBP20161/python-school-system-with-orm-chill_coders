from flask import Flask, request, flash, redirect, url_for, render_template, session, escape
from models import *
from checker import Check
import os

app = Flask(__name__)


# This hook ensures that a connection is opened to handle any queries
# generated by the request.
@app.before_request
def _db_connect():
    db.connect()


# This hook ensures that the connection is closed when we've finished
# processing the request.
@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()


# Homepage
@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'


# Sign up --- registration form
@app.route('/registration', methods=['GET', 'POST'])
def reg_confirmation():
    """Displays and edits registration form"""

    if request.method == "POST":
        incoming_data = (request.form['first_name'],
                         request.form['last_name'],
                         request.form['e_mail'],
                         request.form['location'])

        list_of_booleans = Check.checker(incoming_data[0], incoming_data[1], incoming_data[2])

        # GOOD FORM, CREATES NEW FORM
        if list_of_booleans[:] == [True, True, True]:
            Applicant.create(first_name=request.form['first_name'],
                             last_name=request.form['last_name'],
                             location=request.form['location'],
                             email=request.form['e_mail'])

            # SENDING E_MAILS TO NEWBIES
            Applicant.add_app_code()
            flash('You\'ve just got your application code! Please, check out your mailbox to log in.')
            return redirect('/')

        # ERROR IN CHECKER, RETURNS REG.FORM TEMPLATE WITH ERRORS
        else:
            return render_template('registration_form.html',
                                   cities=City.select(),
                                   error=True,
                                   valid=list_of_booleans,
                                   words=incoming_data)
    # GET
    else:
        return render_template('registration_form.html',
                               cities=City.select(),
                               error=False)


# Login
@app.route('/applicant/login', methods=['GET', 'POST'])
def login():
    """Handles applicants' login page"""

    if request.method == 'POST':

        # Log in without any problem --- session logged-in
        if Applicant.get().where(email=request.form['email'].lstrip(),
                                 app_code=request.form['app_code'].lstrip().uppercase()):
            session['user'] = request.form['app_code']
            flash('Successfully logged in!')
            return redirect('/', error=False)

        # if log in fails
        else:
            # mistype in e-mail address
            if Check.email_check(request.form['email'].lstrip()) is False:
                flash('Not a valid e-mail address.')
            # cannot find data in database
            else:
                flash('Invalid e-mail address and application code pair. Please try again!')
            return redirect('/applicant/login', error=True)

    # Displays login page with blank boxes
    else:
        return render_template('login.html')

@app.route('/applicant/logout', methods=['POST'])
def logout():
    """Handles logout"""

    # remove the user from the session if it's there
    session.pop('user', None)
    return redirect('/')


if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run()
