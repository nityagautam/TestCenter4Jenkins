"""
  @author Ashutosh Mishra (@github: nityagautam)

  Software Engineer & Explorer
  nityanarayan44@gmail.com

  Created on 14 February, 2023 @ 10:25 AM.
"""
from threading import Thread
from app.server import app as application
from flask import jsonify, url_for, request, session
from app.server.config.configurations import Configurations
from app.server.config.crawler_configurations import CrawlerConfig
from crawler import Crawler
from app.server.dbase.DBAccess import DBAccess
from app.server.routes.authentication import gateway, not_authorised
from app.server.dbase.sample_data import latest_data, history_data, project_list_data


@application.route(f'{Configurations.APP_API_BASE_ROUTE}/run-jenkins-crawler', methods=['GET'])
def start_jenkins_crawler():
    # Run the crawler, on request as daemon service
    if gateway.is_session_active():
        if not CrawlerConfig.crawler_thread:
            thread = Thread(target=Crawler().run())
            thread.daemon = True

            # Set to the jenkins config to track
            CrawlerConfig.crawler_thread = thread
            CrawlerConfig.crawler_alive = thread.is_alive()

            # Start the thread
            thread.start()

            # Return the response
            return jsonify({"crawler_status": CrawlerConfig.crawler_status})
        else:
            return jsonify({"crawler_status": CrawlerConfig.crawler_status})
    return not_authorised()


@application.route(f'{Configurations.APP_API_BASE_ROUTE}/activate-project', methods=['GET'])
def activate_project():
    # Run the crawler, on request as daemon service
    if gateway.is_session_active():
        # Verify argument
        # print(f"\n ARGS ==> {request.args} \n")
        if 'project_name' in request.args:
            # activate project
            status = DBAccess().set_project_as_active(project_name=request.args['project_name'])
            if status:
                return jsonify({"project_name": "", "status": True, "msg": "Project activated"})
            else:
                return jsonify({"status": False, "msg": "Project does not exist even. consider creating it first."})

        else:
            return jsonify({"status": "'project_name' arg missing", "msg": " Incomplete request"})

    # otherwise
    return not_authorised()


@application.route(f'{Configurations.APP_API_BASE_ROUTE}/archive-project', methods=['GET'])
def archive_project():
    # Run the crawler, on request as daemon service
    if gateway.is_session_active():
        # Verify argument
        if 'project_name' in request.args:
            # archive project
            status = DBAccess().set_project_as_archived(project_name=request.args['project_name'])
            if status:
                return jsonify(
                    {"project_name": str(request.args['project_name']), "status": True, "msg": "Project archived."})
            else:
                return jsonify({"status": False, "msg": "Project does not exist even. consider creating it first."})

        else:
            return jsonify({"status": "'project_name' arg missing", "msg": " Incomplete request"})

    # otherwise
    return not_authorised()


@application.route(f'{Configurations.APP_API_BASE_ROUTE}/delete-project', methods=['GET'])
def delete_project():
    # Run the crawler, on request as daemon service
    if gateway.is_session_active():
        # Verify argument
        if 'project_name' in request.args:
            # delete project
            status = DBAccess().delete_project(project_name=request.args['project_name'])
            if status:
                return jsonify(
                    {"project_name": str(request.args['project_name']), "status": True, "msg": "Project deleted."})
            else:
                return jsonify({"status": False, "msg": "Project does not exist even. consider creating it first."})

        else:
            return jsonify({"status": "'project_name' arg missing", "msg": " Incomplete request"})

    # otherwise
    return not_authorised()


# ====================================================================
# DUMMY
# ====================================================================
@application.route(f'{Configurations.APP_API_BASE_ROUTE}/get-dashboard-data', methods=['GET'])
def get_dashboard_data():
    # TODO: Need to implement API_KEY for auth
    if gateway.is_session_active():
        return jsonify(latest_data)
    return not_authorised()


@application.route(f'{Configurations.APP_API_BASE_ROUTE}/get-project-list', methods=['GET'])
def get_project_data():
    # TODO: Need to implement API_KEY for auth
    if gateway.is_session_active():
        return jsonify(project_list_data)
    return not_authorised()


@application.route(f'{Configurations.APP_API_BASE_ROUTE}/get-history-data', methods=['GET'])
def get_history_data():
    # TODO: Need to implement API_KEY for auth
    if gateway.is_session_active():
        return jsonify(history_data)
    return not_authorised()


@application.route(f'{Configurations.APP_API_BASE_ROUTE}/get-dummy-data', methods=['GET'])
def get_dummy_data():
    # TODO: Need to implement API_KEY for auth
    if gateway.is_session_active():
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


