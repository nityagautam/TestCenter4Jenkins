import datetime
from app.server.config.db_config import DBConfig
from app.server.dbase.db import DatabaseObject


# Core Template for any children;
# All children have to inherit the table
class Table(DatabaseObject):
    # ========================================
    # Constructor goes here
    # ========================================
    def __init__(self, data_file, table_name, table_field_names):
        # Initialize the super class
        # And we will be having all the props of super class here to use
        super(Table, self).__init__(data_file)
        # Create the given table first; safe creation
        self.create_table(table_name, table_field_names)
        self.table_name = table_name

    # ========================================
    # methods goes here
    # ========================================
    def select_where(self, *args, **kwargs):
        return super(Table, self).select_where([self.table_name], *args, **kwargs)

    def select_all(self, *args):
        return super(Table, self).select_all([self.table_name], *args)

    def insert(self, *args):
        return super(Table, self).insert(self.table_name, *args)

    def update_where(self, set_args, **kwargs):
        return super(Table, self).update_where(self.table_name, set_args, **kwargs)

    def delete(self, **kwargs):
        return super(Table, self).delete(self.table_name, **kwargs)

    def delete_all(self):
        return super(Table, self).delete_all(self.table_name)

    def drop_table(self):
        return super(Table, self).drop_table(self.table_name)


# ========================================
# Usr Class for DB
# ========================================
class User(Table):
    # ----------------------------------------
    # Constructor goes here
    # ----------------------------------------
    def __init__(self, data_file):
        super(User, self).__init__(data_file, DBConfig.USER_TABLE, DBConfig.USER_TABLE_FILED)

    def select_where(self, *args, **kwargs):
        cursor = super(User, self).select_where(*args, **kwargs)
        results = cursor.fetchall()
        cursor.close()
        return results

    def insert(self, **args):
        self.free(super(User, self).insert(**args))

    def update_where(self, set_args, **kwargs):
        self.free(super(User, self).update_where(set_args, **kwargs))

    def delete(self, **kwargs):
        self.free(super(User, self).delete(**kwargs))

    def delete_all(self):
        self.free(super(User, self).delete_all())

    def drop_table(self):
        self.free(super(User, self).drop_table())

    def exists(self, username):
        results = self.select_where(self.table_name, "*", username=username)
        return len(results) > 0

    def authenticate(self, username, password):
        results = self.select_where(self.table_name, "*", username=username, password=password)
        return len(results) > 0


# ========================================
# Usr Class for DB
# ========================================
class Projects(Table):
    # ----------------------------------------
    # Constructor goes here
    # ----------------------------------------
    def __init__(self, data_file):
        super(Projects, self).__init__(data_file, DBConfig.PROJECT_TABLE, DBConfig.PROJECT_TABLE_FIELDS)

    def select_where(self, *args, **kwargs):
        cursor = super(Projects, self).select_where(*args, **kwargs)
        print("==> CUR:", cursor)
        results = cursor.fetchall()
        cursor.close()
        return results

    def exists(self, project_name):
        results = self.select_where(self.table_name, "*", username=project_name)
        return len(results) > 0

    def insert(self, **args):
        self.free(super(User, self).insert(**args))

    def update_where(self, set_args, **kwargs):
        self.free(super(User, self).update_where(set_args, **kwargs))

    def delete(self, **kwargs):
        self.free(super(User, self).delete(**kwargs))


# ========================================
# Usr Class for DB
# ========================================
def normal_usage():
    db_file = './test.db'
    obj = Projects(db_file)

    # Insert project
    if not obj.exists(project_name='p1'):
        obj.insert(project_name='p1', data_source='XML', jenkins_url='NIL', jenkins_user='NIL', jenkins_password='NIL', status='active', created=datetime.datetime.now(), last_modified=datetime.datetime.now())

    # View
    print('==> \n\n', obj.select_all("*"))

    # Release cursor
    obj.free()


# normal_usage()