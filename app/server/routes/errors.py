"""
  @author Ashutosh Mishra (@github: nityagautam)

  Software Engineer & Explorer
  nityanarayan44@gmail.com

  Created on 14 February, 2023 @ 10:25 AM.
"""
from app.server import app as application
from flask import flash
from app.server.config.ui_configurations import UIConfigurations
from app.server.routes.authentication import not_authorised, route_gateway


# ==============================================================
# Error Handlers Starts
# ==============================================================

# 404 Handler; We can also pass the specific request errors codes to the decorator;
@application.errorhandler(404)
def not_found(err):
    if route_gateway.is_session_active():
        flash(UIConfigurations.ERROR_MESSAGES['404'])
        return route_gateway.get_error_template("/error", err, 404)
    return not_authorised()


# Exception/Error handler; We can also pass the specific errors to the decorator;
@application.errorhandler(TypeError)
def type_error(err):
    application.logger.exception(err)
    if route_gateway.is_session_active():
        flash(UIConfigurations.ERROR_MESSAGES['500'])
        return route_gateway.get_error_template("/error", err, 500)
    return not_authorised()
    # return render_template("error.html", app_data=app_ui_config, error_data=err), 500


# Exception/Error handler; We can also pass the specific errors to the decorator;
@application.errorhandler(Exception)
def unknown_error(err):
    application.logger.exception(err)
    if route_gateway.is_session_active():
        flash(UIConfigurations.ERROR_MESSAGES['500'])
        return route_gateway.get_error_template("/error", err, 500)
    return not_authorised()
    # return render_template("error.html", app_data=app_ui_config, error_data=err), 500

# ==============================================================
# Error Handlers Ends
# ==============================================================

