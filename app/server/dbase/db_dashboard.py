import datetime

from app.server.config.db_configurations import DBConfig
from app.server.config.configurations import Configurations
from app.server.dbase.db_engine import DatabaseObject


class Dashboard(Configurations):
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

    def get_latest_data_for_dashboard(self):
        # obj.select_where('sqlite_master', 'name', name="'users'")
        # print("SQLITE TABLES:", obj.fetch_result_from_cursor())
        # ==> SELECT select_list FROM table ORDER BY column_1 ASC, column_2 DESC;

        # ==> Insert some data in to projects
        #self.db_obj.insert(self.project_table, project_id=1, project_name="Helix-QAC Eclipse Plugin", data_source='Jenkins', jenkins_url='http://localhost:8080', jenkins_user='NIL', jenkins_password='NIL', status='active', created=datetime.datetime.now(), last_modified=datetime.datetime.now())

        # ==> Insert more data in to execution
        self.db_obj.insert(self.test_execution_table, project_id=1, project_name="Helix-QAC Eclipse Plugin", test_results='{"pass": 100, "fail": 20, "error": 5, "skipped": 0}', source="XML", source_value="XML_file_PATH", execution_date=datetime.datetime.now(), crawled_date=datetime.datetime.now())
        self.db_obj.insert(self.test_execution_table, project_id=2, project_name="Helix QAC VS Code Plugin", test_results='{"pass": 100, "fail": 20, "error": 5, "skipped": 0}', source="XML", source_value="XML_file_PATH", execution_date=datetime.datetime.now(), crawled_date=datetime.datetime.now())
        self.db_obj.insert(self.test_execution_table, project_id=3, project_name="Helix QAC Dashboard", test_results='{"pass": 100, "fail": 20, "error": 5, "skipped": 0}', source="XML", source_value="XML_file_PATH", execution_date=datetime.datetime.now(), crawled_date=datetime.datetime.now())
        self.db_obj.insert(self.test_execution_table, project_id=4, project_name="Validate Portal UI", test_results='{"pass": 100, "fail": 20, "error": 5, "skipped": 0}', source="XML", source_value="XML_file_PATH", execution_date=datetime.datetime.now(), crawled_date=datetime.datetime.now())
        self.db_obj.insert(self.test_execution_table, project_id=5, project_name="Multi-Engine Parser", test_results='{"pass": 100, "fail": 20, "error": 5, "skipped": 0}', source="XML", source_value="XML_file_PATH", execution_date=datetime.datetime.now(), crawled_date=datetime.datetime.now())
        self.db_obj.insert(self.test_execution_table, project_id=6, project_name="klocwork Server", test_results='{"pass": 100, "fail": 20, "error": 5, "skipped": 0}', source="XML", source_value="XML_file_PATH", execution_date=datetime.datetime.now(), crawled_date=datetime.datetime.now())
        self.db_obj.insert(self.test_execution_table, project_id=7, project_name="Project Theta-5", test_results='{"pass": 100, "fail": 20, "error": 5, "skipped": 0}', source="XML", source_value="XML_file_PATH", execution_date=datetime.datetime.now(), crawled_date=datetime.datetime.now())
        self.db_obj.insert(self.test_execution_table, project_id=1, project_name="Helix-QAC Eclipse Plugin", test_results='{"pass": 100, "fail": 20, "error": 5, "skipped": 0}', source="XML", source_value="XML_file_PATH", execution_date=datetime.datetime.now(), crawled_date=datetime.datetime.now())
        self.db_obj.insert(self.test_execution_table, project_id=1, project_name="Helix-QAC Eclipse Plugin", test_results='{"pass": 100, "fail": 20, "error": 5, "skipped": 0}', source="XML", source_value="XML_file_PATH", execution_date=datetime.datetime.now(), crawled_date=datetime.datetime.now())
        self.db_obj.insert(self.test_execution_table, project_id=1, project_name="Helix-QAC Eclipse Plugin", test_results='{"pass": 100, "fail": 20, "error": 5, "skipped": 0}', source="XML", source_value="XML_file_PATH", execution_date=datetime.datetime.now(), crawled_date=datetime.datetime.now())

        # Approach
        # -----------
        # 1- Get all projects from projects table
        # 2- Get all the latest data (without duplicate project) from executions table
        #   - (it means: Get the latest execution for a given project based on latest crawled time)
        #   - (SAMPLE QUERY: SELECT * FROM execution GROUP BY project_name ORDER BY MAX(crawled_date))
        # 3- Filter-In the records
        #   - if projects status is active
        #   - If project from executions table does exist in the 'projects' record
        #   - If record from executions has the valid data for its 'test_results' column
        # 4- Return the filtered data

        # Step-1
        self.db_obj.select(self.project_table, "*")
        project_lst = self.db_obj.fetch_result_from_cursor()

        # Step-2 (Need to execute custom query)
        self.db_obj.execute_custom_query("SELECT project_name, test_results, execution_date, crawled_date FROM executions GROUP BY project_name ORDER BY MAX(crawled_date)")
        test_executions_lst = self.db_obj.fetch_result_from_cursor()

        # Step-3
        project_names_with_active_status = [project_record for project_record in project_lst]
        active_project_lst = [rec[1] for rec in project_names_with_active_status if str(rec[6]).lower() == 'active']
        print(f"==> Active Project List: ", active_project_lst)

        final_records = []
        for execution_record in test_executions_lst:
            print(f"ASSERTION: PRJ_NAME[EXE]: {execution_record[1]} with list {active_project_lst}")
            if execution_record[1] in active_project_lst:
                final_records.append(execution_record)

        # Step-4
        print("Data for Dashboard =====> ", final_records)
        return final_records

    def __parse_data(self, data):
        return self.db_obj


if __name__ == "__main__":
    o = Dashboard()
    o.get_latest_data_for_dashboard()

