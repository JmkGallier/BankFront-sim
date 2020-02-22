import os
from SQLite_CRUD import CRUD


# Create Build Directory
def check_build():
    build_dir = os.getcwd().replace("src", "build")
    if os.path.exists(build_dir):
        print("'build' Directory Available")
        return build_dir
    else:
        print("No 'build' Directory\nCreating 'build' Directory")
        os.mkdir(build_dir)
        return build_dir


def check_sql(db_filename):
    CRUD.initiate_database(db_filename)


if __name__ == '__main__':
    sql_dest = check_build()
    check_sql(os.path.join(sql_dest, "bank_SQL"))
