"""
  @author Ashutosh Mishra (@github: nityagautam)

  Software Engineer & Explorer
  nityanarayan44@gmail.com

  Created on 14 February, 2023 @ 10:25 AM.
"""
from app.server import app as application
from flask import jsonify, render_template, url_for, request, redirect
from flask import redirect, render_template, session
from app.server.config.uiconfig import app_ui_config
from app.server.routes.controllers import not_authorised
from app.settings import users


# ==============================================================
# Error Handlers Starts
# ==============================================================

# 404 Handler; We can also pass the specific request errors codes to the decorator;
@application.errorhandler(404)
def not_found(err):
    if 'user' in session and session['user'] == users['username']:
        return render_template(app_ui_config["routes"]["/error"]["template_name"],
                               pagename=app_ui_config["routes"]["/error"]["page_name"],
                               username=session['user'],
                               ui_config=app_ui_config,
                               app_data=app_ui_config,  # TODO: need to remove app_data from all routes
                               error_data=err
                               ), 404
    return not_authorised()


# Exception/Error handler; We can also pass the specific errors to the decorator;
@application.errorhandler(TypeError)
def type_error(err):
    application.logger.exception(err)
    if 'user' in session and session['user'] == users['username']:
        return render_template(app_ui_config["routes"]["/error"]["template_name"],
                               pagename=app_ui_config["routes"]["/error"]["page_name"],
                               username=session['user'],
                               ui_config=app_ui_config,
                               app_data=app_ui_config,  # TODO: need to remove app_data from all routes
                               error_data=err
                               ), 500
    return not_authorised()
    # return render_template("error.html", app_data=app_ui_config, error_data=err), 500


# Exception/Error handler; We can also pass the specific errors to the decorator;
@application.errorhandler(Exception)
def unknown_error(err):
    application.logger.exception(err)
    if 'user' in session and session['user'] == users['username']:
        return render_template(app_ui_config["routes"]["/error"]["template_name"],
                               pagename=app_ui_config["routes"]["/error"]["page_name"],
                               username=session['user'],
                               ui_config=app_ui_config,
                               app_data=app_ui_config,  # TODO: need to remove app_data from all routes
                               error_data=err
                               ), 404
    return not_authorised()
    # return render_template("error.html", app_data=app_ui_config, error_data=err), 500

# ==============================================================
# Error Handlers Ends
# ==============================================================

