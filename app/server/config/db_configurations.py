"""
    @author:
      Ashutosh Mishra (@github: nityagautam)
      Software Engineer & Explorer
      nityanarayan44@gmail.com

    Created: 11 Jan, 2022
    reviewer:
    last modified:
    desc: DB Configuration file
"""

from app.server.config.configurations import Configurations


class DBConfig(Configurations):
    # ----------------------------------
    # Database file name/path
    # ----------------------------------
    db_file = {"PROD": "./data/database.db",
               "TEST": "./data/database.db",
               "SAMPLE": "./data/sample_database.db"}

    # ----------------------------------
    # Tables and its schema
    # ----------------------------------
    USER_TABLE = 'users'
    USER_TABLE_FILED = ['id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT',
                        'username TEXT',
                        'password TEXT',
                        'created TIMESTAMP']

    PROJECT_TABLE = 'projects'
    PROJECT_TABLE_FIELDS = [
        'project_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT',
        'project_name TEXT',
        'data_source TEXT',
        'jenkins_job_name TEXT',
        'jenkins_url TEXT',
        'jenkins_user TEXT',
        'jenkins_password TEXT',
        'status TEXT',
        'tags TEXT',
        'created TIMESTAMP',
        'last_modified TIMESTAMP']

    TEST_EXECUTION_TABLE = 'executions'
    TEST_EXECUTION_TABLE_FIELDS = ['project_id INTEGER NOT NULL',
                                   'project_name TEXT',
                                   'jenkins_job_name TEXT',
                                   'jenkins_job_build_no INTEGER',
                                   'jenkins_job_build_url TEXT',
                                   'duration_in_sec INTEGER',
                                   'suite_names TEXT',
                                   'test_result TEXT',
                                   'data_source TEXT',
                                   'tags TEXT',
                                   'jenkins_job_build_timestamp INTEGER',
                                   'crawled_date TIMESTAMP']
    # Within the test_result: {
    #                                    'total_count INTEGER',
    #                                    'pass_count INTEGER',
    #                                    'fail_count INTEGER',
    #                                    'skip_count INTEGER'
    #                                    }

    DATA_PARSING_FOR_TABLE = {
        "EXECUTIONS": "executions",
        "PROJECTS": "projects"
    }

    CUSTOM_QUERIES = {
        "OLDEST_CRAWLED_TEST_EXECUTIONS_DATA_FOR_DISTINCT_PROJECTS":
            "SELECT project_id, project_name, test_results, "
            "execution_date, crawled_date FROM executions "
            "GROUP BY project_name ORDER BY MIN("
            "jenkins_job_build_timestamp)",
        "LATEST_CRAWLED_TEST_EXECUTIONS_DATA_FOR_DISTINCT_PROJECTS":
            "SELECT * FROM executions GROUP BY project_name "
            "ORDER BY MAX(jenkins_job_build_timestamp) "
    }

    TABLE_JOINS = {
        "ORDER": "DESC",
        "ORDER_BY_COLUMN": "crawled_date",
        "JOIN_ON": "project_id",
        "SELECT_COLUMNS_FOR_PROJECTS_AND_EXECUTION": "*"
    }

    SETTINGS_TABLE = 'settings'
    SETTINGS_TABLE_FIELDS = ['project_crawl_interval TEXT'
                             'retain_record_count INTEGER']
