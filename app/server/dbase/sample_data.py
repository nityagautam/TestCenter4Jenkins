# ===[Sample data Starts]============================================================

# Sample recent crawled data
project_list_data = [
    {"project_id": "001", "project_name": "Project Theta-1", "date_created": "15 Aug 2021", "status": "active", "data_source": "jenkins", "jenkins_url": "http://localhost:8080", "jenkins_uname": "dev", "jenkins_pwd": "pwd_digest"},
    {"project_id": "002", "project_name": "Project Theta-2", "date_created": "15 Aug 2021", "status": "active", "data_source": "xml/json", "jenkins_url": "", "jenkins_uname": "", "jenkins_pwd": ""},
    {"project_id": "003", "project_name": "Project Theta-3", "date_created": "15 Aug 2021", "status": "active", "data_source": "xml/json", "jenkins_url": "", "jenkins_uname": "", "jenkins_pwd": ""},
    {"project_id": "004", "project_name": "Project Theta-4", "date_created": "15 Aug 2021", "status": "active", "data_source": "xml/json", "jenkins_url": "", "jenkins_uname": "", "jenkins_pwd": ""},
    {"project_id": "005", "project_name": "Project Theta-5", "date_created": "15 Aug 2021", "status": "active", "data_source": "xml/json", "jenkins_url": "", "jenkins_uname": "", "jenkins_pwd": ""},
    {"project_id": "006", "project_name": "Project Theta-6", "date_created": "15 Aug 2021", "status": "active", "data_source": "xml/json", "jenkins_url": "", "jenkins_uname": "", "jenkins_pwd": ""},
    {"project_id": "007", "project_name": "Project Theta-7", "date_created": "15 Aug 2021", "status": "active", "data_source": "xml/json", "jenkins_url": "", "jenkins_uname": "", "jenkins_pwd": ""},

]
latest_datas = []
latest_data = [
    {
        "key": "server",
        "project_name": "Project Theta-1",
        "build_no": "build16",
        "data_source": "Jenkins",
        "build_url": "https://jenkins.url/prj/build15",
        "report_date": "15 Aug 2021",
        "crawled_date": "10 Aug 2021",
        "report_location": "https://some.path/prj/build15/index.html",
        "test_result": {"pass": 120, "fail": 10, "error": 3, "skipped": 2}
    },
    {
        "key": "Well, I came from flask server",
        "project_name": "Project Theta-2",
        "data_source": "Jenkins",
        "build_no": "build15",
        "build_url": "https://jenkins.url/prj/build15",
        "report_date": "15 Aug 2021",
        "crawled_date": "10 Aug 2021",
        "report_location": "https://some.path/prj/build15/index.html",
        "test_result": {"pass": 200, "fail": 1, "error": 3, "skipped": 2}
    },
    {
        "key": "Well, I came from flask server",
        "project_name": "Project Theta-3",
        "data_source": "Jenkins",
        "build_no": "build15",
        "build_url": "https://jenkins.url/prj/build15",
        "report_date": "15 Aug 2021",
        "crawled_date": "10 Aug 2021",
        "report_location": "https://some.path/prj/build15/index.html",
        "test_result": {"pass": 100, "fail": 5, "error": 0, "skipped": 2}
    },
    {
        "key": "Well, I came from flask server",
        "project_name": "Project Theta-4",
        "data_source": "Jenkins",
        "build_no": "build16",
        "build_url": "https://jenkins.url/prj/build16",
        "report_date": "15 Aug 2021",
        "crawled_date": "11 Aug 2021",
        "report_location": "https://some.path/prj/build16/index.html",
        "test_result": {"pass": 150, "fail": 10, "error": 12, "skipped": 1}
    },
    {
        "key": "Well, I came from flask server",
        "project_name": "Project Theta-5",
        "data_source": "Jenkins",
        "build_no": "build17",
        "build_url": "https://jenkins.url/prj/build17",
        "report_date": "15 Aug 2021",
        "crawled_date": "12 Aug 2021",
        "report_location": "https://some.path/prj/build17/index.html",
        "test_result": {"pass": 6, "fail": 1, "error": 2, "skipped": 1}
    },
    {
        "key": "Well, I came from flask server",
        "project_name": "Project Theta-6",
        "data_source": "Jenkins",
        "build_no": "build17",
        "build_url": "https://jenkins.url/prj/build17",
        "report_date": "15 Aug 2021",
        "crawled_date": "14 Aug 2021",
        "report_location": "https://some.path/prj/build17/index.html",
        "test_result": {"pass": 6, "fail": 1, "error": 2, "skipped": 1}
    },
    {
        "key": "Well, I came from flask server",
        "project_name": "Project Theta-7",
        "data_source": "Jenkins",
        "build_no": "build17",
        "build_url": "https://jenkins.url/prj/build17",
        "report_date": "13 Aug 2021",
        "crawled_date": "14 Aug 2021",
        "report_location": "https://some.path/prj/build17/index.html",
        "test_result": {"pass": 6, "fail": 1, "error": 2, "skipped": 1}
    }

]

# Sample Historical Data
history_data = [
    {
        "project_name": "SMPL Helix QAC Dashboard",
        "history": [
            {
                "build_no": "build1",
                "build_url": "https://jenkins.url/prj/build2",
                "report_date": "1 Aug 2021",
                "crawled_date": "1 Aug 2021",
                "report_location": "https://some.path/prj/build1/index.html",
                "test_result": {"pass": 6, "fail": 1, "error": 2, "skipped": 1}
            },
            {
                "build_no": "build2",
                "build_url": "https://jenkins.url/prj/build2",
                "report_date": "2 Aug 2021",
                "crawled_date": "2 Aug 2021",
                "report_location": "https://some.path/prj/build2/index.html",
                "test_result": {"pass": 2, "fail": 4, "error": 2, "skipped": 1}
            },
            {
                "build_no": "build3",
                "build_url": "https://jenkins.url/prj/build3",
                "report_date": "3 Aug 2021",
                "crawled_date": "3 Aug 2021",
                "report_location": "https://some.path/prj/build3/index.html",
                "test_result": {"pass": 6, "fail": 3, "error": 0, "skipped": 1}
            },
            {
                "build_no": "build4",
                "build_url": "https://jenkins.url/prj/build4",
                "report_date": "4 Aug 2021",
                "crawled_date": "4 Aug 2021",
                "report_location": "https://some.path/prj/build4/index.html",
                "test_result": {"pass": 9, "fail": 0, "error": 0, "skipped": 1}
            },
            {
                "build_no": "build5",
                "build_url": "https://jenkins.url/prj/build5",
                "report_date": "5 Aug 2021",
                "crawled_date": "5 Aug 2021",
                "report_location": "https://some.path/prj/build5/index.html",
                "test_result": {"pass": 1, "fail": 9, "error": 0, "skipped": 0}
            },
            {
                "build_no": "build6",
                "build_url": "https://jenkins.url/prj/build6",
                "report_date": "6 Aug 2021",
                "crawled_date": "6 Aug 2021",
                "report_location": "https://some.path/prj/build6/index.html",
                "test_result": {"pass": 7, "fail": 0, "error": 0, "skipped": 3}
            },
            {
                "build_no": "build7",
                "build_url": "https://jenkins.url/prj/build7",
                "report_date": "7 Aug 2021",
                "crawled_date": "7 Aug 2021",
                "report_location": "https://some.path/prj/build7/index.html",
                "test_result": {"pass": 5, "fail": 0, "error": 5, "skipped": 0}
            },
            {
                "build_no": "build8",
                "build_url": "https://jenkins.url/prj/build8",
                "report_date": "8 Aug 2021",
                "crawled_date": "8 Aug 2021",
                "report_location": "https://some.path/prj/build8/index.html",
                "test_result": {"pass": 1, "fail": 9, "error": 0, "skipped": 0}
            },
            {
                "build_no": "build9",
                "build_url": "https://jenkins.url/prj/build7",
                "report_date": "9 Aug 2021",
                "crawled_date": "9 Aug 2021",
                "report_location": "https://some.path/prj/build9/index.html",
                "test_result": {"pass": 2, "fail": 7, "error": 0, "skipped": 1}
            },
            {
                "build_no": "build10",
                "build_url": "https://jenkins.url/prj/build10",
                "report_date": "10 Aug 2021",
                "crawled_date": "10 Aug 2021",
                "report_location": "https://some.path/prj/build10/index.html",
                "test_result": {"pass": 3, "fail": 6, "error": 0, "skipped": 1}
            },
            {
                "build_no": "build11",
                "build_url": "https://jenkins.url/prj/build11",
                "report_date": "11 Aug 2021",
                "crawled_date": "11 Aug 2021",
                "report_location": "https://some.path/prj/build11/index.html",
                "test_result": {"pass": 4, "fail": 5, "error": 0, "skipped": 1}
            },
            {
                "build_no": "build12",
                "build_url": "https://jenkins.url/prj/build12",
                "report_date": "12 Aug 2021",
                "crawled_date": "12 Aug 2021",
                "report_location": "https://some.path/prj/build12/index.html",
                "test_result": {"pass": 5, "fail": 4, "error": 0, "skipped": 1}
            },
            {
                "build_no": "build13",
                "build_url": "https://jenkins.url/prj/build13",
                "report_date": "13 Aug 2021",
                "crawled_date": "13 Aug 2021",
                "report_location": "https://some.path/prj/build13/index.html",
                "test_result": {"pass": 6, "fail": 3, "error": 0, "skipped": 1}
            },
            {
                "build_no": "build14",
                "build_url": "https://jenkins.url/prj/build14",
                "report_date": "14 Aug 2021",
                "crawled_date": "14 Aug 2021",
                "report_location": "https://some.path/prj/build14/index.html",
                "test_result": {"pass": 7, "fail": 2, "error": 0, "skipped": 1}
            },
            {
                "build_no": "build15",
                "build_url": "https://jenkins.url/prj/build15",
                "report_date": "15 Aug 2021",
                "crawled_date": "15 Aug 2021",
                "report_location": "https://some.path/prj/build15/index.html",
                "test_result": {"pass": 8, "fail": 1, "error": 0, "skipped": 1}
            }
        ]
    },
    {
        "project_name": "SMPL prj-1",
        "history": [
            {
                "build_no": "build1",
                "build_url": "https://jenkins.url/prj/build2",
                "report_date": "1 Aug 2021",
                "crawled_date": "1 Aug 2021",
                "report_location": "https://some.path/prj/build1/index.html",
                "test_result": {"pass": 6, "fail": 1, "error": 2, "skipped": 1}
            },
            {
                "build_no": "build2",
                "build_url": "https://jenkins.url/prj/build2",
                "report_date": "2 Aug 2021",
                "crawled_date": "2 Aug 2021",
                "report_location": "https://some.path/prj/build2/index.html",
                "test_result": {"pass": 2, "fail": 4, "error": 2, "skipped": 1}
            },
            {
                "build_no": "build3",
                "build_url": "https://jenkins.url/prj/build3",
                "report_date": "3 Aug 2021",
                "crawled_date": "3 Aug 2021",
                "report_location": "https://some.path/prj/build3/index.html",
                "test_result": {"pass": 6, "fail": 3, "error": 0, "skipped": 1}
            },
            {
                "build_no": "build4",
                "build_url": "https://jenkins.url/prj/build4",
                "report_date": "4 Aug 2021",
                "crawled_date": "4 Aug 2021",
                "report_location": "https://some.path/prj/build4/index.html",
                "test_result": {"pass": 9, "fail": 0, "error": 0, "skipped": 1}
            },
            {
                "build_no": "build5",
                "build_url": "https://jenkins.url/prj/build5",
                "report_date": "5 Aug 2021",
                "crawled_date": "5 Aug 2021",
                "report_location": "https://some.path/prj/build5/index.html",
                "test_result": {"pass": 9, "fail": 1, "error": 0, "skipped": 0}
            },
            {
                "build_no": "build6",
                "build_url": "https://jenkins.url/prj/build6",
                "report_date": "6 Aug 2021",
                "crawled_date": "6 Aug 2021",
                "report_location": "https://some.path/prj/build6/index.html",
                "test_result": {"pass": 7, "fail": 0, "error": 0, "skipped": 3}
            },
            {
                "build_no": "build7",
                "build_url": "https://jenkins.url/prj/build7",
                "report_date": "7 Aug 2021",
                "crawled_date": "7 Aug 2021",
                "report_location": "https://some.path/prj/build7/index.html",
                "test_result": {"pass": 10, "fail": 0, "error": 0, "skipped": 0}
            }
        ]
    }
]
