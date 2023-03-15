from app.server.config.configurations import Configurations


# =================================================================
# UI Configuration class (Mainly used for templates)
# =================================================================
class UIConfigurations(Configurations):
    # -----------------------------------
    # About APP
    # -----------------------------------
    APP_META = {
        "app_name": Configurations.APP_NAME,
        "app_version": f"v[{Configurations.APP_VERSION}]",
        "app_author": f"{Configurations.AUTHOR_NAME}",
        "app_title": f"AUTOMATION DASHBOARD",
        "app_poc_tag_1": "POC PROTOTYPE-1",
        "app_experimental_tag": f"Experimental",
    }

    # -----------------------------------
    # Error messages
    # -----------------------------------
    ERROR_MESSAGES = {
        "NOT_LOGGED_IN": "You are not logged-in.",
        "NOT_AUTHORISED": "You are not authorised.",
        "INCORRECT_CREDENTIALS": "Oopse, incorrect credentials !",
        "USER_DOES_NOT_EXIST": "Oopse, seems like user does not exist in the DB.",
        "404": "Looks like we don't have it",
        "500": "Oopse, Something went wrong at our side.",
        "KEY_ERROR": "Oopse, Something went wrong at our side.",
        "EMPTY_LIST": "Oopse, Something went wrong at our side.",
        "GENERAL_ERROR_MESSAGE": "Oopse, Something went wrong."
    }

    # -----------------------------------
    # Routes in app
    # -----------------------------------
    ROUTES = {
        "/index": {
            "is_menu": True,
            "page_name": "OVERVIEW",
            "PAGE_DESC": "",
            "template_name": "index.html",
            "data": []
        },
        "/dashboard": {
            "is_menu": True,
            "page_name": "DASHBOARD",
            "PAGE_DESC": "",
            "template_name": "dashboard.html",
            "data": []
        },
        "/trends": {
            "is_menu": True,
            "page_name": "TRENDS",
            "PAGE_DESC": "",
            "template_name": "trends.html",
            "data": []
        },
        "/create-new-space": {
            "is_menu": True,
            "page_name": "CREATE NEW SPACE",
            "PAGE_DESC": "",
            "template_name": "create-new-space.html",
            "data": []
        },
        "/settings": {
            "is_menu": True,
            "page_name": "SETTINGS",
            "PAGE_DESC": "",
            "template_name": "settings.html",
            "data": []
        },
        "/notes": {
            "is_menu": True,
            "page_name": "NOTES",
            "PAGE_DESC": "",
            "template_name": "notes.html",
            "data": []
        },
        "/error": {
            "is_menu": False,
            "page_name": "ERROR",
            "PAGE_DESC": "",
            "template_name": "error.html",
            "data": []
        },
        "/about": {
            "is_menu": True,
            "page_name": "ABOUT",
            "PAGE_DESC": "",
            "template_name": "about.html",
            "data": {
                "desc": """This is the main page of the Automation Dashboard server. This application is to present the reports 
                                               more effectively and in detailed way of the executed automated suites. 
                                               It is just a POC(Proof of Concept) proto-type, to show-case the idea of a dashboard server 
                                               for better reporting of the automation reports and doing/extracting some insights from it.
                                               >>>>>  
                                               This idea came after looking at a lot of reports and jenkins execution data, 
                                               with an idea to represent the insights in a better way.""",
                "info": [
                    "App has 3 main components:: Backend Server + FrontEnd(Aggregation and reports) + Crawler",
                    "Server is written on 'Python3' with 'Flask'",
                    "Frontend is written using Javascript/HTML/CSS/ using Jinja Templating engine ",
                    "Crawler is the data extractor from the HTML/XML/JSON reports (Being written on Python3)",
                    "crawler may/may not be added as a trigger on CI/CD so that once any build get done, crawler should be "
                    "triggered as a POST-ACTION.",
                    "they(Crawlers) can also be triggerd independently."
                ]
            }
        }
    }

    report_data_config = {
        "preserve_reports_history_for_days": 20
    }

    app_ui_config = {
        # -----------------------------------
        # Old UI Config for templates
        # -----------------------------------
        # -----------------------------------------------------------------------------------------
        # Routes of the application [Menus]
        # Key for routes, must exist in the server's routes files (inside the app/server/routes/ )
        # if 'is_menu' is True then it will be rendered in the nav bar as menu option
        # -----------------------------------------------------------------------------------------

        'side_menu': [
            {
                "name": "DASHBOARD",
                "route": "/dashboard",                  # The route name should be in the routes.py file
                "icon": "fa fa-dashboard fa-lg fa-fw"
            },
            {
                "name": "ANALYTICS",
                "route": "/analytics",
                "icon": "fa fa-bar-chart fa-lg fa-fw"
            },
            {"name": "-", "route": "-", "icon": "-"},
            {"name": "-", "route": "-", "icon": "-"},
            {"name": "-", "route": "-", "icon": "-"},
            {"name": "-", "route": "-", "icon": "-"},

            {
                "name": "NOTES",
                "route": "/notes",
                "icon": "fa fa-newspaper-o fa-lg fa-fw"
            },
            {
                "name": "ABOUT",
                "route": "/about",
                "icon": "fa fa-book"
            }
        ]
        # End of side menu
    }
    # ===[UI Config Ends]===================================================================
