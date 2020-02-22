import os
from SQLite_Manage import SQLManage


# Create Build Directory
def check_build():
    build_dir = os.getcwd().replace("src", "build")
    if os.path.exists(build_dir):
        print("Build Directory Available")
        return build_dir
    else:
        print("Build Directory was not detected.")
        print("Build Directory created.")
        os.mkdir(build_dir)
        return build_dir


def check_sql(db_filename):
    SQLManage.create_connection(db_filename)


if __name__ == '__main__':
    sql_dest = check_build()
    check_sql(os.path.join(sql_dest, "bank_SQL"))

