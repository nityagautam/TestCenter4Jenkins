import datetime

from app.server.config.jenkins_configurations import JenkinsConfig
from app.server.crawlers.crawl_jenkins import CrawlJenkins
from app.server.dbase.DBAccess import DBAccess


class Crawler(JenkinsConfig):
    def __init__(self):
        # 1- Initiate the DB Connection
        self.db_obj = DBAccess()

        # 2- Initiate the Jenkins crawler
        self.jenkins_crawler = (CrawlJenkins(self.jenkins_host_url,
                                             self.jenkins_username,
                                             self.jenkins_password,
                                             self.req_timeout)
                                .connect())

    def run(self):
        print(f"\n[Crawler] Initiating ... \n")
        # 1-Get the project list with URL, Credentials, job name
        active_projects = self.db_obj.get_active_project_list()
        print(f"Active project List: {active_projects}")

        # 2- if projects are not there then add initial
        if len(active_projects) == 0:
            self.db_obj.insert_some_prefix_data()
            # fetch again
            active_projects = self.db_obj.get_active_project_list()
            print(f"Active project List: {active_projects}")

        # 2-loop for the active projects,
        for records in active_projects:
            # 3.0 - Fetch from records
            project_id = records[0]
            project_name = records[1]
            job_name = records[3]

            # 3.1 - to fetch the data
            print(f"[Crawler] Fetching data for project:{project_name} Job: {job_name}... ")
            out = self.jenkins_crawler.get_all_test_reports_for_job(job_name)

            # 3.2 - to write the data
            if out:
                print(f"[Crawler] Writing data into DB for project:{project_name}... ")
                self.db_obj.set_execution_data_from_jenkins(out, project_id, project_name)

        print(f"[Crawler] Process completed.\n")

        # Close the db connection now
        self.db_obj.disconnect()


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    obj = Crawler()
    obj.run()
    end_time = datetime.datetime.now()
    print(f"[Crawler] Process Completed; \n[Crawler] Time taken: {end_time - start_time} sec")
