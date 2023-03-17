import datetime
import json
import random

from app.server.config.db_configurations import DBConfig
from app.server.config.configurations import Configurations
from app.server.dbase.db_engine import DatabaseObject


class DBData(Configurations):
    def __init__(self):
        # Initialize the DB file for data source
        self.db_obj = DatabaseObject(DBConfig.db_file[Configurations.APP_ENVIRONMENT])

        # basic tables and its schema
        self.project_table = DBConfig.PROJECT_TABLE
        self.project_table_fields = DBConfig.PROJECT_TABLE_FIELDS
        self.test_execution_table = DBConfig.TEST_EXECUTION_TABLE
        self.test_execution_table_fields = DBConfig.TEST_EXECUTION_TABLE_FIELDS

        # Create the table (if they don't exist)
        self.db_obj.create_table(self.project_table, self.project_table_fields)
        self.db_obj.create_table(self.test_execution_table, self.test_execution_table_fields)

        # Create some dummy records
        self.__insert_some_dummy_data()

    # ------------------------------------------------------------------------
    # Methods specific to the pages
    # ------------------------------------------------------------------------

    def get_overview_data(self):
        # We are going to give
        # --------------------------------------
        # - projects list (no of projs, active/archived)
        # - no of execution
        # - pass rate
        # - apply filter to have active projects only
        # - the latest project executions history (each active project with the latest crawled date)
        # -
        return {}

    def get_dashboard_data(self):
        # We are going to give
        # --------------------------------------
        # - latest test executions data based on the crawled data for distinct project
        # - apply filter to have active projects only

        # Now in Action
        # ---------------
        dashboard_data = self.filter_test_executions_data_for_active_projects(
            self.get_latest_crawled_test_executions_data_for_distinct_projects())
        print("\n\nData for Dashboard =====> ", dashboard_data)
        return self.__parse_data_to_dict(DBConfig.DATA_PARSING_TYPES["FOR_DASHBOARD"], dashboard_data)

    # ------------------------------------------------------------------------
    # Methods for Internal usage
    # ------------------------------------------------------------------------

    def get_projects_list(self):
        self.db_obj.select(self.project_table, "*")
        return self.db_obj.fetch_result_from_cursor()

    def get_active_project_list(self):
        self.db_obj.select_where(self.project_table, "*", status="'active'")
        return self.db_obj.fetch_result_from_cursor()

    def get_test_executions_data(self):
        self.db_obj.select(self.test_execution_table, "*")
        return self.db_obj.fetch_result_from_cursor()

    def get_test_executions_data_for_project(self, project_name):
        self.db_obj.select_where(self.test_execution_table, "*", project_name=project_name)
        return self.db_obj.fetch_result_from_cursor()

    def get_latest_crawled_test_executions_data_for_distinct_projects(self):
        self.db_obj.execute_custom_query(
            DBConfig.CUSTOM_QUERIES["LATEST_CRAWLED_TEST_EXECUTIONS_DATA_FOR_DISTINCT_PROJECTS"])
        return self.db_obj.fetch_result_from_cursor()

    def get_oldest_crawled_test_executions_data_for_distinct_projects(self):
        self.db_obj.execute_custom_query(
            DBConfig.CUSTOM_QUERIES["OLDEST_CRAWLED_TEST_EXECUTIONS_DATA_FOR_DISTINCT_PROJECTS"])
        return self.db_obj.fetch_result_from_cursor()

    def filter_test_executions_data_for_active_projects(self, test_executions_data):
        # step-1: Get active project list
        active_project_list = self.get_active_project_list()

        # step-2: match, and apply filter against project name in test_execution_data
        tmp_lst_for_active_projects = [project_record[1] for project_record in active_project_list]
        final_filtered_result = [execution_record for execution_record in test_executions_data if execution_record[1] in tmp_lst_for_active_projects]
        return final_filtered_result

    @staticmethod
    def __parse_data_to_dict(parse_for: str, data: any) -> any:
        # trim the 'executions' data, and convert it to json
        parsed_data_obj = []
        if parse_for == 'executions':
            for item in data:
                # Preparing dict data to be appended in the list
                # This format(keys) are going to be used in the templates directly.
                parsed_data_obj.append({"project_id": item[0], "project_name": item[1], "test_result": json.loads(item[2]), "source": item[3], "execution_date": item[5], "report_date": item[5], "crawled_date": item[6]})
        else:
            # TODO: Add more parsing for history trends, etc
            pass

        # now, return the parsed obj
        # DEBUG: print(f"JOSN DUMPS: {json.dumps(parsed_data_obj)}")
        return parsed_data_obj

    # ---------------------------------------------------------------------------------------------
    # DUMMY DATA CREATION
    # ---------------------------------------------------------------------------------------------

    def __insert_some_dummy_data(self):

        # ==> Insert some data in to "projects" table
        # ---------------------------------------------------------------------------------------------
        # self.db_obj.insert(self.project_table, project_id=1, project_name="Helix-QAC Eclipse Plugin", data_source='Jenkins', jenkins_url='http://localhost:8080', jenkins_user='NIL', jenkins_password='NIL', status='active', created=datetime.datetime.now(), last_modified=datetime.datetime.now())
        # self.db_obj.insert(self.project_table, project_id=2, project_name="Helix-QAC VSCode Plugin", data_source='XML', jenkins_url='NIL', jenkins_user='NIL', jenkins_password='NIL', status='active', created=datetime.datetime.now(), last_modified=datetime.datetime.now())
        # self.db_obj.insert(self.project_table, project_id=3, project_name="Helix-QAC VisualStudio Plugin", data_source='XML', jenkins_url='NIL', jenkins_user='NIL', jenkins_password='NIL', status='active', created=datetime.datetime.now(), last_modified=datetime.datetime.now())
        # self.db_obj.insert(self.project_table, project_id=4, project_name="Helix-QAC QACLI", data_source='XML', jenkins_url='NIL', jenkins_user='NIL', jenkins_password='NIL', status='active', created=datetime.datetime.now(), last_modified=datetime.datetime.now())
        # self.db_obj.insert(self.project_table, project_id=5, project_name="Validate CLI", data_source='XML', jenkins_url='NIL', jenkins_user='NIL', jenkins_password='NIL', status='active', created=datetime.datetime.now(), last_modified=datetime.datetime.now())
        # self.db_obj.insert(self.project_table, project_id=6, project_name="Validate Portal UI", data_source='XML', jenkins_url='NIL', jenkins_user='NIL', jenkins_password='NIL', status='active', created=datetime.datetime.now(),last_modified=datetime.datetime.now())
        # self.db_obj.insert(self.project_table, project_id=7, project_name="Helix-QAC Dashboard", data_source='XML', jenkins_url='NIL', jenkins_user='NIL',jenkins_password='NIL', status='active', created=datetime.datetime.now(), last_modified=datetime.datetime.now())
        #
        # # Update a project as an archived project where project_name is given
        # # ---------------------------------------------------------------------------------------------
        # self.db_obj.update_where(self.project_table, {"status": "archived"}, project_name="Helix-QAC Dashboard")

        # ==> Insert more data in to "executions" table
        # ---------------------------------------------------------------------------------------------
        self.db_obj.insert(self.test_execution_table, project_id=1, project_name="Helix-QAC Eclipse Plugin", test_results='{"pass": '+str(random.randrange(10, 200))+', "fail": '+str(random.randrange(10, 200))+', "error": '+str(random.randrange(10, 200))+', "skipped": '+str(random.randrange(10, 200))+'}', source="XML", source_value="XML_file_PATH", execution_date=datetime.datetime.now(), crawled_date=datetime.datetime.now())
        self.db_obj.insert(self.test_execution_table, project_id=2, project_name="Helix-QAC VSCode Plugin", test_results='{"pass": '+str(random.randrange(10, 200))+', "fail": '+str(random.randrange(10, 200))+', "error": '+str(random.randrange(10, 200))+', "skipped": '+str(random.randrange(10, 200))+'}', source="XML", source_value="XML_file_PATH", execution_date=datetime.datetime.now(), crawled_date=datetime.datetime.now())
        self.db_obj.insert(self.test_execution_table, project_id=3, project_name="Helix-QAC VisualStudio Plugin", test_results='{"pass": '+str(random.randrange(10, 200))+', "fail": '+str(random.randrange(10, 200))+', "error": '+str(random.randrange(10, 200))+', "skipped": '+str(random.randrange(10, 200))+'}', source="XML", source_value="XML_file_PATH", execution_date=datetime.datetime.now(), crawled_date=datetime.datetime.now())
        self.db_obj.insert(self.test_execution_table, project_id=4, project_name="Helix-QAC QACLI", test_results='{"pass": '+str(random.randrange(10, 200))+', "fail": '+str(random.randrange(10, 200))+', "error": '+str(random.randrange(10, 200))+', "skipped": '+str(random.randrange(10, 200))+'}', source="XML", source_value="XML_file_PATH", execution_date=datetime.datetime.now(), crawled_date=datetime.datetime.now())
        self.db_obj.insert(self.test_execution_table, project_id=5, project_name="Validate CLI", test_results='{"pass": '+str(random.randrange(10, 200))+', "fail": '+str(random.randrange(10, 200))+', "error": '+str(random.randrange(10, 200))+', "skipped": '+str(random.randrange(10, 200))+'}', source="XML", source_value="XML_file_PATH", execution_date=datetime.datetime.now(), crawled_date=datetime.datetime.now())
        self.db_obj.insert(self.test_execution_table, project_id=6, project_name="Validate Portal UI", test_results='{"pass": '+str(random.randrange(10, 200))+', "fail": '+str(random.randrange(10, 200))+', "error": '+str(random.randrange(10, 200))+', "skipped": '+str(random.randrange(10, 200))+'}', source="XML", source_value="XML_file_PATH", execution_date=datetime.datetime.now(), crawled_date=datetime.datetime.now())
        self.db_obj.insert(self.test_execution_table, project_id=7, project_name="Helix-QAC Dashboard", test_results='{"pass": '+str(random.randrange(10, 200))+', "fail": '+str(random.randrange(10, 200))+', "error": '+str(random.randrange(10, 200))+', "skipped": '+str(random.randrange(10, 200))+'}', source="XML", source_value="XML_file_PATH", execution_date=datetime.datetime.now(), crawled_date=datetime.datetime.now())
        self.db_obj.insert(self.test_execution_table, project_id=8, project_name="Alpha-1", test_results='{"pass": '+str(random.randrange(10, 200))+', "fail": '+str(random.randrange(10, 200))+', "error": '+str(random.randrange(10, 200))+', "skipped": '+str(random.randrange(10, 200))+'}', source="XML", source_value="XML_file_PATH", execution_date=datetime.datetime.now(), crawled_date=datetime.datetime.now())
        self.db_obj.insert(self.test_execution_table, project_id=9, project_name="Beta-1", test_results='{"pass": '+str(random.randrange(10, 200))+', "fail": '+str(random.randrange(10, 200))+', "error": '+str(random.randrange(10, 200))+', "skipped": '+str(random.randrange(10, 200))+'}', source="XML", source_value="XML_file_PATH", execution_date=datetime.datetime.now(), crawled_date=datetime.datetime.now())


# ------------------
# For CLI Execution
# ------------------
if __name__ == "__main__":
    o = DBData()
    o.get_dashboard_data()

