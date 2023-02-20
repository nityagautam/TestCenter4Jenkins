"""
  @author Ashutosh Mishra (@github: nityagautam)

  Software Engineer & Explorer
  nityanarayan44@gmail.com

  Created on 14 February, 2023 @ 10:25 AM.
"""

from app.server import app as application
from flask import redirect, render_template, session
from app.server.config.uiconfig import app_ui_config
from app.server.dbase import sample_data
from app.settings import users


@application.route('/home', methods=['GET'])
def home():
    if 'user' in session and session['user'] == users['username']:
        return redirect('/dashboard')
    return not_authorised()


@application.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user' in session and session['user'] == users['username']:
        return render_template("dashboard.html", app_data=app_ui_config, data=sample_data.latest_data, username=session['user'])
    return not_authorised()


@application.route('/about', methods=['GET'])
def about():
    if 'user' in session and session['user'] == users['username']:
        return render_template("about.html", app_data=app_ui_config, data=sample_data.latest_data)
    return not_authorised()


@application.route('/notes')
def info():
    if 'user' in session and session['user'] == users['username']:
        return render_template("notes.html", app_data=app_ui_config)
    return not_authorised()


@application.route('/index')
def index():
    if 'user' in session and session['user'] == users['username']:
        return render_template("index.html", username=session['user'], app_data=app_ui_config)
    return not_authorised()

# When User is not authorised, then where to redirect
def not_authorised():
    return redirect('/login')
