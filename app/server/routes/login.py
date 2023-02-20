"""
  @author Ashutosh Mishra (@github: nityagautam)
  Software Engineer & Explorer
  nityanarayan44@gmail.com

  Created on 14 February, 2023 @ 10:25 AM.
"""

from app.server import app as application
from flask import flash, redirect, render_template, request, session
from app.settings import users


@application.route('/', methods=['POST', 'GET'])
def root():
    if not session.get('logged_in'):
        print('>>> User is not authorised: ', session.get('logged_in'))
        return render_template("login.html", data="Any message on the login page")
    else:
        print('>>> User is authorised, let in')
        return redirect('/home')


@application.route('/login', methods=['POST', 'GET'])
def login():
    # Check requests for the form login
    print(">>> In the login section ...")
    if request.method == 'POST':
        print(">>> In the form section ...")
        if request.form['password'] == users['password'] and request.form['username'] == users['username']:
            print(f'Accepted the user: {request.form["username"]}')
            session['logged_in'] = True
            session['user'] = request.form['username']
            return redirect('/home')
        else:
            print(f'Incorrect creds for user: {request.form["username"]}')
            flash('Oopse, incorrect credential!')
            return redirect('/login')
    else:
        # User's session is valid, let him in to home page
        return root()


@application.route("/logout")
def logout():
    session['logged_in'] = False
    session.pop('user', None)
    return root()
    # return "Logged out"
