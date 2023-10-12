import datetime
import json
from app.server.config.db_configurations import DBConfig
from app.server.config.configurations import Configurations
from app.server.dbase.DBEngine import DBEngine


class DBAccess(Configurations):
    def __init__(self):
        # Initialize the DB file for data source
        self.db_obj = DBEngine(DBConfig.db_file[Configurations.APP_ENVIRONMENT])
        # self.db_obj = DBEngine("data.db")

        # basic tables and its schema
        # 1- for users table
        self.user_table = DBConfig.USER_TABLE
        self.user_table_fields = DBConfig.USER_TABLE_FILED
        # 2- for projects table
        self.project_table = DBConfig.PROJECT_TABLE
        self.project_table_fields = DBConfig.PROJECT_TABLE_FIELDS
        # 3- for executions table
        self.test_execution_table = DBConfig.TEST_EXECUTION_TABLE
        self.test_execution_table_fields = DBConfig.TEST_EXECUTION_TABLE_FIELDS

        # Create the table (if they don't exist)
        # 1- For users table
        self.db_obj.create_table(self.user_table, self.user_table_fields)
        # 2- For projects table
        self.db_obj.create_table(self.project_table, self.project_table_fields)
        # 3- For executions table
        self.db_obj.create_table(self.test_execution_table, self.test_execution_table_fields)

        # Add Default users, if no user found
        if self.get_users_count() == 0:
            self.db_obj.insert(self.user_table, username='root', password='root', created=datetime.datetime.now())
            self.db_obj.insert(self.user_table, username='admin', password='admin', created=datetime.datetime.now())
            self.db_obj.insert(self.user_table, username='test', password='password', created=datetime.datetime.now())

        # Create some dummy records
        # self.insert_some_prefix_data()

        # Load User list
        self.users = {}
        self.fetch_users()

    def disconnect(self):
        self.db_obj.disconnect()

    # -----------------------------------
    # API for the 'users' table
    # -----------------------------------
    def get_user(self, username: str):
        pass

    def get_users(self):
        pass

    def create_user(self, email: str, username: str, password: str, role: str):
        pass

    def delete_user(self, username: str):
        pass

    def get_users_count(self):
        self.db_obj.select(self.user_table, "COUNT(1)")
        user_count = self.db_obj.fetch_result_from_cursor()[0][0]
        # print(f"Total users: {user_count}")
        return user_count

    def fetch_users(self):
        if not self.users:
            cursor = self.db_obj.select(self.user_table, "*")
            for user in cursor.fetchall():
                # print(f"[DBAccess] Entry User: {user}")
                self.users[user[1]] = user[2]
            # print(f"==> Prepared list of users: {self.users}")
        return self.users

    def authenticate(self, username, password):
        if len(self.users) < 1:
            # Load the users from db
            self.fetch_users()
        # Verify the user from users dictionary
        return True if self.users.get(username) == password else False

    # -----------------------------------
    # API for the 'settings' table
    # -----------------------------------
    def get_setting(self, column_name: str):
        pass

    def get_settings(self):
        pass

    def update_setting(self, column_name: str, value: str):
        pass

    # -----------------------------------
    # API for the 'projects' table
    # -----------------------------------
    def add_project(self, data, check_duplicate: bool = True):
        # - Insert data in to "executions" table from the jenkins crawler (for DS, see crawl_jenkins.py)
        if data:

            # 1- Verify if project name already exists
            if check_duplicate:
                query = f"SELECT * FROM {self.project_table} WHERE project_name='{data['project_name']}' LIMIT 1"
                self.db_obj.execute_query(query)
                query_res = self.db_obj.fetch_result_from_cursor()

                if len(query_res) > 0:
                    print(f"[WRITE PROJECT TO DB] Seems like project name already exists in DB: \n {query_res} ")
                    return False

            # 2- Insert the data for creation of new project
            self.db_obj.insert(self.project_table,
                               project_name=data["project_name"],
                               data_source=data["data_source"],
                               jenkins_job_name=data["jenkins_job_name"],
                               jenkins_url=data["jenkins_url"],
                               jenkins_user=data["jenkins_user"],
                               jenkins_password=data["jenkins_password"],
                               status='active',
                               tags=data["tags"],
                               created=datetime.datetime.now(),
                               last_modified=datetime.datetime.now()
                               )
            return True

    def get_projects_list(self):
        self.db_obj.select(self.project_table, "*")
        return self.db_obj.fetch_result_from_cursor()

    def get_projects_count(self):
        print("\n Inserting dummy projects ...")
        self.db_obj.select(self.project_table, "COUNT(1)")
        projects_count = self.db_obj.fetch_result_from_cursor()[0][0]
        print("Project count: {projects_count}")
        return projects_count

    def get_active_project_list(self):
        self.db_obj.select_where(self.project_table, "*", status="'active'")
        return self.db_obj.fetch_result_from_cursor()

    def set_project_as_active(self, project_name: str = ""):
        self.db_obj.update_where(self.project_table, {"status": "active"}, project_name=project_name)
        # print(self.db_obj.fetch_result_from_cursor())
        return True

    def set_project_as_archived(self, project_name: str = ""):
        self.db_obj.update_where(self.project_table, {"status": "archived"}, project_name=project_name)
        # print(self.db_obj.fetch_result_from_cursor())
        return True

    def delete_project(self, project_name: str = ""):
        self.db_obj.delete(self.project_table, project_name=project_name)
        # print(self.db_obj.fetch_result_from_cursor())
        return True

    # -----------------------------------
    # API for the 'executions' table
    # -----------------------------------
    def add_execution_data(self, data, project_id, project_name, data_source: str = "Jenkins"):
        # ==> Insert data in to "executions" table from the jenkins crawler (for DS, see crawl_jenkins.py)
        for execution_data in data:
            if execution_data:
                self.db_obj.insert(self.test_execution_table,
                                   project_id=project_id,
                                   project_name=project_name,
                                   jenkins_job_name=execution_data["jenkins_job_name"],
                                   jenkins_job_build_no=execution_data["jenkins_job_build_no"],
                                   jenkins_job_build_url=execution_data["jenkins_job_build_url"],
                                   duration_in_sec=execution_data["duration_in_sec"],
                                   suite_names=", ".join(execution_data["suite_names"]),
                                   test_result='{"pass_count": ' + str(execution_data["test_result"]["pass_count"]) +
                                               ', "fail_count": ' + str(execution_data["test_result"]["fail_count"]) +
                                               ', "skip_count": ' + str(execution_data["test_result"]["skip_count"]) + '}',
                                   data_source=data_source,
                                   tags=execution_data["tags"],
                                   jenkins_job_build_timestamp=execution_data["jenkins_job_build_timestamp"],
                                   crawled_date=execution_data["crawled_date"]
                                   )

    def get_test_executions_data(self):
        self.db_obj.select(self.test_execution_table, "*")
        return self.db_obj.fetch_result_from_cursor()

    def get_builds_from_execution_data(self, jenkins_job_name):
        query = f"SELECT jenkins_job_build_no FROM executions WHERE jenkins_job_name='{jenkins_job_name}'"
        self.db_obj.execute_query(query)
        data = self.db_obj.fetch_result_from_cursor()
        return data

    def get_test_executions_data_count(self):
        self.db_obj.select(self.test_execution_table, "COUNT")
        return self.db_obj.fetch_result_from_cursor()

    def get_test_executions_data_for_active_project(self):
        self.db_obj.select(self.test_execution_table, "*")
        return self.filter_test_executions_data_for_active_projects(self.db_obj.fetch_result_from_cursor())

    def get_test_executions_data_for_project(self, project_name):
        # self.db_obj.select_where_with_limit(self.test_execution_table, '30', "*", project_name=project_name)
        self.db_obj.select_where_with_limit_and_desc_order_by(self.test_execution_table,
                                                              '30',
                                                              'jenkins_job_build_timestamp',
                                                              "*",
                                                              project_name=project_name)
        return self.db_obj.fetch_result_from_cursor()

    def get_latest_crawled_test_executions_data_for_distinct_projects(self):
        self.db_obj.execute_query(
            DBConfig.CUSTOM_QUERIES["LATEST_CRAWLED_TEST_EXECUTIONS_DATA_FOR_DISTINCT_PROJECTS"])
        return self.db_obj.fetch_result_from_cursor()

    def get_oldest_crawled_test_executions_data_for_distinct_projects(self):
        self.db_obj.execute_query(
            DBConfig.CUSTOM_QUERIES["OLDEST_CRAWLED_TEST_EXECUTIONS_DATA_FOR_DISTINCT_PROJECTS"])
        return self.db_obj.fetch_result_from_cursor()

    def filter_test_executions_data_for_active_projects(self, test_executions_data):
        # step-1: Get active project list
        active_project_list = self.get_active_project_list()

        # step-2: match, and apply filter against project name in test_execution_data
        tmp_lst_for_active_projects = [project_record[1] for project_record in active_project_list]
        final_filtered_result = [execution_record for execution_record in test_executions_data if
                                 execution_record[1] in tmp_lst_for_active_projects]
        return final_filtered_result

    # -----------------------------------
    # API for the Various pages
    # -----------------------------------

    def get_overview_data(self):
        # Data for the overview/index page
        # --------------------------------------

        # For Projects
        projects_list = self.get_projects_list()
        total_projects_count = len(projects_list)
        active_projects_count = len(self.get_active_project_list())
        archived_projects_count = total_projects_count - active_projects_count

        # For Executions
        executions_data = self.get_test_executions_data()
        # execution_data_for_active_projects = self.get_test_executions_data_for_active_project()
        # total_executions_for_active_projects = len(execution_data_for_active_projects)
        execution_data_for_active_projects_with_latest_crawled_date = self.__parse_data_to_dict(
            DBConfig.DATA_PARSING_FOR_TABLE["EXECUTIONS"], self.filter_test_executions_data_for_active_projects(
                self.get_latest_crawled_test_executions_data_for_distinct_projects()))

        # For TC: From the latest Executions
        total_tc, passed, failed, error, skipped = 0, 0, 0, 0, 0
        for record in execution_data_for_active_projects_with_latest_crawled_date:
            # test_result
            total_tc += record['test_result']['pass_count'] + record['test_result']['fail_count'] + \
                        record['test_result']['skip_count']
            passed += record['test_result']['pass_count']
            failed += record['test_result']['fail_count']
            skipped += record['test_result']['skip_count']
            error += 0

        # Defining schema for overview data (for HTML Templates)
        # And setting the value as well
        overview_data = {
            "PROJECTS_LIST": self.__parse_data_to_dict(DBConfig.DATA_PARSING_FOR_TABLE["PROJECTS"], projects_list),
            "TOTAL_PROJECTS_COUNT": total_projects_count,
            "TOTAL_ACTIVE_PROJECTS": active_projects_count,
            "TOTAL_ARCHIVED_PROJECTS": archived_projects_count,

            "TOTAL_EXECUTIONS_COUNT": len(executions_data),
            "LATEST_EXECUTION_FOR_ACTIVE_PROJECTS": execution_data_for_active_projects_with_latest_crawled_date,

            "TOTAL_TESTCASES_FROM_LATEST_EXECUTIONS": total_tc,
            "TC_PASSED_FROM_LATEST_EXECUTIONS": passed,
            "TC_FAILED_FROM_LATEST_EXECUTIONS": failed,
            "TC_ERROR_FROM_LATEST_EXECUTIONS": error,
            "TC_SKIPPED_FROM_LATEST_EXECUTIONS": skipped}
        return overview_data

    def get_dashboard_data(self):
        # We are going to give
        # --------------------------------------
        # - latest test executions data based on the crawled data for distinct project
        # - apply filter to have active projects only

        # Now in Action
        # ---------------
        dashboard_data = self.filter_test_executions_data_for_active_projects(
            self.get_latest_crawled_test_executions_data_for_distinct_projects())
        # print("\n\nData for Dashboard =====> ", dashboard_data)
        return self.__parse_data_to_dict(DBConfig.DATA_PARSING_FOR_TABLE["EXECUTIONS"], dashboard_data)

    def get_history_data(self):
        # We are going to give
        # --------------------------------------
        # - from executions, history for each project
        history_data = {}
        for project_record in self.get_projects_list():
            project_name = project_record[1]
            history_data[project_name] = self.__parse_data_to_dict(
                DBConfig.DATA_PARSING_FOR_TABLE["EXECUTIONS"],
                self.get_test_executions_data_for_project("'" + project_name + "'")
            )
            # print("\n\n====>\n", history_data[project_name])

        # Return the history data
        return history_data

    # -----------------------------------
    # API for the internal usage
    # -----------------------------------

    @staticmethod
    def __parse_data_to_dict(parse_for_table: str, data: any) -> any:
        # trim the 'executions' data, and convert it to json
        parsed_data_obj = []
        if parse_for_table == 'executions':
            for item in data:
                # Preparing dict data to be appended in the list
                # SCHEMA: check the db_configurations for 'executions' table
                # print("\n\n===> EXECUTION RECORD: ", item)
                parsed_data_obj.append(
                    {
                        "project_id": item[0],
                        "project_name": item[1],
                        "jenkins_job_name": item[2],
                        "jenkins_job_build_no": item[3],
                        "jenkins_job_build_url": item[4],
                        "duration_in_sec": item[5],
                        "suite_names": item[6],
                        "test_result": json.loads(item[7]),
                        "source": item[8],
                        "tags": item[9],
                        "jenkins_job_build_timestamp": item[10],
                        "crawled_date": item[11],
                    }
                )
        elif parse_for_table == 'projects':
            for item in data:
                # Preparing dict data to be appended in the list
                # SCHEMA: check the db_configurations for 'projects' table
                # print("\n\n===> PROJECT RECORD: ", item)
                parsed_data_obj.append(
                    {
                        "PROJECT_ID": item[0],
                        "PROJECT_NAME": item[1],
                        "DATA_SOURCE": item[2],
                        "JENKINS_JOB_NAME": item[3],
                        "JENKINS_URL": item[4],
                        "JENKINS_USER": item[5],
                        "JENKINS_PASSWORD": item[6],
                        "STATUS": item[7],
                        "TAGS": item[8],
                        "CREATED": item[9],
                        "LAST_MODIFIED": item[10]
                    }
                )
        else:
            # if table not recognised then return the given data
            return data

        # now, return the parsed obj
        # DEBUG: print(f"JOSN DUMPS: {json.dumps(parsed_data_obj)}")
        return parsed_data_obj

    # ---------------------------------------------------------------------------------------------
    # DUMMY DATA CREATION
    # ---------------------------------------------------------------------------------------------
    # # Update a project as an archived project where project_name is given
    # # ---------------------------------------------------------------------------------------------
    # self.db_obj.update_where(self.project_table, {"status": "archived"}, project_name="Validate CLI")
    # self.db_obj.update_where(self.project_table, {"status": "active"}, project_name="Helix-QAC Dashboard")


# ------------------
# For CLI Execution
# ------------------
if __name__ == "__main__":
    print("\n Running from terminal ... \n ")
    o = DBAccess()
    print("\n\n", o.get_dashboard_data())
    # o.insert_some_prefix_data()
