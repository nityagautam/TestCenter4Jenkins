"""
  @author Ashutosh Mishra (@github: nityagautam)

  Software Engineer & Explorer
  nityanarayan44@gmail.com

  Created on 14 February, 2023 @ 10:25 AM.
"""

from passlib.hash import sha256_crypt
from app.settings import APP_SRC_DIR_NAME


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = sha256_crypt.encrypt(APP_SRC_DIR_NAME)
