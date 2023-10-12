"""
    @author:
      Ashutosh Mishra (@github: nityagautam)
      Software Engineer & Explorer
      nityanarayan44@gmail.com

    Created: 11 Jan, 2022
    reviewer:
    last modified: 12 Oct 2023
    desc: SQLite3 Engine;
"""

import sqlite3

# =============================
# Define the queries
# =============================

queries = {
    'SELECT': 'SELECT %s FROM %s',
    'SELECT_ALL': 'SELECT * FROM %s',
    'SELECT_WHERE': 'SELECT %s FROM %s WHERE %s',
    'SELECT_WHERE_WITH_LIMIT': 'SELECT %s FROM %s WHERE %s LIMIT %s',
    'SELECT_WHERE_WITH_LIMIT_AND_DESC_ORDER_BY': 'SELECT %s FROM %s WHERE %s ORDER BY %s DESC LIMIT %s',
    'INSERT': 'INSERT INTO %s (%s) VALUES(%s)',
    'UPDATE_WHERE': 'UPDATE %s SET %s WHERE %s',
    'DELETE_WHERE': 'DELETE FROM %s WHERE %s',
    'DELETE_ALL': 'DELETE FROM %s',
    'CREATE_TABLE': 'CREATE TABLE IF NOT EXISTS %s(%s)',
    'DROP_TABLE': 'DROP TABLE %s'}


# =============================
# Define the Base class
# =============================
class DBEngine(object):

    def __init__(self, data_file):
        print(f"  [DatabaseObject] DB Given to connect ===> : {data_file}")
        self.db = sqlite3.connect(data_file, check_same_thread=True)
        self.cursor = self.db.cursor()
        self.data_file = data_file

    # -----------------------------------
    # Basic sqlite APIs
    # -----------------------------------

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

    def read(self, query):
        # print("QUERY:", query)
        try:
            self.cursor.execute(query)
            # print(f'|  QUERY EXECUTED[R]:==> "{query}"')
            return self.cursor
        except sqlite3.OperationalError as e:
            print(f'[DB OP ERROR] Error while executing query: {query}\n', e)
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
            # print(f'|  QUERY EXECUTED[W]:==> "{query}"')
            return self.cursor
        except sqlite3.IntegrityError as e:
            # Unique / Primary key rule failed
            print(f'[DB OP ERROR] Error while executing query {query}\n', e)
            return None
        except sqlite3.OperationalError as e:
            print(f'[DB OP ERROR] Error while executing query: {query}\n', e)
            return None

    # -----------------------------------
    # To execute custom query string
    # -----------------------------------

    def execute_query(self, query):
        """
        To execute a custom query string

        :param query:
        :return: db cursor
        """
        if query.split(' ')[0] in ['SELECT']:
            return self.read(query)
        else:
            return self.write(query)

    # -----------------------------------
    # Custom APIs related to CREATE
    # -----------------------------------

    def create_table(self, table_name, table_field_schema):
        query = queries['CREATE_TABLE'] % (table_name, ','.join(table_field_schema))
        return self.write(query)

    # -----------------------------------
    # Custom APIs related to SELECT
    # -----------------------------------

    def select(self, table, *args):
        """
        To select everything from table but for provided columns

        Usage:  obj.select(<TABLE_NAME>, <field_name1>, <field_name2>, ...)
                obj.select('users', 'field_name1', 'field_name2', 'field_name3', 'field_name4')
        :param table:
        :param args:
        :return:
        """
        vals = ','.join([field_name for field_name in args])
        query = queries['SELECT'] % (vals, table)
        return self.read(query)

    def select_everything(self, table):
        """
        To select everything from table

        Usage:  obj.select(<TABLE_NAME>)
                obj.select('users')

        :param table:
        :return: returns data for entire table
        """
        query = queries['SELECT_ALL'] % table
        return self.read(query)

    def select_where(self, table, *args, **kwargs):
        """
        To select provided column from table with WHERE condition

        Usage:  obj.select_where(<table_name>, <field_name1>, ..., <filed_name>=<filed_value>)
                obj.select_where('table1', 'name', name="dev")
        :param table:
        :param args: denotes the fields to be selected
        :param kwargs: denotes the where conditions
        :return: entire selected record
        """
        if len(kwargs) >= 1:
            vals = ','.join([field_name for field_name in args])
            conditions = ' and '.join(['%s=%s' % (k, v) for k, v in kwargs.items()])
            query = queries['SELECT_WHERE'] % (vals, table, conditions)
            return self.read(query)
        else:
            print('[ERROR]: No data condition provided for where cond')
            return None

    def select_where_with_limit(self, table, limit, *args, **kwargs):
        """
        To select provided column with WHERE condition with provided LIMIT

        Usage:  obj.select_where(<table_name>, <limit>, <field_name1>, ..., <filed_name>=<filed_value>)
                obj.select_where('sqlite_master', '30', 'name', name="dev")
        :param table:
        :param limit: integer type for the limiting the selected record
        :param args: denotes the fields to be selected
        :param kwargs: denotes the where conditions
        :return: entire selected record
        """
        if len(kwargs) >= 1:
            vals = ','.join([field_name for field_name in args])
            conditions = ' and '.join(['%s=%s' % (k, v) for k, v in kwargs.items()])
            if not limit:
                # Setting limit by default; Should refer from Configurations
                limit = '30'
            query = queries['SELECT_WHERE_WITH_LIMIT'] % (vals, table, conditions, limit)
            return self.read(query)
        else:
            print('[ERROR]: No data condition provided for where cond')
            return None

    def select_where_with_limit_and_desc_order_by(self, table, limit, order_by_column: str, *args, **kwargs):
        """
        To select provided column with WHERE condition with provided LIMIT with descending order.

        Usage:  obj.select_where(<table_name>, <limit>, <order_by_column>, <field_name1>, ..., <filed_name>=<filed_value>)
                obj.select_where('sqlite_master', '30', 'report_date', 'name', name="dev")
        :param table:
        :param limit:
        :param order_by_column:
        :param args:
        :param kwargs:
        :return:
        """
        if len(kwargs) >= 1:
            vals = ','.join([field_name for field_name in args])
            conditions = ' and '.join(['%s=%s' % (k, v) for k, v in kwargs.items()])
            if not limit:
                limit = '30'
            query = queries['SELECT_WHERE_WITH_LIMIT_AND_DESC_ORDER_BY'] % (vals, table, conditions, order_by_column, limit)
            return self.read(query)
        else:
            print('[ERROR]: Some data were not provided to fetch from DB; Check for where cond, limit, order by column')
            return None

    # -----------------------------------
    # Custom APIs related to INSERT
    # -----------------------------------

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

    # -----------------------------------
    # Custom APIs related to UPDATE
    # -----------------------------------

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
        conditions = ' and '.join(['%s=?' % k for k in kwargs])
        vals = [set_args[k] for k in set_args]
        subs = [kwargs[k] for k in kwargs]
        query = queries['UPDATE_WHERE'] % (table_name, updates, conditions)
        return self.write(query, vals + subs)

    # -----------------------------------
    # Custom APIs related to DELETE
    # -----------------------------------

    def delete(self, table_name, **kwargs):
        conditions = ' and '.join(['%s=?' % k for k in kwargs])
        subs = [kwargs[k] for k in kwargs]
        query = queries['DELETE_WHERE'] % (table_name, conditions)
        return self.write(query, subs)

    def delete_all(self, table_name):
        query = queries['DELETE_ALL'] % table_name
        return self.write(query)

    def drop_table(self, table_name):
        query = queries['DROP_TABLE'] % table_name
        return self.write(query)


# ======================
# Sample Usage:
# ======================
def sample_usage():
    obj = DBEngine('./app/server/dbase/test.db')
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
