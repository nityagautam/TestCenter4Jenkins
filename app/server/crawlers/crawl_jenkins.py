"""
    @author: Ashutosh Mishra (amishra)
    @dated: 28 Sep 2023
    @last-modified: 02 Oct 2023
    @desc:
        Crawls to Jenkins server for the job/build info/test-reports;
"""

# Python Jenkins API
# http://0.0.0.0:8080/api/python?pretty=true
import datetime
import json
import jenkins
import requests


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
        "TOTAL": "total_count",
        "PASS": "pass_count",
        "FAIL": "fail_count",
        "SKIP": "skip_count",
        "DURATION": "duration_in_sec",
        "CRAWL_DATE": "crawled_date"
    }

    def __init__(self, url: str, username: str = '', password: str = '', timeout: int = 60, retry: int = 1):
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
        self.output_file = "out.txt"
        self.output_file_mode = "+w"
        self.log_file = "crawler_log.log"
        self.log_file_mode = "+w"

    def connect(self):
        try:
            self.server = jenkins.Jenkins(self.jenkins_url,
                                          username=self.username,
                                          password=self.password,
                                          timeout=self.timeout)
            self.jenkins_user = self.server.get_whoami()
            self.jenkins_version = self.server.get_version()
            self.jenkins_user_fullname = self.jenkins_user['fullName']
            # Success message
            print(f'Connected to jenkins ({self.jenkins_url}) ! \n'
                  f'Hello {self.jenkins_user_fullname} from Jenkins v[{self.jenkins_version}]')
            print(f"Total Jenkins job count: {self.get_jenkins_job_count()} \n\n")
            return self
        except requests.exceptions.HTTPError as e:
            print(f"[Login Error] There is a HTTP problem: \n {e}")
        except jenkins.NotFoundException as e:
            print(f"[Login Error] There is a 404 problem: \n {e}")
        except jenkins.JenkinsException as e:
            print(f"[Login Error] There is a Jenkins Exception problem: \n {e}")

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
            print(f"[JENKINS JOB INFO] Fetching for [{jenkins_job_name}]...")
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
                print(f"[JENKINS JOB INFO] Returning job info")
                return data
            else:
                print(f"Provided Jenkins job [{jenkins_job_name}] does not exist")
                return None
        except requests.exceptions.HTTPError as e:
            print(f"There is a HTTP problem: \n {e}")
        except jenkins.NotFoundException as e:
            print(f"There is a 404 problem: \n {e}")
        except jenkins.JenkinsException as e:
            print(f"There is a Jenkins Exception problem: \n {e}")

    def __get_jenkins_job_build_info(self, jenkins_job_name: str, jenkins_build_number: int) -> any:
        try:
            print(f"[JENKINS JOB BUILD INFO] Fetching for [{jenkins_job_name}]...")
            return self.server.get_build_info(jenkins_job_name, jenkins_build_number, depth=0)
        except requests.exceptions.HTTPError as e:
            print(f"There is a HTTP problem: \n {e}")
        except jenkins.NotFoundException as e:
            print(f"There is a 404 problem: \n {e}")
        except jenkins.JenkinsException as e:
            print(f"There is a Jenkins Exception problem: \n {e}")

    def __get_jenkins_job_test_report_data(self, jenkins_job_name: str, jenkins_build_number: int, depth: int = 0) -> any:
        """
        To fetch the latest test report for a jenkins job for a given build number.

        Usage:  obj.get_jenkins_job_test_report_data('job1', 10)
                obj.get_jenkins_job_test_report_data('job1', 10, 0)

        Output sample:
                    {
                        "jenkins_job_name": "FW-430/QAF_430_Test_Eclipse_Centos7x64_EN",
                        "jenkins_job_build_no": 26,
                        "jenkins_job_url": "https://jenkins.qac.perforce.com/abcd",
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
                print(f"[JENKINS TEST REPORT] Fetching for ({jenkins_job_name}/{jenkins_build_number})...")
                # composing job url
                job_build_info = self.__get_jenkins_job_build_info(jenkins_job_name, jenkins_build_number)

                if job_build_info:
                    job_url = job_build_info["url"]
                    job_status = job_build_info["result"]
                    job_timestamp = job_build_info["timestamp"]
                    time_stamp = ''
                    # fetching data for build test report
                    data = self.server.get_build_test_report(name=jenkins_job_name,
                                                             number=jenkins_build_number,
                                                             depth=depth)
                    # Composing columns based on data
                    if data:
                        # TODO: removing for now:
                        # "suite_details": data['suites']
                        print(f"[JENKINS TEST REPORT] Collecting...")
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
                            self.test_report_fields["JOB_TIMESTAMP"]: job_timestamp,
                            self.test_report_fields["CRAWL_DATE"]: str(datetime.datetime.now())
                        }
                    else:
                        print(f"[JENKINS TEST REPORT] Test report is not available, "
                              f"either the job was aborted or failed due to setup.")
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
                            self.test_report_fields["JOB_TIMESTAMP"]: job_timestamp,
                            self.test_report_fields["CRAWL_DATE"]: str(datetime.datetime.now())
                        }

                    # return the data
                    return compiled_data
                else:
                    return None

            else:
                print(f"Provided jenkins job [{jenkins_job_name}] does not exist")
                return None
        except requests.exceptions.HTTPError as e:
            print(f"There is a HTTP problem: \n {e}")
        except jenkins.NotFoundException as e:
            print(f"There is a 404 problem: \n {e}")
        except jenkins.JenkinsException as e:
            print(f"There is a Jenkins Exception problem: \n {e}")

    def __verify_jenkins_build_range(self, start: int = 1, end: int = 2):
        result = False
        # Both should be greater to 0
        if start >= 1 and end >= 1:
            result = True
        # start should less or equalTo end
        elif start <= end:
            result = True

        # return the verification result
        return result

    def __get_historical_test_reports_for_job_with_build_range(self, jenkins_job_name: str, start: int = 1, end: int = 2, depth: int = 0) -> any:
        """
            To fetch the latest test report for a jenkins job for a given build number.

            Usage:  obj.get_historical_test_reports_for_job_with_build_range('job1', 1, 2)
                    obj.get_historical_test_reports_for_job_with_build_range('job1', 1, 1)
                    obj.get_historical_test_reports_for_job_with_build_range('job1', 1, 2, 0)

            Output sample:
                        [
                            {
                                "jenkins_job_name": "FW-430/QAF_430_Test_Eclipse_Centos7x64_EN",
                                "jenkins_job_build_no": 26,
                                "jenkins_job_url": "https://jenkins.qac.perforce.com/abcd",
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
        # If job exist then fetch
        if self.__jenkins_job_does_exist(jenkins_job_name):

            # Verify the provided build range
            if self.__verify_jenkins_build_range(start, end):
                print(f"[JENKINS TEST REPORT FOR BUILD RANGE] Fetching for [{jenkins_job_name}] for range: ({start}-{end})...\n")

                # Loop for the given range
                for build_no in range(start, end+1):
                    # fetch job test report
                    data_retry_count = self.retry
                    data = self.__get_jenkins_job_test_report_data(jenkins_job_name, build_no, depth)

                    # Applying Retry, if data is null for the very first time
                    while not data and data_retry_count > 0:
                        print(f"[JENKINS TEST REPORT FOR BUILD RANGE] Retrying...")
                        data = self.__get_jenkins_job_test_report_data(jenkins_job_name, build_no, depth)
                        data_retry_count -= 1

                    # append into the final list
                    compiled_data.append(data)
                    print(f"")

                # return the collected data
                return compiled_data
            else:
                print(f"Provided jenkins job:'{jenkins_job_name}' build range({start}, {end}) is invalid;")
                return None
        else:
            print(f"Provided jenkins job [{jenkins_job_name}] does not exist")
            return None

            # ======================================================================
    # === [PUBLIC API] =====================================================
    # ======================================================================

    def write_to_file(self, data):
        with open(self.output_file, self.output_file_mode) as f:
            f.write(data)
            f.close()

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

    def get_all_test_reports_for_job(self, jenkins_job_name: str) -> any:
        print(f"[GET ALL TEST REPORT] Initiating...")
        # Fetch the job info
        job_info = self.__get_jenkins_job_info(jenkins_job_name)

        if job_info:
            # Fetch the first and last build no
            first_build_no = job_info["firstBuild"]["number"]
            last_build_no = job_info["lastBuild"]["number"]
            builds_no = [build["number"] for build in job_info["builds"]]
            print(f"[JENKINS BUILDS] Available Builds: => {builds_no}")

            # Fetch for the start and end build no
            return self.__get_historical_test_reports_for_job_with_build_range(jenkins_job_name, int(first_build_no), int(last_build_no))
        else:
            return None

    def get_latest_test_reports_for_job(self, jenkins_job_name: str) -> any:
        print(f"[GET LATEST TEST REPORT] Initiating...")
        # Fetch the job info
        job_info = self.__get_jenkins_job_info(jenkins_job_name)

        if job_info:
            # Fetch the latest build no
            latest_build_no = job_info["lastBuild"]["number"]

            # Fetch the result for the latest build no
            return self.__get_historical_test_reports_for_job_with_build_range(jenkins_job_name, int(latest_build_no), int(latest_build_no))
        else:
            return None

    def get_nth_test_report_for_job(self, jenkins_job_name: str, nth_build_no: int = 1) -> any:
        # Fetch the job info
        # Fetch the last build no
        # Loop for the start and end build no
        return self.__get_historical_test_reports_for_job_with_build_range(jenkins_job_name, nth_build_no, nth_build_no)


# ====[ CLI Execution ]======================
if __name__ == "__main__":

    print(f"[Jenkins Crawler] FROM CLI ...")
    # DATA
    # --------------
    jenkins_host_url = "https://jenkins.qac.perforce.com"  # "https://jenkins.qac.perforce.com"
    jenkins_username = 'amishra'
    jenkins_password = 'Me@here1'
    # This is access token
    # self.password = "11f9cada0ab7b05ef59afce3f260eba6c9"
    req_timeout = 60

    # TODO: Change the job/build streams or the full names as needed
    # Sample data for job names
    job_name = ["FW-430/QAF_430_Test_Eclipse_Win10x64_EN",
                "FW-430/QAF_430_Test_Eclipse_Centos7x64_EN",

                "FW-430/QAF_430_Test_GUI_Win11x64_EN_Regression",
                "FW-430/QAF_430_Test_GUI_Win11x64_EN_Sanity",
                "FW-430/QAF_430_Test_GUI_Win10x64_JP_Regression",
                "FW-430/QAF_430_Test_GUI_Win10x64_JP_sanity",

                "FW-430/QAF_430_Qacli_UI_Test_AdminAndUser_Win10x64",
                "FW-430/QAF_430_Qacli_UI_Test_AdminAndAdmin_Win11x64",

                "FW-430/Squish_VS2022_Win10x64_EN_Regression",
                "FW-430/Squish_VS2022_Win10x64_EN_Sanity",
                "FW-430/Squish_VS2019_Win10x64_EN_Regression",
                "FW-430/Squish_VS2019_Win10x64_EN_Sanity",

                "FW-430/VSCode_Win11_EN_Sanity",
                "FW-430/VSCode_Win10_EN_Sanity",
                ]
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
