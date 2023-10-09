from flask import session, render_template
from app.server.config.ui_configurations import UIConfigurations
from app.server.dbase import sample_data
from app.server.dbase.DBAccess import DBAccess


class Gateway(UIConfigurations):
    def __init__(self):
        # - Fetch users list
        self.db_access_obj = None
        self.user_lists = None

    # Fetch users from DB
    # ------------------------
    def get_users_from_db(self):
        try:
            if not self.user_lists:
                if self.db_access_obj:
                    self.user_lists = self.db_access_obj.fetch_users()
                else:
                    self.db_access_obj = DBAccess()
                    self.user_lists = self.db_access_obj.fetch_users()
            return self.user_lists
        except Exception as e:
            print(e)
            # Return the app's fallback/default users
            return {'admin': 'admin', 'user1': 'password1', 'user2': 'password2'}

    #
    # User Authentication
    # -----------------------
    def is_session_active(self):
        return True if 'user' in session and session['user'] and session['user'] in self.user_lists.keys() else False

    def is_valid_user(self, username, password):
        self.get_users_from_db()
        return True if self.user_lists.get(username) and self.user_lists.get(username) == password else False

    def logout_from_session(self, username):
        session['logged_in'] = False
        session.pop(username, None)
        return True

    # Get the UI Configurations (for templates)
    # -----------------------------------------------
    def get_ui_configs_for_templates(self):
        return {"APP_META": self.APP_META, "ROUTES": self.ROUTES}

    # Get the data for templates based on "route" name
    # --------------------------------------------------
    def get_arg_data_for_template(self, route_name):
        """
        Return the data for a template based on given/provided route
        :param route_name:
        :return: 'TEMPLATE_NAME', 'PAGE_NAME', 'SESSION_USER_NAME', 'UI_CONFIG'
        """
        return self.ROUTES[route_name]["template_name"], self.ROUTES[route_name]["page_name"], session['user'], self.get_ui_configs_for_templates()

    # Get the complete template with args
    # -------------------------------------
    def get_template(self, route_name):
        template_name, page_name, session_user, ui_config = self.get_arg_data_for_template(route_name)
        print(f"REQUESTED ROUTE ==> {route_name};")
        # print(f" UI_CONFIG: {ui_config}")
        # data=sample_data.latest_data if '/dashboard' in route_name
        #           else sample_data.project_list_data if '/index' in route_name else sample_data.latest_data
        return render_template(template_name,
                               pagename=page_name,
                               username=session_user,
                               ui_config=ui_config,
                               db_data=[],
                               data=DBAccess().get_dashboard_data() if '/dashboard' in route_name
                                        else DBAccess().get_overview_data() if '/index' in route_name
                                        else DBAccess().get_history_data() if '/history' in route_name
                                        else sample_data.latest_data
                               )

    def get_error_template(self, route_name, error_data, error_code):
        template_name, page_name, session_user, ui_config = self.get_arg_data_for_template(route_name)
        return render_template(template_name,
                               pagename=page_name,
                               username=session_user,
                               ui_config=ui_config,
                               error_data=error_data
                               ), error_code
