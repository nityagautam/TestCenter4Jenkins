"""
  @author Ashutosh Mishra (@github: nityagautam)
  
  Software Engineer & Explorer
  nityanarayan44@gmail.com
  
  Created on 14 February, 2023 @ 10:25 AM.
"""

# Import Section
# ==========================
import os


# Application Structure
# ==========================
# ReportDashboard
#               \____ app                           # This is the application source dir
#                   |____ client
#                       |____ static                # This contains all the static sources like: js, css
#                       |____ templates             # This contains all the HTML source files
#
#                   |____ server
#                       |____ entire source code lies here # This has all the python3 back-end server logic
#                       |____ config
#                       |____ crawlers
#                       |____ dbase
#                       |____ routes
#                       |____ unittests
#                       |____ utilities
#                       |____ views
#
#                   |____ __init__.py
#                   |____ settings.py               # This contains the setting for the client dirs/folders
#
#               |____ LICENSE
#               |____ main.py                       # This is the entry point; starts the server
#               |____ pytest.ini                    # This is pytest configuration for testing server
#               |____ README.md                     # Refer this file for more details of HowTo
#               |____ requirements.txt              # Python packages requirement file
#


# Core details
# ==========================
APP_SERVER_HOST = '0.0.0.0'
APP_SERVER_PORT = 8000
APP_SRC_DIR_NAME = 'app'    # This is the name for the very first level dir in this repo source
APP_NAME = 'REPORT_DASHBOARD'
AUTHOR_NAME = 'Ashutosh Mishra [amishra]'
APP_VERSION = '1.0.0'
APP_MODE_TAG = 'Experimental'

# Set the dirs location based on the app dir name
# ===================================================
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

# Our fallback users.
# ===================
fallback_users = {'username': 'admin', 'password': 'admin'}
