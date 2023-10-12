"""
    @author:
      Ashutosh Mishra (@github: nityagautam)
      Software Engineer & Explorer
      nityanarayan44@gmail.com

    Created: 11 Jan, 2022
    reviewer:
    last modified: 12 Oct 2023
    desc: Authentication route;
"""

from app.server import app as application
from flask import flash, redirect, render_template, request, session
from app.server.config.ui_configurations import UIConfigurations
from app.server.routes import Gateway

# Create an object for gateway;
# And entire app will use this object by importing
# It deals with Authentications, Session, UserDB
gateway = Gateway()


@application.route('/', methods=['POST', 'GET'])
def root():
    if not session.get('logged_in'):
        print('>>> User is not authorised: ', session.get('logged_in'))
        return render_template("login.html",
                               ui_config={"APP_META": UIConfigurations.APP_META,
                                          "ROUTES": UIConfigurations.ROUTES},
                               data="Any message on the login page")
    else:
        print('>>> User is authorised, let in')
        return redirect('/home')


@application.route('/login', methods=['POST', 'GET'])
def login():
    # Check requests for the form login
    if request.method == 'POST':
        print(
            f">>> Login request came with [User : '{request.form['username']}', Password: '{request.form['username']}']")
        if gateway.is_valid_user(request.form["username"], request.form['password']):
            print(f'>>> Login Accepted for user: {request.form["username"]}')
            session['logged_in'] = True
            # Since, session is a cookie stored in the client computer so multi user can login
            session['user'] = request.form['username']
            return redirect('/home')
        else:
            print(f'>>> Login rejected for user: {request.form["username"]}')
            # Send a message to the next redirect page, and we can recieve it by calling get_flashed_messages()
            flash(UIConfigurations.ERROR_MESSAGES['INCORRECT_CREDENTIALS'])
            return redirect('/login')
    else:
        # User's session is valid, let him in to home page
        return root()


@application.route("/logout", methods=['POST', 'GET'])
def logout():
    gateway.logout_from_session(request.args.get('username'))
    flash(UIConfigurations.ERROR_MESSAGES['USER_LOGGED_OUT'])
    return root()
    # return "Logged out"


# ===============================
# When User is not authorised,
# then where to redirect
# ===============================
def not_authorised():
    flash(UIConfigurations.ERROR_MESSAGES['NOT_AUTHORISED'])
    return redirect('/login')
