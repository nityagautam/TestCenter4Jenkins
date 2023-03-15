from app.server.config.configurations import Configurations


class DBConfig(Configurations):
    # ----------------------------------
    # Database file name/path
    # ----------------------------------
    db_file = {"PROD": "./app/server/dbase/prod_database.db",
               "TEST": "./app/server/dbase/test.db",
               "SAMPLE": "./app/server/dbase/sample.db"}

    # ----------------------------------
    # Tables and its schema
    # ----------------------------------
    USER_TABLE = 'users'
    USER_TABLE_FILED = ['id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT',
                        'username TEXT',
                        'password TEXT',
                        'created TIMESTAMP']

    PROJECT_TABLE = 'projects'
    PROJECT_TABLE_FIELDS = ['project_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT',
                            'project_name TEXT',
                            'data_source TEXT',
                            'jenkins_url TEXT',
                            'jenkins_user TEXT',
                            'jenkins_password TEXT',
                            'status TEXT',
                            'created TIMESTAMP',
                            'last_modified TIMESTAMP']

    TEST_EXECUTION_TABLE = 'executions'
    TEST_EXECUTION_TABLE_FIELDS = ['project_id INTEGER NOT NULL',
                                   'project_name TEXT',
                                   'test_results TEXT',
                                   'source TEXT',
                                   'source_value TEXT',
                                   'execution_date TIMESTAMP',
                                   'crawled_date TIMESTAMP']

    TABLE_JOINS = {
        "ORDER": "DESC",
        "ORDER_BY_COLUMN": "crawled_date",
        "JOIN_ON": "project_id",
        # "SELECT_COLUMNS_FOR_PROJECTS_AND_EXECUTION": "project_name, test_results, source, source_value, crawled_date"
        "SELECT_COLUMNS_FOR_PROJECTS_AND_EXECUTION": "*"
    }

    SETTINGS_TABLE = 'settings'
    SETTINGS_TABLE_FIELDS = ['project_crawl_interval TEXT'
                             'retain_record_count INTEGER']

