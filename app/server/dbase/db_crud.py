import datetime

from app.server.config.db_config import DBConfig
from app.server.dbase.db_engine import DatabaseObject


class CRUD:
    def __init__(self, db_file, table_name, table_fields):
        # Initialize the DB file
        self.db_obj = DatabaseObject(db_file)

        # Creation begins
        # Create Projects table, if not exist
        self.table_name = table_name
        self.table_fields = table_fields
        self.db_obj.create_table(table_name, table_fields)


class Users(CRUD):
    def __init__(self):
        super(Users, self).__init__(DBConfig.db_file["TEST"], DBConfig.USER_TABLE, DBConfig.USER_TABLE_FILED)

    def add(self, **field_values):
        self.db_obj.insert(self.table_name, **field_values)

    def exists(self, user_name):
        cur_obj = self.db_obj.select_where(self.table_name, "*", username=user_name)
        if cur_obj:
            return len(cur_obj.fetchall()) > 0
        else:
            # Got Some Error
            return False

    def authenticate(self, username, password):
        cur_obj = self.db_obj.select_where(self.table_name, "*", username=username, password=password)
        if cur_obj:
            return len(cur_obj.fetchall()) > 0
        else:
            # Got Some Error
            return False

    def list_all(self):
        self.db_obj.select(self.table_name, "*")
        return self.db_obj.fetch_result_from_cursor()

    def update_where(self, set_fields: dict, **where):
        self.db_obj.update_where(self.table_name, set_fields, **where)

    def delete_all(self):
        self.db_obj.delete_all(self.table_name)

    def delete(self, **where):
        self.db_obj.delete(self.table_name, **where)

    def release(self):
        self.db_obj.free()

    def get_cursor(self):
        return self.db_obj.get_cursor()


class Projects(CRUD):
    def __init__(self):
        super(Projects, self).__init__(DBConfig.db_file["TEST"], DBConfig.PROJECT_TABLE, DBConfig.PROJECT_TABLE_FIELDS)

    def add(self, **field_values):
        self.db_obj.insert(self.table_name, **field_values)

    def list_all(self):
        self.db_obj.select(self.table_name, "*")
        return self.db_obj.fetch_result_from_cursor()

    def select_where(self, *fields, **where):
        cur_obj = self.db_obj.select_where(self.table_name, *fields, **where)
        if cur_obj:
            return cur_obj.fetchall()
        else:
            # Got Some Error
            return None

    def update_where(self, set_fields: dict, **where):
        self.db_obj.update_where(self.table_name, set_fields, **where)

    def delete_all(self):
        self.db_obj.delete_all(self.table_name)

    def delete(self, **where):
        self.db_obj.delete(self.table_name, **where)

    def release(self):
        self.db_obj.free()

    def get_cursor(self):
        return self.db_obj.get_cursor()


class TestExecution(CRUD):
    def __init__(self):
        super(TestExecution, self).__init__(DBConfig.db_file["TEST"], DBConfig.TEST_EXECUTION_TABLE, DBConfig.TEST_EXECUTION_TABLE_FIELDS)

    def add(self, **field_values):
        self.db_obj.insert(self.table_name, **field_values)

    def fetch_mapped_entries(self):
        pass

    def get_all_entry(self):
        self.db_obj.select(self.table_name, "*")
        return self.db_obj.fetch_result_from_cursor()

    def delete(self, **where):
        self.db_obj.delete(self.table_name, **where)

    def delete_all(self):
        self.db_obj.delete_all(self.table_name)

    def release(self):
        self.db_obj.free()

    def get_cursor(self):
        return self.db_obj.get_cursor()


# ======================
# Sample Usage:
# ======================
# --------------------------------------------------
# I am going to generate sample data in to DB
# --------------------------------------------------
def generate_sample_data_to_db():

    # For Users
    # ====================
    user_obj = Users()
    user_obj.delete_all()
    user_obj.add(username='root', password='root', created=datetime.datetime.now())
    user_obj.add(username='admin', password='admin', created=datetime.datetime.now())
    user_obj.add(username='test', password='password', created=datetime.datetime.now())
    print("\nListed Users: ==> ", user_obj.list_all(), "\n")
    # user_obj.release()

    # For Projects
    # ====================
    projects_obj = Projects()
    # o.delete_all()
    projects_obj.add(project_id=1, project_name="Helix-QAC Eclipse Plugin", data_source='Jenkins', jenkins_url='http://localhost:8080', jenkins_user='NIL', jenkins_password='NIL', status='active', created=datetime.datetime.now(), last_modified=datetime.datetime.now())
    projects_obj.add(project_id=2, project_name="Helix-QAC VSCode Plugin", data_source='XML', jenkins_url='NIL', jenkins_user='NIL', jenkins_password='NIL', status='active', created=datetime.datetime.now(), last_modified=datetime.datetime.now())
    projects_obj.add(project_id=3, project_name="Helix-QAC VisualStudio Plugin", data_source='XML', jenkins_url='NIL', jenkins_user='NIL', jenkins_password='NIL', status='active', created=datetime.datetime.now(), last_modified=datetime.datetime.now())
    projects_obj.add(project_id=4, project_name="Helix-QAC QACLI", data_source='XML', jenkins_url='NIL', jenkins_user='NIL', jenkins_password='NIL', status='active', created=datetime.datetime.now(), last_modified=datetime.datetime.now())
    projects_obj.add(project_id=5, project_name="Validate CLI", data_source='XML', jenkins_url='NIL', jenkins_user='NIL', jenkins_password='NIL', status='active', created=datetime.datetime.now(), last_modified=datetime.datetime.now())
    projects_obj.add(project_id=6, project_name="Validate Portal UI", data_source='XML', jenkins_url='NIL', jenkins_user='NIL', jenkins_password='NIL', status='active', created=datetime.datetime.now(), last_modified=datetime.datetime.now())
    projects_obj.add(project_id=7, project_name="Alpha-1", data_source='XML', jenkins_url='NIL', jenkins_user='NIL', jenkins_password='NIL', status='active', created=datetime.datetime.now(), last_modified=datetime.datetime.now())
    print("\nListed Projects ===> ", projects_obj.list_all(), "\n")
    # Release cursor
    # projects_obj.release()

    # For TestExecutions
    # ====================
    test_execution_obj = TestExecution()
    # test_execution_obj.delete_all()
    # test_execution_obj.add(project_id=1, test_results='{"pass": 100, "fail": 20, "error": 5, "skipped": 0}', source="XML", source_value="XML_file_PATH", execution_date=datetime.datetime.now(), crawled_date=datetime.datetime.now())
    # test_execution_obj.add(project_id=2, test_results='{"pass": 105, "fail": 0, "error": 0, "skipped": 0}', source="XML", source_value="XML_file_PATH", execution_date=datetime.datetime.now(), crawled_date=datetime.datetime.now())
    # test_execution_obj.add(project_id=3, test_results='{"pass": 50, "fail": 20, "error": 10, "skipped": 10}', source="XML", source_value="XML_file_PATH", execution_date=datetime.datetime.now(), crawled_date=datetime.datetime.now())
    # test_execution_obj.add(project_id=4, test_results='{"pass": 70, "fail": 2, "error": 1, "skipped": 1}', source="XML", source_value="XML_file_PATH", execution_date=datetime.datetime.now(), crawled_date=datetime.datetime.now())
    # test_execution_obj.add(project_id=5, test_results='{"pass": 20, "fail": 12, "error": 1, "skipped": 0}', source="XML", source_value="XML_file_PATH", execution_date=datetime.datetime.now(), crawled_date=datetime.datetime.now())
    # test_execution_obj.add(project_id=6, test_results='{"pass": 40, "fail": 22, "error": 1, "skipped": 1}', source="XML", source_value="XML_file_PATH", execution_date=datetime.datetime.now(), crawled_date=datetime.datetime.now())
    # test_execution_obj.add(project_id=7, test_results='{"pass": 60, "fail": 32, "error": 1, "skipped": 0}', source="XML", source_value="XML_file_PATH", execution_date=datetime.datetime.now(), crawled_date=datetime.datetime.now())
    # test_execution_obj.add(project_id=1, test_results='{"pass": 135, "fail": 2, "error": 10, "skipped": 2}', source="XML", source_value="XML_file_PATH", execution_date=datetime.datetime.now(), crawled_date=datetime.datetime.now())
    # test_execution_obj.add(project_id=1, test_results='{"pass": 145, "fail": 0, "error": 12, "skipped": 4}', source="XML", source_value="XML_file_PATH", execution_date=datetime.datetime.now(), crawled_date=datetime.datetime.now())
    # test_execution_obj.add(project_id=1, test_results='{"pass": 115, "fail": 1, "error": 11, "skipped": 10}', source="XML", source_value="XML_file_PATH", execution_date=datetime.datetime.now(), crawled_date=datetime.datetime.now())
    print("\nListed Executions: ==> ", test_execution_obj.get_all_entry(), "\n")
    # test_execution_obj.release()


    # and return all these three objects as well.
    return user_obj, projects_obj, test_execution_obj
