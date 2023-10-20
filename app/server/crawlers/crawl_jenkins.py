"""
    @author:
      Ashutosh Mishra (@github: nityagautam)
      Software Engineer & Explorer
      nityanarayan44@gmail.com

    Created: 11 Jan, 2022
    reviewer:
    last modified: 02 Oct 2023
    desc: Crawls to Jenkins server for the job/build info/test-reports;
"""

# Python Jenkins API
# http://0.0.0.0:8080/api/python?pretty=true
import datetime
import json
import jenkins
import requests
from app.server.config.crawler_configurations import CrawlerConfig
from app.server.dbase.DBAccess import DBAccess


class CrawlJenkins:
    # Server ref
    server = None

    # execution / test report Fields name
    test_report_fields = {
        "JOB_NAME": "jenkins_job_name",
        "BUILD_NO": "jenkins_job_build_no",
        "JOB_URL": "jenkins_job_build_url",
        "JOB_TIMESTAMP": "jenkins_job_build_timestamp",
        "SUITE_NAMES": "suite_names",
        "TEST_RESULT": "test_result",
        "TAGS": "tags",
        "TOTAL": "total_count",
        "PASS": "pass_count",
        "FAIL": "fail_count",
        "SKIP": "skip_count",
        "DURATION": "duration_in_sec",
        "CRAWL_DATE": "crawled_date"
    }

    def __init__(self, url: str, username: str = '', password: str = '', timeout: int = 60, retry: int = 1):
        # data access
        self.db_obj = DBAccess()

        # jenkins props
        self.jenkins_url = url
        self.username = username
        self.password = password
        self.timeout = timeout
        self.retry = retry

        # other props values
        self.server = None
        self.jenkins_user = None
        self.jenkins_user_fullname = None
        self.jenkins_version = None
        self.build_no = None

        # For logging the info
        self.write_output = CrawlerConfig.write_output      # Boolean
        self.output_file = CrawlerConfig.crawler_output_file
        self.output_file_mode = CrawlerConfig.crawler_output_file_mode
        self.log_file = "crawler_log.log"
        self.log_file_mode = "+w"

    def connect(self):
        try:
            self.server = jenkins.Jenkins(url=self.jenkins_url,
                                          username=self.username,
                                          password=self.password,
                                          timeout=self.timeout)
            print("|  [Jenkins Crawler] Fetching Jenkins Server information...")
            self.jenkins_user = self.server.get_whoami()
            self.jenkins_version = self.server.get_version()
            self.jenkins_user_fullname = self.jenkins_user['fullName']

            # Success message for connection
            print(f'|\n'
                  f'|  +--[Jenkins Crawler]{"-"*58}+\n'
                  f'|  | Connected to jenkins ({self.jenkins_url}) ! \n'
                  f'|  | Hello {self.jenkins_user_fullname} from Jenkins v[{self.jenkins_version}] \n'
                  f'|  | Total Jenkins job count: {self.get_jenkins_job_count()} \n'
                  f'|  +--{"-"*75}+\n|')

            return self
        except requests.exceptions.HTTPError as e:
            print(f"|  [Login Error] There is a HTTP problem: \n {e}")
            raise e
        except jenkins.NotFoundException as e:
            # Failure message
            print(f'|\n'
                  f'|  +--[Jenkins Crawler Error]{"-" * 52}+\n'
                  f'|  | Failed to Connect to jenkins ({self.jenkins_url}) ! \n'
                  f'|  | Error: 404 \n'
                  f'|  | {e} \n'
                  f'|  +--{"-" * 75}+\n|')
            raise e
        except jenkins.JenkinsException as e:
            # Failure message
            print(f'|\n'
                  f'|  +--[Jenkins Crawler Error]{"-" * 52}+\n'
                  f'|  | Failed to Connect to jenkins ({self.jenkins_url}) ! \n'
                  f'|  | Error: JenkinsException \n'
                  f'|  | {e} \n'
                  f'|  +--{"-" * 75}+\n|')
            raise e
        except Exception as e:
            # Failure message
            print(f'\n'
                  f'|  +--[Jenkins Crawler Error]{"-" * 52}+\n'
                  f'|  | Failed to Connect to jenkins ({self.jenkins_url}) ! \n'
                  f'|  | Creds: ({self.username}:{self.password}) \n'
                  f'|  | Reason: {e} \n'
                  f'|  +--{"-" * 75}+\n|')
            raise e

    def __jenkins_job_does_exist(self, jenkins_job_name: str):
        return self.server.job_exists(name=jenkins_job_name)

    def __verify_job_exists(self, jenkins_job_name: str) -> bool:
        return self.server.assert_job_exists(name=jenkins_job_name, exception_message="Jenkins job [%s] does not exist")

    def __get_jenkins_jobs_list(self):
        return self.server.get_jobs_list()

    def get_jenkins_build_data(self, build_no):
        pass

    def get_latest_jenkins_build_data(self):
        pass

    def __get_jenkins_job_info(self, jenkins_job_name):
        try:
            print(f"|  [JENKINS JOB INFO] Fetching for [{jenkins_job_name}]...")
            if self.__jenkins_job_does_exist(jenkins_job_name):
                data = self.server.get_job_info(jenkins_job_name, depth=0, fetch_all_builds=False)
                # print(f"Job Display Name: {data['name']}")
                # print(f"Job Full Name: {data['fullName']}")
                # print(f"Job URL: {data['url']}")
                # print(f"Total Builds: {len(data['builds'])}")
                # print(f"Next Build Number: {data['nextBuildNumber']}")
                # print(f"Last Build: {data['lastBuild']}")
                # print(f"Builds: {data['builds']}")
                # print(f"\nObject Dump: \n {json.dumps(data)}")
                print("|  [JENKINS JOB INFO] Returning job info")
                return data
            else:
                print(f"|  Provided Jenkins job [{jenkins_job_name}] does not exist")
                return None
        except requests.exceptions.HTTPError as e:
            print(f"|  There is a HTTP problem: \n {e}")
        except jenkins.NotFoundException as e:
            print(f"|  There is a 404 problem: \n {e}")
        except jenkins.JenkinsException as e:
            print(f"|  There is a Jenkins Exception problem: \n {e}")

    def __get_jenkins_job_build_info(self, jenkins_job_name: str, jenkins_build_number: int) -> any:
        try:
            print(f"|  [JENKINS JOB BUILD INFO] Fetching for [{jenkins_job_name}]...")
            return self.server.get_build_info(jenkins_job_name, jenkins_build_number, depth=0)
        except requests.exceptions.HTTPError as e:
            print(f"|  There is a HTTP problem: \n {e}")
        except jenkins.NotFoundException as e:
            print(f"|  There is a 404 problem: \n {e}")
        except jenkins.JenkinsException as e:
            print(f"|  There is a Jenkins Exception problem: \n {e}")

    def __get_jenkins_job_test_report_data(self, jenkins_job_name: str, jenkins_build_number: int, depth: int = 0) -> any:
        """
        To fetch the latest test report for a jenkins job for a given build number.

        Usage:  obj.get_jenkins_job_test_report_data('job1', 10)
                obj.get_jenkins_job_test_report_data('job1', 10, 0)

        Output sample:
                    {
                        "jenkins_job_name": "SomeJobName",
                        "jenkins_job_build_no": 26,
                        "jenkins_job_url": "https://jenkins_url/abcd",
                        "duration_in_sec": 69521.82,
                        "suite_names": [
                            "suite_Regression_Testing"
                        ],
                        "test_result": {
                            "total_count": 4674,
                            "pass_count": 4626,
                            "fail_count": 48,
                            "skip_count": 0
                        },
                        "jenkins_job_timestamp": 1695559740364,
                        "crawled_date": "2023-10-02 00:03:18.895308"
                    }

        :param jenkins_job_name:str Jenkins Job name,
        :param jenkins_build_number:int Jenkins Build number,
        :param depth:int
        :return: dict object with test execution report
        """
        compiled_data = None
        try:
            # If job exist then fetch
            if self.__jenkins_job_does_exist(jenkins_job_name):
                print(f"|\n|  [JENKINS TEST REPORT] Fetching for ({jenkins_job_name}/{jenkins_build_number})...")
                # composing job url
                job_build_info = self.__get_jenkins_job_build_info(jenkins_job_name, jenkins_build_number)

                if job_build_info:
                    job_url = job_build_info["url"]
                    # job_status = job_build_info["result"]
                    job_timestamp = job_build_info["timestamp"]
                    # time_stamp = ''
                    # fetching data for build test report
                    data = self.server.get_build_test_report(name=jenkins_job_name,
                                                             number=jenkins_build_number,
                                                             depth=depth)
                    # Composing columns based on data
                    if data:
                        # TODO: removing for now:
                        # "suite_details": data['suites']
                        print("|  [JENKINS TEST REPORT] Collecting...")
                        compiled_data = {
                            self.test_report_fields["JOB_NAME"]: jenkins_job_name,
                            self.test_report_fields["BUILD_NO"]: jenkins_build_number,
                            self.test_report_fields["JOB_URL"]: job_url,
                            self.test_report_fields["DURATION"]: data['duration'],
                            self.test_report_fields["SUITE_NAMES"]: list(set([suite['name'] for suite in data['suites']])),
                            self.test_report_fields["TEST_RESULT"]: {
                                # self.test_report_fields["TOTAL"]: int(data['passCount']) + int(data['failCount']) + int(data['skipCount']),
                                self.test_report_fields["PASS"]: data['passCount'],
                                self.test_report_fields["FAIL"]: data['failCount'],
                                self.test_report_fields["SKIP"]: data['skipCount']
                            },
                            self.test_report_fields["TAGS"]: "",
                            self.test_report_fields["JOB_TIMESTAMP"]: job_timestamp,
                            self.test_report_fields["CRAWL_DATE"]: str(datetime.datetime.now())
                        }
                    else:
                        print("|  [JENKINS TEST REPORT] Test report is not available, "
                              "either the job was aborted or failed due to setup.")
                        compiled_data = {
                            self.test_report_fields["JOB_NAME"]: jenkins_job_name,
                            self.test_report_fields["BUILD_NO"]: jenkins_build_number,
                            self.test_report_fields["JOB_URL"]: job_url,
                            self.test_report_fields["DURATION"]: 0,
                            self.test_report_fields["SUITE_NAMES"]: [],
                            self.test_report_fields["TEST_RESULT"]: {
                                # self.test_report_fields["TOTAL"]: 0,
                                self.test_report_fields["PASS"]: 0,
                                self.test_report_fields["FAIL"]: 0,
                                self.test_report_fields["SKIP"]: 0
                            },
                            self.test_report_fields["TAGS"]: "",
                            self.test_report_fields["JOB_TIMESTAMP"]: job_timestamp,
                            self.test_report_fields["CRAWL_DATE"]: str(datetime.datetime.now())
                        }

                    # return the data
                    return compiled_data
                else:
                    return None

            else:
                print(f"|  Provided jenkins job [{jenkins_job_name}] does not exist")
                return None
        except requests.exceptions.HTTPError as e:
            print(f"|  There is a HTTP problem: \n {e}")
        except jenkins.NotFoundException as e:
            print(f"|  There is a 404 problem: \n {e}")
        except jenkins.JenkinsException as e:
            print(f"|  There is a Jenkins Exception problem: \n {e}")

    def __get_builds_no_to_crawl(self, builds_no_from_db: list = [], input_list_of_build_no: list = []):

        # 1- create the final list
        final_build_no_list = list(input_list_of_build_no)

        # 2- verify and reduce the input list based on the existing from the DB
        for build_from_db in builds_no_from_db:
            if build_from_db in final_build_no_list:
                final_build_no_list.remove(build_from_db)

        # 3- Output / Log
        # print(f"|  [CRAWL CHECK] Given builds: {input_list_of_build_no}")
        # print(f"|  [CRAWL CHECK] Existing DB builds: {builds_no_from_db}")
        print(f"|  [CRAWL CHECK] Final List to crawl: {final_build_no_list}")

        # 4- Return the final build_no list
        return final_build_no_list

    def __resolve_builds_range(self, build_list: any = None, start: int = 1, end: int = 2) -> any:

        # 1- Resole given build range/list
        list_of_builds_no = []
        # print(f"|  [RESOLV BUILD RANGE] Given data: ({build_list}, {start}, {end})")
        if build_list is not None:
            list_of_builds_no = build_list
        else:
            list_of_builds_no = [no for no in range(start, end+1)] if ((start > 0 and end > 0) and (start <= end)) else []

        # 2- Return the list of build no
        return list_of_builds_no

    def __get_jenkins_test_report_for_builds(self, jenkins_job_name: str, build_list: list = [], start: int = 1, end: int = 2, depth: int = 0) -> any:
        """
            To fetch the latest test report for a jenkins job for a given build number.

            Usage:  obj.get_historical_test_reports_for_job_with_build_range('job1', build_list=[1, 2])
                    obj.get_historical_test_reports_for_job_with_build_range('job1', start=1, end=2)
                    obj.get_historical_test_reports_for_job_with_build_range('job1', start=1, end=1)
                    obj.get_historical_test_reports_for_job_with_build_range('job1', start=1, end=2, depth=0)

            Output sample:
                        [
                            {
                                "jenkins_job_name": "SomeJobName",
                                "jenkins_job_build_no": 26,
                                "jenkins_job_url": "https://jenkins_url/abcd",
                                "duration_in_sec": 69521.82,
                                "suite_names": [
                                    "suite_Regression_Testing"
                                ],
                                "total_count": 4674,
                                "pass_count": 4626,
                                "fail_count": 48,
                                "skip_count": 0,
                                "jenkins_job_timestamp": 1695559740364,
                                "crawled_date": "2023-10-02 00:03:18.895308"
                            },
                            ...


            :param jenkins_job_name:str Jenkins Job name,
            :param start:int starting jenkins build number for range
            :param end:int ending jenkins build number for range
            :param depth:int
            :return: dict object with test execution report for n number of builds
        """

        compiled_data = []

        # 1 - If jenkins job exist then proceed
        if self.__jenkins_job_does_exist(jenkins_job_name):

            # 1.1 - Get the verified build list to be crawled
            builds_no_to_crawl = self.__get_builds_no_to_crawl(
                    builds_no_from_db=list(set([number[0] for number in self.db_obj.get_builds_from_execution_data(jenkins_job_name)])),
                    input_list_of_build_no=self.__resolve_builds_range(build_list, start, end))

            # 1.2 - If we have any build(s) to crawl
            if len(builds_no_to_crawl) > 0:

                # 1.2.1 - Start Fetching for the builds
                print(f"|  [TEST REPORT FOR BUILDS] Fetching for job:{jenkins_job_name} for builds: {builds_no_to_crawl}")
                for build_no in builds_no_to_crawl:
                    # 1.2.1.1 - fetch job test report for the first time
                    data_retry_count = self.retry
                    data = self.__get_jenkins_job_test_report_data(jenkins_job_name, build_no, depth)

                    # 1.2.1.2 - Applying Retry, incase data is null for the very first time
                    while not data and data_retry_count > 0:
                        print("|  [TEST REPORT FOR BUILDS] Retrying...")
                        data = self.__get_jenkins_job_test_report_data(jenkins_job_name, build_no, depth)
                        data_retry_count -= 1

                    # 1.2.1.3 - Append into the final list
                    compiled_data.append(data)
                    print("|  ")

                # if logging the collected output is true the write to output file
                if self.write_output:
                    print(f"|  [TEST REPORT FOR BUILDS] Writing to file:{self.output_file} ...")
                    self.write_to_file(json.dumps(compiled_data, indent=4, separators=(',', ': ')))

                # return the collected data
                return compiled_data

            else:
                print(f"|  [TEST REPORT FOR BUILDS] Up to date for Job:{jenkins_job_name} for builds: {builds_no_to_crawl}")

        else:
            print(f"[TEST REPORT FOR BUILDS] Provided jenkins job [{jenkins_job_name}] does not exist.")

        # If flow comes this end, then return the empty list
        return compiled_data

    # ======================================================================
    # === [PUBLIC API] =====================================================
    # ======================================================================

    def write_to_file(self, data):
        try:
            with open(self.output_file, self.output_file_mode) as f:
                f.write(data)
                f.close()
        except Exception as e:
            # Failure message
            print(f'|\n'
                  f'|  +--[Jenkins Crawler Error]{"-" * 52}+\n'
                  f'|  | Failed to write output to file: ({self.output_file}) \n'
                  f'|  | Error: {e} \n'
                  f'|  +--{"-" * 75}')

    def get_jenkins_job_count(self):
        return self.server.jobs_count()

    def get_user_fullname(self):
        if not self.jenkins_user_fullname:
            self.jenkins_user_fullname = self.server.get_whoami()
        return self.jenkins_user_fullname

    def get_jenkins_version(self):
        if not self.jenkins_version:
            self.jenkins_version = self.server.get_version()
        return self.jenkins_version

    def get_builds_from_jenkins(self, jenkins_job_name: str) -> list:
        # 1- Extract the job info
        list_of_build_no = []
        job_info = self.__get_jenkins_job_info(jenkins_job_name)

        # 2- fetch the available builds for the job
        if job_info:
            # Fetch all the builds no
            list_of_build_no = [build["number"] for build in job_info["builds"]]

        # 3- return
        return list_of_build_no

    def get_all_test_reports_for_job(self, jenkins_job_name: str) -> any:
        print("|  [GET ALL TEST REPORT] Initiating...")
        # Fetch for the start and end build no
        return self.__get_jenkins_test_report_for_builds(jenkins_job_name, build_list=self.get_builds_from_jenkins(jenkins_job_name))

    def get_latest_test_reports_for_job(self, jenkins_job_name: str) -> any:
        print("|  [GET LATEST TEST REPORT] Initiating...")
        # Fetch the result for the latest build no
        return self.__get_jenkins_test_report_for_builds(jenkins_job_name, build_list=max(self.get_builds_from_jenkins(jenkins_job_name)))

    def get_nth_test_report_for_job(self, jenkins_job_name: str, nth_build_no: int = 1) -> any:
        # Fetch the job info
        # Fetch the last build no
        # Loop for the start and end build no
        return self.__get_jenkins_test_report_for_builds(jenkins_job_name, nth_build_no, nth_build_no)


# ====[ CLI Execution ]======================
if __name__ == "__main__":

    print("[Jenkins Crawler] FROM CLI ...")
    # DATA
    # --------------
    jenkins_host_url = "https://jenkins_url"
    jenkins_username = 'username'
    jenkins_password = 'pwd'
    req_timeout = 60

    # TODO: Change the job/build streams or the full names as needed
    # Sample data for job names
    job_name = ["SomeJobName"]
    job_build_no = 22

    # Object creation
    # ----------------------
    start_time = datetime.datetime.now()
    obj = CrawlJenkins(jenkins_host_url, jenkins_username, jenkins_password, req_timeout).connect()

    # Method call
    # ----------------------
    # Get Latest test reports
    # out = obj.get_latest_test_reports_for_job(job_name[1])

    # Get All test reports
    out = obj.get_all_test_reports_for_job(job_name[5])

    # Get the nth test reports
    # out = obj.get_nth_test_report_for_job(job_name[1], job_build_no)
    end_time = datetime.datetime.now()

    # DEBUG / LOG
    obj.write_to_file(json.dumps(out, indent=4, separators=(',', ': ')))
    # print(json.dumps(out, indent=4, separators=(',', ': ')))
    print(f"Time taken: {end_time-start_time} sec")


if __name__ == "__mmain__":
    # a = '"{\\"pass_count\\": 10, \\"fail_count\\": 2, \\"skip_count\\": 1}"'
    # b='"{\\"pass_count\\": 98, \\"fail_count\\": 99, \\"skip_count\\": 153}"'
    # print(json.loads(b))
    c = [(12,)]
    print(c[0][0])
