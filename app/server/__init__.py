"""
  @author Ashutosh Mishra (@github: nityagautam)

  Software Engineer & Explorer
  nityanarayan44@gmail.com

  Created on 14 February, 2023 @ 10:25 AM.
"""

import os
from flask import Flask
from app.settings import STATIC_FOLDER, TEMPLATE_FOLDER, APP_SRC_DIR_NAME

# Creating/Registering app object from the Flask
app = Flask(__name__, static_folder=STATIC_FOLDER, template_folder=TEMPLATE_FOLDER)
app.config.from_object(f'{APP_SRC_DIR_NAME}.server.config.mode.Development')
app.secret_key = os.urandom(12)

# Now, Importing server routes
from app.server.routes import login, errors, controllers, apis
