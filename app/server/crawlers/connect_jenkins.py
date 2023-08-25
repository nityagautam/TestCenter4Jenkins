# Python Jenkins API
# http://0.0.0.0:8080/api/python?pretty=true
import json

import jenkins
import requests

server = jenkins.Jenkins('http://localhost:8080', username='admin', password='admin')
user = server.get_whoami()
version = server.get_version()
print('Hello %s from Jenkins %s' % (user['fullName'], version))

# fetch build data
print("Job Name: Test1 info: \n\n")
try:
    data = server.get_job_info("Job1", depth=0, fetch_all_builds=True)

    print(f"Job Display Name: {data['name']}")
    print(f"Job URL: {data['url']}")
    print(f"Total Builds: {len(data['builds'])}")
    print(f"Next Build Number: {data['nextBuildNumber']}")
    print(f"Last Build: {data['lastBuild']}")
    print(f"Builds: {data['builds']}")
    d = json.loads(json.dumps(data))
    #print(f"\n\n Extra: \n {d}")
except requests.exceptions.HTTPError as e:
    pass
except jenkins.NotFoundException as e:
    pass
except jenkins.JenkinsException as e:
    pass


class ConnectToJenkins:
    def __init__(self):
        pass

    def get_jobs_list(self):
        pass

    def get_build_data(self, build_no):
        pass

