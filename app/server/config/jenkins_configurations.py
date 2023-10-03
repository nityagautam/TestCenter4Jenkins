from app.server.config.configurations import Configurations


class JenkinsConfig(Configurations):
    # ----------------------------------
    # Jenkins data
    # ----------------------------------
    jenkins_host_url = "https://jenkins.qac.perforce.com"  # "https://jenkins.qac.perforce.com"
    jenkins_username = 'amishra'
    jenkins_password = 'Me@here1'
    # This is access token
    # self.password = "11f9cada0ab7b05ef59afce3f260eba6c9"
    req_timeout = 60

