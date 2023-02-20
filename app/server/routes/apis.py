"""
  @author Ashutosh Mishra (@github: nityagautam)

  Software Engineer & Explorer
  nityanarayan44@gmail.com

  Created on 14 February, 2023 @ 10:25 AM.
"""

from app.server import app as application
from flask import jsonify, render_template, url_for, request, redirect
from app.server.config.uiconfig import app_ui_config


# Route For Sample data
@application.route('/data')
def get_data():
    data = {
        "reports": [
            {
                "build": "build_no",
                "created": "Imported 05052021T11:30:00:00IST",
                "platform": "Imported Win/Unix/Mac",
                "project_name": "project_name_1",
                "report_location_path": "path/to/report/location/index.html",
                "report_summary": {"pass": "50", "fail": "0", "ignored": "0", "skipped": "0"},
                "total_time": "35 min."
            },
            {
                "build": "build_no",
                "created": "Imported 05052021T11:30:00:00IST",
                "platform": "Imported Win/Unix/Mac",
                "project_name": "project_name_2",
                "report_location_path": "path/to/report/location/index.html",
                "report_summary": {"pass": "10", "fail": "2", "ignored": "0", "skipped": "0"},
                "total_time": "0.2345 secs."
            },
            {
                "build": "build_no",
                "created": "Imported 05052021T11:30:00:00IST",
                "platform": "Imported Win/Unix/Mac",
                "project_name": "project_name_3",
                "report_location_path": "path/to/report/location/index.html",
                "report_summary": {"pass": "100", "fail": "5", "ignored": "0", "skipped": "0"},
                "total_time": "5 days"
            }
        ]
    }
    return jsonify(data)


# ==============================================================
# Extra routes starts
# ==============================================================
@application.route('/sample1')
def sample1():
    return render_template("web-analytics-overview.html")


@application.route('/sample2')
def sample2():
    return render_template("web-analytics-real-time.html")


@application.route('/logo')
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


