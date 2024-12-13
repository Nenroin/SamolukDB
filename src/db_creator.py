import os


class DBCreator:
    @staticmethod
    def create_db(name: str, path_to_db: str = os.getcwd()):
        table_path = os.path.join(path_to_db, name)

        if os.path.exists(table_path):
            raise Exception(f"The {table_path} file already exists.")

        with open(path_to_db + name, "w") as file:
            file.write(f"db_name${name}\n")