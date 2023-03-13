"""
  @author Ashutosh Mishra (@github: nityagautam)

  Software Engineer & Explorer
  nityanarayan44@gmail.com

  Created on 14 February, 2023 @ 10:25 AM.
"""

import os
from flask import Flask
from app.server.dbase.db_crud import generate_sample_data_to_db
from app.settings import STATIC_FOLDER, TEMPLATE_FOLDER, APP_SRC_DIR_NAME


# ==========================================================================
# Generate the dummy data
# ==========================================================================
print("*"*20, "\n PREPARING SAMPLE DB\n", "*"*20, )
users_obj, projects_obj, test_executions_obj = generate_sample_data_to_db()

# Preparing user database.
# ---------------------------
users = {}
lst_users = users_obj.list_all()
for user in lst_users:
    users[user[1]] = user[2]
print(f"==> Prepared list of users: {users}")

# ==========================================================================
# Creating/Registering app object from the Flask
# ==========================================================================
app = Flask(__name__, static_folder=STATIC_FOLDER, template_folder=TEMPLATE_FOLDER)
app.config.from_object(f'{APP_SRC_DIR_NAME}.server.config.mode.Development')
app.secret_key = os.urandom(12)

# ==========================================================================
# Now, Importing server routes
# ==========================================================================
from app.server.routes import login, errors, controllers, apis

