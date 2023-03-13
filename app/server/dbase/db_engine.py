"""
    author: Ashutosh Mishra (@github: nityagautam)
    desc: sqlite3 core implementation
    Caution: Do not touch this core implementation, instead use the db_manager;
"""
import datetime
import sqlite3

# =============================
# Define the queries
# =============================
import time

queries = {
    'SELECT': 'SELECT %s FROM %s',
    'SELECT_WHERE': 'SELECT %s FROM %s WHERE %s',
    'SELECT_ALL': 'SELECT %s FROM %s',
    'INSERT': 'INSERT INTO %s (%s) VALUES(%s)',
    'UPDATE_WHERE': 'UPDATE %s SET %s WHERE %s',
    'DELETE': 'DELETE FROM %s where %s',
    'DELETE_ALL': 'DELETE FROM %s',
    'CREATE_TABLE': 'CREATE TABLE IF NOT EXISTS %s(%s)',
    'DROP_TABLE': 'DROP TABLE %s'}


# =============================
# Define the Base class
# =============================
class DatabaseObject(object):

    def __init__(self, data_file):
        self.db = sqlite3.connect(data_file, check_same_thread=False)
        self.cursor = self.db.cursor()
        self.data_file = data_file

    def free(self):
        self.cursor.close()

    def get_cursor(self):
        self.cursor = self.db.cursor()
        return self.cursor

    def disconnect(self):
        self.db.close()

    def fetch_result_from_cursor(self):
        return self.cursor.fetchall()

    def fetch_one_result_from_cursor(self):
        return self.cursor.fetchone()

    def fetch_many_result_from_cursor(self, size=1):
        return self.cursor.fetchmany(size=size)

    def execute_custom_query(self, query):
        if query.split(' ')[0] in ['SELECT']:
            return self.read(query)
        else:
            return self.write(query)

    def read(self, query):
        # print("QUERY:", query)
        try:
            self.cursor.execute(query)
            return self.cursor
        except sqlite3.OperationalError as e:
            print('[DB OP ERROR]', e)
            return None

    def write(self, query, values=None):
        # print("QUERY:", query)
        # print("VALUE:", values)
        try:
            if values is not None and len(values) >= 1:
                self.cursor.execute(query, list(values))
            else:
                self.cursor.execute(query)
            self.db.commit()
            print(f'QUERY EXECUTED:==> "{query}"')
            return self.cursor
        except sqlite3.IntegrityError as e:
            # Unique / Primary key rule failed
            print('[DB OP ERROR]', e)
            return None
        except sqlite3.OperationalError as e:
            print('[DB OP ERROR]', e)
            return None

    def select(self, table, *args):
        """
        Usage:  obj.select(<TABLE_NAME>, <field_name1>, <field_name2>, ...)
                obj.select('users', 'field_name1', 'field_name2', 'field_name3', 'field_name4')
        :param table:
        :param args:
        :return:
        """
        vals = ','.join([field_name for field_name in args])
        query = queries['SELECT'] % (vals, table)
        return self.read(query)

    def select_where(self, table, *args, **kwargs):
        """
        Usage:  obj.select_where(<table_name>, <field_name1>, ..., <filed_name>=<filed_value>)
                obj.select_where('sqlite_master', 'name', name="dev")
        :param table:
        :param args:
        :param kwargs:
        :return:
        """
        if len(kwargs) >= 1:
            vals = ','.join([field_name for field_name in args])
            conds = ' and '.join(['%s=%s' % (k, v) for k, v in kwargs.items()])
            query = queries['SELECT_WHERE'] % (vals, table, conds)
            return self.read(query)
        else:
            print('[ERROR]: No data condition provided for where cond')
            return None

    def select_all(self, table, *args):
        vals = ','.join([field_name for field_name in args])
        query = queries['SELECT_ALL'] % (vals, table)
        return self.read(query)

    def insert(self, table_name, **kwargs):
        """
        Usage:  obj.insert(<TABLE_NAME>, <val1>, <val2>, ...)
                obj.insert('users', 'val1', 'val2', 'val3', 'val4')
        :param table_name:
        :param args:
        :return:
        """
        field_names = ','.join(['%s' % field for field in kwargs])
        field_value_replacements = ','.join(['?' for field in kwargs])
        values = [v for k, v in kwargs.items()]
        # print('==> VALUES: ', values)
        query = queries['INSERT'] % (table_name, field_names, field_value_replacements)
        return self.write(query, values)

    def update_where(self, table_name, set_args, **kwargs):
        """
        Usage:  obj.update_where(<table_name>, SET: {'field_name1': 'field_value1', ...}, WHERE: <field_name1>=<file_value1>, ...)
                obj.update_where('users', {'user_name': 'dev', 'user_password': 'new_pwd', 'date_created': datetime.datetime.now()}, user_name='tester')
                Above means, update the given fields, where user_name ='tester'
        :param table_name:
        :param set_args:
        :param kwargs:
        :return:
        """
        updates = ','.join(['%s=?' % k for k in set_args])
        conds = ' and '.join(['%s=?' % k for k in kwargs])
        vals = [set_args[k] for k in set_args]
        subs = [kwargs[k] for k in kwargs]
        query = queries['UPDATE_WHERE'] % (table_name, updates, conds)
        return self.write(query, vals + subs)

    def delete(self, table_name, **kwargs):
        conds = ' and '.join(['%s=?' % k for k in kwargs])
        subs = [kwargs[k] for k in kwargs]
        query = queries['DELETE'] % (table_name, conds)
        return self.write(query, subs)

    def delete_all(self, table_name):
        query = queries['DELETE_ALL'] % table_name
        return self.write(query)

    def create_table(self, table_name, values):
        query = queries['CREATE_TABLE'] % (table_name, ','.join(values))
        return self.write(query)

    def drop_table(self, table_name):
        query = queries['DROP_TABLE'] % table_name
        return self.write(query)


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
