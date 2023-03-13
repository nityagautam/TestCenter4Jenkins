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
from app.server.dbase.db_crud import generate_sample_data_to_db
from app.server import users


# ==========================================================================
# This '/home' route is to set a default page to open after login;
# Right now it is set to open '/dashboard', but we can set whatever we want
# ==========================================================================
@application.route('/home', methods=['GET'])
def home():
    if 'user' in session and session['user'] in users.keys():
        return redirect('/dashboard')
    return not_authorised()


@application.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user' in session and session['user'] in users.keys():
        return render_template(app_ui_config["routes"]["/dashboard"]["template_name"],
                               pagename=app_ui_config["routes"]["/dashboard"]["page_name"],
                               username=session['user'],
                               ui_config=app_ui_config,
                               data=sample_data.latest_data
                               )
    return not_authorised()


@application.route('/index')
def index():
    if 'user' in session and session['user'] in users.keys():
        return render_template(app_ui_config["routes"]["/index"]["template_name"],
                               pagename=app_ui_config["routes"]["/index"]["page_name"],
                               username=session['user'],
                               ui_config=app_ui_config,
                               data=sample_data.project_list_data)
    return not_authorised()


@application.route('/trends', methods=['GET'])
def trends():
    if 'user' in session and session['user'] in users.keys():
        return render_template(app_ui_config["routes"]["/trends"]["template_name"],
                               pagename=app_ui_config["routes"]["/trends"]["page_name"],
                               username=session['user'],
                               ui_config=app_ui_config,
                               data=sample_data.latest_data)
    return not_authorised()


@application.route('/settings', methods=['GET'])
def settings():
    if 'user' in session and session['user'] in users.keys():
        return render_template(app_ui_config["routes"]["/settings"]["template_name"],
                               pagename=app_ui_config["routes"]["/settings"]["page_name"],
                               username=session['user'],
                               ui_config=app_ui_config,
                               data=sample_data.latest_data)
    return not_authorised()


@application.route('/create-new-space')
def create_new_project_space():
    if 'user' in session and session['user'] in users.keys():
        return render_template(app_ui_config["routes"]["/create-new-space"]["template_name"],
                               pagename=app_ui_config["routes"]["/create-new-space"]["page_name"],
                               username=session['user'],
                               ui_config=app_ui_config)
    return not_authorised()


@application.route('/about', methods=['GET'])
def about():
    if 'user' in session and session['user'] in users.keys():
        return render_template("about.html", ui_config=app_ui_config, data=sample_data.latest_data)
    return not_authorised()


@application.route('/notes')
def info():
    if 'user' in session and session['user'] in users.keys():
        return render_template(app_ui_config["routes"]["/notes"]["template_name"],
                               pagename=app_ui_config["routes"]["/notes"]["page_name"],
                               username=session['user'],
                               ui_config=app_ui_config)
    return not_authorised()


# ===============================
# When User is not authorised,
# then where to redirect
# ===============================
def not_authorised():
    return redirect('/login')
