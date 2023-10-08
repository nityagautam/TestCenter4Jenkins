"""
  @author Ashutosh Mishra (amishra)(@github: nityagautam)

  Software Engineer & Explorer
  nityanarayan44@gmail.com

  Created on 14 February, 2023 @ 10:25 AM.
"""
# import app.server
from app.server import app as application
from flask import redirect, jsonify, request, json, flash
from app.server.config.crawler_configurations import CrawlerConfig
from app.server.dbase.DBAccess import DBAccess
from app.server.routes.authentication import not_authorised, gateway


# ==========================================================================
# This '/home' route is to set a default page to open after login;
# Right now it is set to open '/dashboard', but we can set whatever we want
# ==========================================================================
@application.route('/home', methods=['GET'])
def home():
    if gateway.is_session_active():
        return redirect('/index')
    return not_authorised()


@application.route('/dashboard', methods=['GET'])
def dashboard():
    if gateway.is_session_active():
        return gateway.get_template("/dashboard")
    return not_authorised()


@application.route('/index')
def index():
    if gateway.is_session_active():
        return gateway.get_template("/index")
    return not_authorised()


@application.route('/history', methods=['GET'])
def trends():
    if gateway.is_session_active():
        return gateway.get_template("/history")
    return not_authorised()


@application.route('/settings', methods=['GET'])
def settings():
    if gateway.is_session_active():
        flash(json.dumps({"crawler_status": CrawlerConfig.crawler_status}))
        return gateway.get_template("/settings")
    return not_authorised()


@application.route('/utility', methods=['GET'])
def utility():
    if gateway.is_session_active():
        return gateway.get_template("/utility")
    return not_authorised()


@application.route('/notes')
def info():
    if gateway.is_session_active():
        return gateway.get_template("/notes")
    return not_authorised()


@application.route('/about', methods=['GET'])
def about():
    if gateway.is_session_active():
        return gateway.get_template("/about")
    return not_authorised()


# ====================================================
# APIs
# ====================================================
@application.route('/create-project-space', methods=['GET', 'POST'])
def create_new_project_space():
    if gateway.is_session_active():
        # Verify if we received a form
        if request.method == 'POST':
            print(f"\n Collecting the data for new project: {request.form}")
            data = None
            if len(request.form.keys()) == 7:
                data = {}
                for key, value in request.form.items():
                    data[key] = value.strip()
                    print(f"Key: {key}, Value: {value}")

                # share the info to dbaccess class
                write_status = DBAccess().add_project(data)

                if write_status is True:
                    # return success message
                    flash(f"Project '{data['project_name']}' created successfully.")
                else:
                    # return a message saying we already have this name
                    flash(f"Well, Seems like we already have this Project '{data['project_name']}' in the DB. "
                          f"If this project is not visible in the dashboard or history then consider checking its status")
                return redirect('/create-project-space')

            else:
                flash(f"Please fill all the '*' fields")
                return redirect('/create-project-space')

        else:
            return gateway.get_template("/create-project-space")
    return not_authorised()
