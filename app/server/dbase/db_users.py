import datetime
from app.server.config.db_configurations import DBConfig
from app.server.config.configurations import Configurations
from app.server.dbase.DBEngine import DBEngine


class Users(Configurations):
    # ------------------------------
    # Constructor for Users class
    # ------------------------------
    def __init__(self):
        print("*" * 20, "\nPreparing Users from DB ...\n", "*" * 20, )
        # Initialize the DB file for data source
        self.db_obj = DBEngine(DBConfig.db_file[Configurations.APP_ENVIRONMENT])

        # basic tables and its schema
        self.user_table = DBConfig.USER_TABLE
        self.user_table_fields = DBConfig.USER_TABLE_FILED

        # Create the table if they don't exist
        self.db_obj.create_table(self.user_table, self.user_table_fields)

        # Add Default users
        # self.db_obj.insert(self.user_table, username='root', password='root', created=datetime.datetime.now())
        # self.db_obj.insert(self.user_table, username='admin', password='admin', created=datetime.datetime.now())
        # self.db_obj.insert(self.user_table, username='test', password='password', created=datetime.datetime.now())

        # Load User list
        self.users = {}
        self.fetch()

    # ---------------------------
    # Methods for user DB
    # ---------------------------

    def fetch(self):
        self.db_obj.select(self.user_table, "*")
        for user in self.db_obj.fetch_result_from_cursor():
            self.users[user[1]] = user[2]
        print(f"==> Prepared list of users: {self.users}")
        return self.users

    def authenticate(self, username, password):
        if len(self.users) < 1:
            # Load the users from db
            self.fetch()
        # Verify the user from users dictionary
        return True if self.users.get(username) == password else False

