"""
  @author Ashutosh Mishra (@github: nityagautam)

  Software Engineer & Explorer
  nityanarayan44@gmail.com

  Created on 14 February, 2023 @ 10:25 AM.
"""
# import app.server
from app.server import app as application
from flask import redirect, render_template, session
from app.server.routes.authentication import not_authorised, route_gateway
from app.server.config.ui_configurations import UIConfigurations
from app.server.dbase import sample_data


# ==========================================================================
# This '/home' route is to set a default page to open after login;
# Right now it is set to open '/dashboard', but we can set whatever we want
# ==========================================================================
@application.route('/home', methods=['GET'])
def home():
    if route_gateway.is_session_active():
        return redirect('/index')
    return not_authorised()


@application.route('/dashboard', methods=['GET'])
def dashboard():
    if route_gateway.is_session_active():
        return route_gateway.get_template("/dashboard")
    return not_authorised()


@application.route('/index')
def index():
    if route_gateway.is_session_active():
        return route_gateway.get_template("/index")
    return not_authorised()


@application.route('/history', methods=['GET'])
def trends():
    if route_gateway.is_session_active():
        return route_gateway.get_template("/history")
    return not_authorised()


@application.route('/settings', methods=['GET'])
def settings():
    if route_gateway.is_session_active():
        return route_gateway.get_template("/settings")
    return not_authorised()


@application.route('/create-project-space')
def create_new_project_space():
    if route_gateway.is_session_active():
        return route_gateway.get_template("/create-project-space")
    return not_authorised()


@application.route('/about', methods=['GET'])
def about():
    if route_gateway.is_session_active():
        return route_gateway.get_template("/about")
    return not_authorised()


@application.route('/utility', methods=['GET'])
def utility():
    if route_gateway.is_session_active():
        return route_gateway.get_template("/utility")
    return not_authorised()


@application.route('/notes')
def info():
    if route_gateway.is_session_active():
        return route_gateway.get_template("/notes")
    return not_authorised()
