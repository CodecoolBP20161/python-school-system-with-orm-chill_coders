from flask import Flask, request, flash, redirect, url_for, render_template
from models import *
from checker import Check

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


@app.route('/')
def index():
    return redirect("https://media.giphy.com/media/10Shl99Vghh5aU/giphy.gif")


@app.route('/registration', methods=['GET', 'POST'])
def reg_confirmation():
    """Displays and edits registration form"""
    cities = City.select()
    if request.method == "POST":
        b = (request.form['first_name'], request.form['last_name'], request.form['e_mail'], request.form['location'])
        a = Check.checker(b[0], b[1], b[2])
        if a[:] == [True, True, True]:  # GOOD FORM, CREATES NEW FORM
            Applicant.create(first_name=request.form['first_name'],
                             last_name=request.form['last_name'],
                             location=request.form['location'],
                             email=request.form['e_mail'])
            return redirect('/')
        else:  # ERROR IN CHECKER, RETURNS REG.FORM TEMPLATE WITH ERRORS
            return render_template('registration_form.html', cities=cities, error=True, valid=a, words=b)
    else:  # GET
        return render_template('registration_form.html', cities=cities, error=False)

if __name__ == '__main__':
    app.run()
