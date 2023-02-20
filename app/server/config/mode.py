"""
  @author Ashutosh Mishra (@github: nityagautam)

  Software Engineer & Explorer
  nityanarayan44@gmail.com

  Created on 14 February, 2023 @ 10:25 AM.
"""

from app.server.config.base import Config, APP_SRC_DIR_NAME


class Production(Config):
    DATABASE_URI = f'mysql://victor@localhost/{APP_SRC_DIR_NAME}'


class Development(Config):
    DEBUG = True


class Testing(Config):
    TESTING = True
