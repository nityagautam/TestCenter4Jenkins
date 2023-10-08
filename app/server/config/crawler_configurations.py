from app.server.config.configurations import Configurations


class CrawlerConfig(Configurations):
    # ----------------------------------
    # Jenkins data
    # ----------------------------------
    # jenkins_host_url = "https://jenkins.qac.perforce.com"  # "https://jenkins.qac.perforce.com"
    # jenkins_username = 'amishra'
    # jenkins_password = 'Me@here1'
    # This is access token
    # self.password = "11f9cada0ab7b05ef59afce3f260eba6c9"
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
