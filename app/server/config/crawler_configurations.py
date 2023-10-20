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

from app.server.config.configurations import Configurations


class CrawlerConfig(Configurations):
    # ----------------------------------
    # Jenkins data
    # ----------------------------------
    # jenkins_host_url = "https://jenkins_url"
    # jenkins_username = 'username'
    # jenkins_password = 'password'
    req_timeout = 60

    # ----------------------------------
    # Crawler thread info
    # ----------------------------------
    crawler_thread = None
    crawler_alive = False
    crawler_status = None

    # ----------------------------------
    # Dump / logging
    # ----------------------------------
    write_output = True
    crawler_output_file = "./logs/crawler_output.txt"
    crawler_output_file_mode = "+w"
    crawler_log_file = "./logs/crawler_output.log"
    crawler_log_file_mode = "+w"
