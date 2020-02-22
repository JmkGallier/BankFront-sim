import sqlite3
import os


class SQLManage:

    # Initiate database
    @staticmethod
    def create_connection(db_file):
        print(db_file)
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except sqlite3.Error as e:
            print(e)
        finally:
            if conn:
                conn.close()


# if __name__ == '__main__':
#     pass
    # Create build directory and create database in directory with OS module.
    # db_name = "bankFront_SQL"
    # create_connection(db_name)
