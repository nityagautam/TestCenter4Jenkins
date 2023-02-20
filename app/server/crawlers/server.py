from flask import Flask
from flask import jsonify
from flask import render_template
from flask import url_for
from flask import request
from flask import redirect
import os
import json
import argparse
import jinja2
import sample_data

# ==============================================================
# Flask configuration
# ==============================================================
public_folder_path = "/ReportDashboard/static/"
public_folder_name = "static"
app = Flask(__name__, static_url_path=public_folder_path, static_folder=public_folder_name)


# ==============================================================
# App Routes/Gateways
# ==============================================================
@app.route('/')
@app.route('/home')
def root():
    return render_template("dashboard.html", app_data=sample_data.app_data, data=sample_data.latest_data)


@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html", app_data=sample_data.app_data, data=sample_data.latest_data)


@app.route('/history')
def history():
    return render_template("history.html", app_data=sample_data.app_data, data=sample_data.history_data)


@app.route('/about')
def about():
    return render_template("about.html", app_data=sample_data.app_data, data=sample_data.latest_data)


@app.route('/get-todo', methods=['POST'])
def get_todo():
    print("KEY :: VALUE (from the received form data)")
    print([(key, val) for key, val in zip(request.form.keys(), request.form.values())])
    return redirect("/notes", code=302)


#
# @app.route('/analytics')
# def analytics():
#     return "<h4> Sorry ! NOT AVAILABLE YET </h4> " \
#            "<hr/> " \
#            "<p> Navigate to the <a href='/'> home </a> </p>"
#
#
# @app.route('/crawler-history')
# def crawler_history():
#     return "<h4> Sorry ! NOT AVAILABLE YET </h4>" \
#            "<hr/> " \
#            "<p> Navigate to the <a href='/'> home </a> </p>"


@app.route('/help')
@app.route('/info')
@app.route('/notes')
def info():
    return render_template("notes.html", app_data=sample_data.app_data)
    # return "<h4> Write your notes here </h4> " \
    #        "<textarea style='height: 40%; width: 100%' placeholder='Type here'> Type something here ... </textarea>" \
    #        "<button> Store </button>" \
    #        "<hr/> " \
    #        "<p> Navigate to the <a href='/'> home </a> </p>"

# ==============================================================
# Extra routes starts
# ==============================================================
@app.route('/sample1')
def sample1():
    return render_template("web-analytics-overview.html")


@app.route('/sample2')
def sample2():
    return render_template("web-analytics-real-time.html")


@app.route('/logo')
def get_logo():
    """
    Queries the snapshot data for both Serenity and JMeter projects from the MongoDB.
    Renders the Snapshot view of html
    :return: N/A
    """
    # set template directory of the Flask App to the  path set by the user as command line arg.
    return f'<html><head><title>Root</title><head><body><hr/> Welcome to the main page <hr/> ' \
           f'Building image from static static location: <br/> ' \
           f'<img src=\'{url_for("static", filename="images/logo.svg")}\' /> </body></html>'


@app.route('/used-data')
def get_used_data():
    return jsonify(sample_data.latest_data)



@app.route('/sample-data')
def get_sample_data():
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


@app.route('/error')
def get_error():
    # It will throw an error
    d = {1: True, 2: False}
    json.dumps(d)
    return json.stringify(d)
# ==============================================================
# Extra routes ends
# ==============================================================


# ==============================================================
# Error Handlers Starts
# ==============================================================
# 404 Handler; We can also pass the specific request errors codes to the decorator;
@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(err):
    return render_template("error.html", app_data=sample_data.app_data, error_data=err), 400


# Exception/Error handler; We can also pass the specific errors to the decorator;
@app.errorhandler(TypeError)
def server_error(err):
    app.logger.exception(err)
    return render_template("error.html", app_data=sample_data.app_data, error_data=err), 500


# Exception/Error handler; We can also pass the specific errors to the decorator;
@app.errorhandler(Exception)
def server_error(err):
    app.logger.exception(err)
    return render_template("error.html", app_data=sample_data.app_data, error_data=err), 500

# ==============================================================
# Error Handlers Ends
# ==============================================================


# ==============================================================
# Executor
# ==============================================================
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=10000, threaded=True)  # Running the app in debug mode
