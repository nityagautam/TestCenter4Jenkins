import datetime

from app.server.config.crawler_configurations import CrawlerConfig
from app.server.crawlers.crawl_jenkins import CrawlJenkins
from app.server.dbase.DBAccess import DBAccess


class Crawler(CrawlerConfig):
    def __init__(self):
        # 1- Initiate the DB Connection
        self.db_obj = DBAccess()

        # 2- Jenkins crawler object
        self.stdout = ""
        self.stderr = ""
        self.jenkins_crawler = None

    def run(self):
        start_time = datetime.datetime.now()
        try:
            # Set the flags
            CrawlerConfig.crawler_status = "Running"
            self.stdout += f"\n[Crawler] Initiating ..."
            print(f"\n\n|`Initiating Crawler`\\{'_' * 80}\n|")
            # 1-Get the project list with URL, Credentials, job name
            active_projects = self.db_obj.get_active_project_list()
            project_list = [item[1] for item in active_projects]
            self.stdout += f"\n[Crawler] Active project List: {project_list}"

            # 2- if projects are not there then say this
            if len(active_projects) == 0:
                # self.db_obj.insert_some_prefix_data()
                # fetch again
                # active_projects = self.db_obj.get_active_project_list()
                self.stdout += f"\n[Crawler] No Active project found."
                print(f"| No Active project found.")

            else:
                # Log the project lists
                print(f"| Active project List: ")
                for project_name in project_list:
                    print(f"|  - {project_name}")

                # 3- loop for the active projects, (fetch and write)
                for records in active_projects:
                    # 3.0 - Fetch from records
                    project_id = records[0]
                    project_name = records[1]
                    data_source = records[2]
                    jenkins_job_name = records[3]
                    jenkins_url = records[4]
                    jenkins_username = records[5]
                    jenkins_password = records[6]

                    # Log
                    print(f"|\n"
                          f"|{'_' * 100}\n|\n"
                          f"| For Project: {project_name}")

                    # 3.1 - See, if the project data source is jenkins
                    if str(data_source).lower() in ["jenkins"]:
                        pass

                        # 3.1.1 - Initiate the jenkins connection with project credentials
                        print(f"| Starting for project:{project_name} with creds: ({jenkins_username}:{jenkins_password})")
                        self.stdout += f"\n[Crawler] Starting for project:{project_name} with creds: ({jenkins_username}:{jenkins_password})"
                        self.jenkins_crawler = CrawlJenkins(jenkins_url,
                                                            jenkins_username,
                                                            jenkins_password,
                                                            self.req_timeout)
                        self.jenkins_crawler.connect()

                        # 3.1.2 - to fetch the data
                        print(f"| Fetching data for project:{project_name} Job: {jenkins_job_name}... ")
                        output = self.jenkins_crawler.get_all_test_reports_for_job(jenkins_job_name)

                        # 3.1.3 - to write the data
                        if output:
                            # 3.3.1 - Write data to db
                            print(f"| Writing data into DB for project:{project_name}... ")
                            self.db_obj.add_execution_data(output, project_id, project_name, data_source="Jenkins")
                    else:
                        print(f"| Data source is not jenkins, moving on ...\n|")

            # 4- Close the db connection now
            self.db_obj.disconnect()

            # 5- Calculate execution time
            end_time = datetime.datetime.now()
            print(f'\n'
                  f'+--[Crawler]{"-" * 25}+\n'
                  f'| Process completed successfully.    |\n'
                  f'| Time taken: {end_time - start_time} \n'
                  f'+--{"-" * 34}+\n')

        except Exception as e:
            # Log the exception
            # 5- Calculate execution time
            end_time = datetime.datetime.now()
            print(f'\n'
                  f'+--[Crawler Error]{"-" * 30}+\n'
                  f'| Process failed; \n'
                  f'| Time taken: {end_time - start_time} \n'
                  f'+--{"-" * 45}+\n')
        finally:
            # 6- Set the flags
            CrawlerConfig.crawler_status = "Not Running"


if __name__ == "__main__":
    obj = Crawler()
    obj.run()
