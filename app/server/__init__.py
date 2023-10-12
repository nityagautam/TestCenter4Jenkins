"""
    @author:
      Ashutosh Mishra (@github: nityagautam)
      Software Engineer & Explorer
      nityanarayan44@gmail.com

    Created: 11 Jan, 2022
    reviewer:
    last modified: 12 Oct 2023
    desc: Flask app;
"""

from flask import Flask
from app.server.config.configurations import Configurations

# ==========================================================================
# Creating/Registering app object from the Flask
# ==========================================================================
app = Flask(__name__, static_folder=Configurations.STATIC_FOLDER, template_folder=Configurations.TEMPLATE_FOLDER)
app.config.from_object(f'{Configurations.APP_SRC_DIR_NAME}.server.config.configurations.Development')
app.secret_key = Configurations.APP_SECRET_KEY

# ==========================================================================
# Now, Importing server routes
# ==========================================================================
from app.server.routes import authentication, errors, router, apis

