import datetime

from app.server.config.db_config import DBConfig
from app.server.dbase.db import DatabaseObject


class CRUD:
    def __init__(self, db_file, table_name, table_fields):
        # Initialize the DB file
        # obj = DatabaseObject('./app/server/dbase/test.db')
        self.db_obj = DatabaseObject(db_file)

        # Creation begins
        # Create Projects table, if not exist
        self.table_name = table_name
        self.table_fields = table_fields
        self.db_obj.create_table(table_name, table_fields)


class Projects(CRUD):
    def __init__(self):
        super(Projects, self).__init__(DBConfig.db_file, DBConfig.PROJECT_TABLE, DBConfig.PROJECT_TABLE_FIELDS)

    def add(self, **field_values):
        self.db_obj.insert(self.table_name, **field_values)

    def list_all(self):
        self.db_obj.select(self.table_name, "*")
        return self.db_obj.fetch_result_from_cursor()

    def update_where(self, set_fields: dict, **where):
        self.db_obj.update_where(self.table_name, set_fields, **where)

    def delete_all(self):
        self.db_obj.delete_all(self.table_name)

    def release(self):
        self.db_obj.free()

    def get_cursor(self):
        return self.db_obj.get_cursor()

# ======================
# Sample Usage:
# ======================
def run():
    o = Projects()
    o.add("project1", data_source='XML',
          jenkins_url='NIL', jenkins_user='NIL', jenkins_password='NIL', status='active', created=datetime.datetime.now(), last_modified=datetime.datetime.now())
    print("Projects ===> ", o.list_all())
# run()


# ======================
# Sample Usage:
# ======================
def sample_usage():
    obj = DatabaseObject('./app/server/dbase/test.db')
    # obj = DatabaseObject(DBConfig.db_file)

    # # Create a user base
    # obj.create_table('users', ['user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT', 'user_name TEXT', 'user_password TEXT', 'date_created TIMESTAMP'])
    # # Check table
    # # obj.select('sqlite_master', 'name')
    # obj.select_where('sqlite_master', 'name', name="'users'")
    # print("SQLITE TABLES:", obj.fetch_result_from_cursor())

    # Insert data to table
    # Check before insertion
    # obj.select_where('users', 'user_name', user_name="'a'")
    # res = obj.fetch_result_from_cursor()
    # if len(res) == 0:
    #     # obj.insert('users', 'a', 'pwd', datetime.datetime.now())
    #     obj.insert('users', user_name='a', user_password='pwd', date_created=datetime.datetime.now())
    # else:
    #     print(f'"a" User already exists')

    # Fetch data from table
    obj.select('users', '*')
    print("USER FROM DB:", obj.fetch_result_from_cursor())

    obj.select('projects', '*')
    print("USER FROM DB:", obj.fetch_result_from_cursor())

    # # Update User data
    # # Check before update
    # obj.select_where('users', 'user_name', user_name="'tester'")
    # res = obj.fetch_result_from_cursor()
    # if len(res) >= 1:
    #     obj.update_where('users', {'user_name': 'dev', 'user_password': 'new_pwd', 'date_created': datetime.datetime.now()}, user_name='tester')
    # else:
    #     print(f'No "dev" user exists')
    #
    # # Fetch data from table
    # obj.select('users', '*')
    # print("USER FROM DB:", obj.fetch_result_from_cursor())

    # Release the DB
    obj.free()
    obj.disconnect()
# sample_usage()
