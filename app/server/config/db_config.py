class DBConfig:
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
                        'username TEXT PRIMARY KEY',
                        'password TEXT',
                        'created TIMESTAMP']

    PROJECT_TABLE = 'projects'
    PROJECT_TABLE_FIELDS = ['id INTEGER AUTOINCREMENT',
                            'project_id INTEGER NOT NULL PRIMARY KEY',
                            'project_name TEXT NOT NULL PRIMARY KEY',
                            'data_source TEXT',
                            'jenkins_url TEXT',
                            'jenkins_user TEXT',
                            'jenkins_password TEXT',
                            'status TEXT',
                            'created TIMESTAMP',
                            'last_modified TIMESTAMP']

    TEST_EXECUTION_TABLE = 'executions'
    TEST_EXECUTION_TABLE_FIELDS = ['project_id INTEGER NOT NULL',
                                   'test_results TEXT',
                                   'source TEXT',
                                   'source_value TEXT',
                                   'execution_date TIMESTAMP',
                                   'crawled_date TIMESTAMP']

    SETTINGS_TABLE = 'settings'
    SETTINGS_TABLE_FIELDS = ['project_crawl_interval TEXT'
                             'retain_record_count INTEGER']

