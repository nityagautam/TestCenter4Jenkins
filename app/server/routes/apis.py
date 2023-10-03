"""
  @author Ashutosh Mishra (@github: nityagautam)

  Software Engineer & Explorer
  nityanarayan44@gmail.com

  Created on 14 February, 2023 @ 10:25 AM.
"""

from app.server import app as application
from flask import jsonify, render_template, url_for, request, redirect, session
from app.server.config.configurations import Configurations
from app.server.routes.authentication import route_gateway, not_authorised
from app.server.dbase.sample_data import latest_data, history_data, project_list_data


@application.route(f'{Configurations.APP_API_BASE_ROUTE}/get-dashboard-data', methods=['GET'])
def get_dashboard_data():
    # TODO: Need to implement API_KEY for auth
    if route_gateway.is_session_active():
        return jsonify(latest_data)
    return not_authorised()


@application.route(f'{Configurations.APP_API_BASE_ROUTE}/get-project-list', methods=['GET'])
def get_project_data():
    # TODO: Need to implement API_KEY for auth
    if route_gateway.is_session_active():
        return jsonify(project_list_data)
    return not_authorised()


@application.route(f'{Configurations.APP_API_BASE_ROUTE}/get-history-data', methods=['GET'])
def get_history_data():
    # TODO: Need to implement API_KEY for auth
    if route_gateway.is_session_active():
        return jsonify(history_data)
    return not_authorised()


@application.route(f'{Configurations.APP_API_BASE_ROUTE}/get-dummy-data', methods=['GET'])
def get_dummy_data():
    # TODO: Need to implement API_KEY for auth
    if route_gateway.is_session_active():
        return jsonify(history_data)
    return not_authorised()


@application.route(f'{Configurations.APP_API_BASE_ROUTE}/logo')
def get_logo():
    """
    Queries the snapshot data for both Serenity and JMeter projects from the MongoDB.
    Renders the Snapshot view of html
    :return: N/A
    """
    # set template directory of the Flask App to the  path set by the user as command line arg.
    return f'<html><head><title>Root</title><head><body><hr/> Welcome to the main page <hr/> ' \
           f'Building image from static public location: <br/> ' \
           f'<img src=\'{url_for("static", filename="images/logo.svg")}\' /> </body></html>'


