import sqlite3
# import os


class CRUD:

    @staticmethod
    def check_database():
        pass

    @staticmethod
    def initiate_database(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except sqlite3.Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    @staticmethod
    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except sqlite3.Error as e:
            print(e)
        return conn

    @staticmethod
    def create_institutions():
        pass

    @staticmethod
    def account_types():
        pass

    @staticmethod
    def accounting_definitions():
        pass

    @staticmethod
    def account_institution_packages():
        pass

    @staticmethod
    def user_holdings():
        pass

    @staticmethod
    def user_flags():
        pass


if __name__ == '__main__':
    pass
