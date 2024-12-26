import os
from src import validate_db_fields
from src.core.db_controller_base import DBControllerBase


class DBCreator:
    @staticmethod
    def create_db(name: str, path_to_db: str = os.getcwd()):
        validate_db_fields(name)

        db_path = os.path.join(path_to_db, name)

        if os.path.exists(db_path):
            raise Exception(f"The {db_path} file already exists.")

        with open(path_to_db + name, "w") as file:
            file.write(f"db_name${name}\n")

    @staticmethod
    def delete_db(db: DBControllerBase):
        db.delete_db()