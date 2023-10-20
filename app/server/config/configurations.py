"""
    @author:
      Ashutosh Mishra (@github: nityagautam)
      Software Engineer & Explorer
      nityanarayan44@gmail.com

    Created: 11 Jan, 2022
    reviewer:
    last modified:
    desc: Configuration file
"""

# ==========================
# Import Section
# ==========================
import os
from passlib.hash import sha256_crypt


# ==========================
# Base Configurations
# ==========================
class Configurations(object):
    # -------------------
    # Core properties
    # -------------------
    APP_NAME = 'TEST_CENTER'
    AUTHOR_NAME = 'Ashutosh Mishra'
    APP_VERSION = '1.0.0'
    APP_ENVIRONMENT = "TEST"
    DEBUG = True
    TESTING = True

    # Flask app configs
    # ----------------------------------------------------
    APP_SERVER_HOST = '0.0.0.0'
    APP_SERVER_PORT = 8000
    # This is the name for the very first level dir in this repo source
    APP_SRC_DIR_NAME = 'app'
    APP_SECRET_KEY = sha256_crypt.encrypt(APP_SRC_DIR_NAME)
    APP_SECRET_KEY_OTHER = os.urandom(12)
    APP_API_BASE_ROUTE = "/api/v1"

    # Dirs location based on the app dir name
    # ----------------------------------------------------
    PROJECT_DIR = os.getcwd()
    PROJECT_SUB_DIR = os.path.join(PROJECT_DIR, APP_SRC_DIR_NAME)

    # This is for the server & client locations
    # ----------------------------------------------------------
    CLIENT_FOLDER = os.path.join(PROJECT_SUB_DIR, 'client')
    SERVER_FOLDER = os.path.join(PROJECT_SUB_DIR, 'server')

    # This is for the public shared assets (client stuff)
    # ----------------------------------------------------------
    STATIC_FOLDER = os.path.join(CLIENT_FOLDER, 'static')
    TEMPLATE_FOLDER = os.path.join(CLIENT_FOLDER, 'templates')


# =============================================
# Classes used for Flask configurations
# =============================================
class Development(Configurations):
    DEBUG = True


class Testing(Configurations):
    TESTING = True


class Production(Configurations):
    # For DB config, Look into app/server/config/db_configurations.py
    # MYSQL_DATABASE_URI = f'mysql://amishra@localhost/app'
    pass
