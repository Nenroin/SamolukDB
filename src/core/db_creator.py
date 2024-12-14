import os
from src import validate_db_fields
from src.core.db_manager import DBManager


class DBCreator:
    @staticmethod
    def create_db(name: str, path_to_db: str = os.getcwd()):
        validate_db_fields(name)

        table_path = os.path.join(path_to_db, name)

        if os.path.exists(table_path):
            raise Exception(f"The {table_path} file already exists.")

        with open(path_to_db + name, "w") as file:
            file.write(f"db_name${name}\n")

    @staticmethod
    def delete_db(path_to_db: str):
        db = DBManager(path_to_db)
        db_tables = db.get_table_names()

        for db_table in db_tables:
            db.delete_table(db_table)

        del db

        os.remove(path_to_db)