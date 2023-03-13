class DBConfig:
    # Database name/path
    # ----------------------------------
    db_file = './app/server/dbase/test.db'

    # Tables and its schema
    # ----------------------------------
    USER_TABLE = 'users'
    USER_TABLE_FILED = ['user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT',
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
                                   'test_results TEXT',
                                   'source TEXT',
                                   'source_value TEXT',
                                   'execution_date TIMESTAMP',
                                   'crawled_date TIMESTAMP']

    SETTINGS_TABLE = 'settings'
    SETTINGS_TABLE_FIELDS = ['project_crawl_interval TEXT'
                             'retain_record_count INTEGER']

