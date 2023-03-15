# ===============================================================
# @author       : Ashutosh Mishra [nityanarayan44@live.com]
# @written      : 08 December 2021
# @re-written   : 14 February 2023
# @desc         : Backend server for the Dashboard of reports.
# ===============================================================

# Import section
# import multiprocessing
import argparse
import subprocess
from app.server.config.configurations import Configurations


# Runner Class
# ======================
class Runner(Configurations):
    DEBUG = True
    LAST_STDOUT = None

    def __init__(self):
        pass

    # Do some extra work
    def do_extra_work(self):
        subprocess.call('cd {} && npm run watch'.format(Configurations.STATIC_FOLDER.replace(' ', '\ ')), shell=True)
        # process = multiprocessing.Process(target=do_extra_work)
        # process.start()
        # process.join()
        self.LAST_STDOUT = None

    # Processing the CLI args (if any)
    def main(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-d', '--debug', default=True, help='Run the web server in debug mode.')
        args = parser.parse_args()
        #
        self.DEBUG = args['debug']

    def run(self):
        from app.server import app
        app.run(host=Configurations.APP_SERVER_HOST, port=Configurations.APP_SERVER_PORT, threaded=True, debug=self.DEBUG)


# ==============================================================
# App Execution
# ==============================================================
if __name__ == '__main__':
    # Run the flask server
    Runner().run()

