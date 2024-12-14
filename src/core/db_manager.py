import os
from src import EValueType
from src.entities.link import Link
from src.entities.row_data import RowData
from src.entities.table import Table


class DBManager:
    __path_to_db: str
    __db_name: str
    __db_tables: dict[str, str]

    def __init__(self, path_to_db):
        self.__path_to_db = path_to_db
        self.__db_tables = {}

        with open(path_to_db, "r") as file:
            for index, line in enumerate(file):
                if index == 0:
                    self.__db_name = line.split("$")[1].rstrip("\n")
                else:
                    self.__db_tables[line.split("$")[0].rstrip("\n")] = line.split("$")[1].rstrip("\n")

    @property
    def name(self):
        return self.__db_name

    def add_tables(self, tables: list[Table]):
        table_path = self.__path_to_db.rsplit("/", 1)[0] + "/"

        if any(table.name in self.__db_tables for table in tables):
            raise Exception("A table with that name already exists")

        for table in tables:
            with open(table_path + table.name, "w") as file:
                file.write(f"id${EValueType.INT.value}, ")

                for index, row in enumerate(table.columns):
                    file.write(f"{row.name}${row.type}")

                    if index == (len(table.columns) - 1):
                        file.write("\n")
                    else:
                        file.write(", ")

            with open(self.__path_to_db, "a") as file:
                file.write(f"{table.name}${table_path + table.name}\n")
                self.__db_tables[table.name] = table_path + table.name

    def delete_table(self, table_name: str):
        self.__is_table_exist(table_name)

        os.remove(self.__db_tables.get(table_name))
        self.__db_tables.pop(table_name)

    def get_table_names(self) -> list[str]:
        table_names: list[str] = []
        for name in self.__db_tables:
            table_names.append(name)

        return table_names

    def get_table_row_names(self, table_name: str) -> list[str]:
        self.__is_table_exist(table_name)

        table_path = self.__path_to_db.rsplit("/", 1)[0] + "/"

        table_rows: str
        with open(table_path + table_name, "r") as file:
            table_rows = file.readline().rstrip("\n")

        return [item.split("$")[0] for item in table_rows.split(', ')]

    def get_table_row_types(self, table_name: str) -> list[str]:
        self.__is_table_exist(table_name)

        table_path = self.__path_to_db.rsplit("/", 1)[0] + "/"

        table_rows: str
        with open(table_path + table_name, "r") as file:
            table_rows = file.readline().rstrip("\n")

        return [item.split("$")[1] for item in table_rows.split(', ')]

    def add_item(self, table_name: str, data: RowData):
        self.__is_table_exist(table_name)
        data.check_types(self.get_table_row_types(table_name)[1:])

        current_index = self.__get_last_table_index(table_name) + 1
        table_path = self.__path_to_db.rsplit("/", 1)[0] + "/"

        with open(table_path + table_name, "a") as file:
            file.write(f"{current_index}$")
            for idx, d in enumerate(data):
                separator = "\n" if idx == (len(data) - 1) else "$"
                value = f"{d.table_name},{d.row_index}" if isinstance(d, Link) else str(d)
                file.write(f"{value}{separator}")

    def update_item(self, table_name: str, item_id: str, data: dict):
        pass

    def delete_item(self, table_name: str, item_id: str):
        pass

    def get_item_list(self, table_name: str):
        self.__is_table_exist(table_name)

        table_path = self.__path_to_db.rsplit("/", 1)[0] + "/"

        with open(table_path + table_name, "r") as file:
            for idx, line in enumerate(file):
                if idx == 0:
                    for col in line.split(", "):
                        print(col.split("$")[0], end="   ")
                    print()
                else:
                    print(line.replace("$", "   "), end="")

    def get_item(self, table_name: str, row: str, value: str):
        pass

    def __check_links(self, data:RowData):
        pass

    def __get_last_table_index(self, table_name: str) -> int:
        table_path = self.__path_to_db.rsplit("/", 1)[0] + "/"

        last_idx: int = 0
        with open(table_path + table_name, "r") as file:
            for _ in file:
                last_idx += 1

        return last_idx - 1

    def __is_table_exist(self, name: str):
        if self.__db_tables.get(name) is None:
            raise Exception("A table with that name does not exist")
