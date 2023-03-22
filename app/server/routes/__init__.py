from flask import session, render_template
from app.server.config.ui_configurations import UIConfigurations
from app.server.dbase import sample_data
from app.server.dbase.db_access_data import DBData
from app.server.dbase.db_users import Users


class Gateway(UIConfigurations):
    # ==========================================================================
    # Fetch users from DB
    # ==========================================================================
    user_lists = None

    def get_users_from_db(self):
        try:
            if self.user_lists is None:
                user_lists = Users().fetch()
            return user_lists
        except Exception as e:
            print(e)
            # Return the app's fallback/default users
            return {'user': 'pwd', 'user1': 'pwd1'}

    # ==========================================================================
    # User Authentication
    # ==========================================================================
    def is_session_active(self):
        return True if 'user' in session and session['user'] and session['user'] in self.get_users_from_db().keys() else False

    def is_valid_user(self, username, password):
        return True if self.get_users_from_db().get(username) and self.get_users_from_db().get(username) == password else False

    def logout_from_session(self, username):
        session['logged_in'] = False
        session.pop('username', None)
        return True

    # ==========================================================================
    # Get the UI Configurations (for templates)
    # ==========================================================================
    def get_ui_configs_for_templates(self):
        return {"APP_META": self.APP_META, "ROUTES": self.ROUTES}

    # ==========================================================================
    # Get the data for templates based on "route" name
    # ==========================================================================
    def get_arg_data_for_template(self, route_name):
        """
        Return the data for a template based on given/provided route
        :param route_name:
        :return: 'TEMPLATE_NAME', 'PAGE_NAME', 'SESSION_USER_NAME', 'UI_CONFIG'
        """
        return self.ROUTES[route_name]["template_name"], self.ROUTES[route_name]["page_name"], session['user'], self.get_ui_configs_for_templates()

    # ==========================================================================
    # Get the complete template with args
    # ==========================================================================
    def get_template(self, route_name):
        template_name, page_name, session_user, ui_config = self.get_arg_data_for_template(route_name)
        print(f"Processing for route: {route_name}; UI_CONFIG: {ui_config}")
        # data=sample_data.latest_data if '/dashboard' in route_name else sample_data.project_list_data if '/index' in route_name else sample_data.latest_data
        return render_template(template_name,
                               pagename=page_name,
                               username=session_user,
                               ui_config=ui_config,
                               db_data=[],
                               data=DBData().get_dashboard_data() if '/dashboard' in route_name
                                        else DBData().get_overview_data() if '/index' in route_name
                                        else DBData().get_history_data() if '/history' in route_name
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
