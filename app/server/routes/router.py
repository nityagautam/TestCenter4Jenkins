#===============================================================
# @author:  nityanarayan44@live.com
# @written: 08 December 2021
# @desc:    Routes for the Backend server
#===============================================================

# Import section with referecne of entry file or main file;
#from __main__ import app
# from app.server import app as application
# from flask import jsonify, render_template, url_for, request, redirect
# from app.server.config.uiconfig import app_ui_config
# # Local sample data import
# from app.server.dbase import sample_data
#
#
# # ==============================================================
# # App Routes/Gateways
# # ==============================================================
# @application.route('/test', methods=['GET'])
# def test():
#     return '<h4>HELLO WORLD!</h4><hr/> it works!'
#
#
# @application.route('/history', methods=['GET'])
# def history():
#     return render_template("history.html", app_data=app_ui_config, data=sample_data.history_data)
#
#
# @application.route('/get-notes', methods=['POST'])
# def get_todo():
#     print("KEY :: VALUE (from the received form data)")
#     print([(key, val) for key, val in zip(request.form.keys(), request.form.values())])
#     return redirect("/notes", code=302)
#
#
# @application.route('/sample-data')
# def get_sample_data():
#     return jsonify(app_ui_config)
