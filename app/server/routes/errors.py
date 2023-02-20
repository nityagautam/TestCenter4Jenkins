"""
  @author Ashutosh Mishra (@github: nityagautam)

  Software Engineer & Explorer
  nityanarayan44@gmail.com

  Created on 14 February, 2023 @ 10:25 AM.
"""
from app.server import app as application
from flask import jsonify, render_template, url_for, request, redirect
from app.server.config.uiconfig import app_ui_config


# ==============================================================
# Error Handlers Starts
# ==============================================================
# 404 Handler; We can also pass the specific request errors codes to the decorator;
@application.errorhandler(404)
def not_found(err):
    return render_template("error.html", app_data=app_ui_config, error_data=err), 400


# Exception/Error handler; We can also pass the specific errors to the decorator;
@application.errorhandler(TypeError)
def type_error(err):
    application.logger.exception(err)
    return render_template("error.html", app_data=app_ui_config, error_data=err), 500


# Exception/Error handler; We can also pass the specific errors to the decorator;
@application.errorhandler(Exception)
def unknown_error(err):
    application.logger.exception(err)
    return render_template("error.html", app_data=app_ui_config, error_data=err), 500
# ==============================================================
# Error Handlers Ends
# ==============================================================

