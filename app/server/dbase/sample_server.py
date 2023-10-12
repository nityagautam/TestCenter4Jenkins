from flask import Flask
from flask import jsonify
from flask import render_template
from app.server.dbase import sample_data

# ==============================================================
# Flask configuration
# ==============================================================
public_folder_path = "/ReportDashboard/app/client/static"
public_folder_name = "static"
app = Flask(__name__, static_url_path=public_folder_path, static_folder=public_folder_name)


# ==============================================================
# App Routes/Gateways
# ==============================================================
@app.route('/')
@app.route('/home')
def root():
    return jsonify({"msg": "Welcome to the server"})


@app.route('/api/v1/hi')
def get_used_data():
    return jsonify({"msg": "Hi"})


@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html", app_data=sample_data.app_data, data=sample_data.latest_data)


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


# ==============================================================
# Error Handlers Ends
# ==============================================================


# ==============================================================
# Executor
# ==============================================================
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=10000, threaded=True)  # Running the app in debug mode
