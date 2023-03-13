#===============================================================
# @author       : Ashutosh Mishra [nityanarayan44@live.com]
# @written      : 08 December 2021
# @re-written   : 14 February 2023
# @desc         : Backend server for the Dashboard of reports.
#===============================================================

# Import section
#from flask import Flask
#from app.server.utilites.console_animator import ConsoleAnimator
# import multiprocessing
import argparse
import datetime
import subprocess
from app.settings import STATIC_FOLDER
from app.server.dbase.db_crud import Projects


# Runner Class
# ======================
class Runner:
    DEBUG = True
    LAST_STDOUT = None

    def __init__(self):
        pass

    # Do some extra work
    def do_extra_work(self):
        subprocess.call('cd {} && npm run watch'.format(STATIC_FOLDER.replace(' ', '\ ')), shell=True)
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
        from app.settings import APP_SERVER_HOST, APP_SERVER_PORT
        app.run(host=APP_SERVER_HOST, port=APP_SERVER_PORT, threaded=True, debug=self.DEBUG)


# ==============================================================
# App Execution
# ==============================================================
def normal_db_usage():
    o = Projects()
    # o.delete_all()
    o.add(project_name="project2",
          data_source='Jenkins',
          jenkins_url='http://localhost:8080', jenkins_user='NIL', jenkins_password='NIL',
          status='active',
          created=datetime.datetime.now(),
          last_modified=datetime.datetime.now())
    print("Listed Projects ===> ", o.list_all())

    # Release cursor
    o.release()


if __name__ == '__main__':
    # Runner().run()
    normal_db_usage()

