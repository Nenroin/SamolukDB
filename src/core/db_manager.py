import os
from typing import TextIO
from src import EValueType, convert_to
from src.entities.link import Link
from src.entities.row_data import RowData
from src.entities.table import Table


class DBManager:
    __path_to_db: str
    __db_name: str
    __db_tables: dict[str, str]
    __db_open_files: dict[str, TextIO]

    def __init__(self, path_to_db: str = None):
        if path_to_db:
            self.open(path_to_db)
        else:
            self.__clear_variables()

    def open(self, path_to_db: str):
        if not os.path.exists(path_to_db):
            raise Exception("DB does not exist")

        self.__path_to_db = path_to_db
        self.__db_tables = {}
        temporary_db_name = "temporary_name"
        self.__db_open_files = {temporary_db_name: open(path_to_db, "r+")}

        file = self.__db_open_files[temporary_db_name]

        for index, line in enumerate(file):
            if index == 0:
                self.__db_name = line.split("$")[1].rstrip("\n")
                self.__db_open_files[self.__db_name] = self.__db_open_files.pop(temporary_db_name)
            else:
                table_name, table_path = line.split("$")[0].rstrip("\n"), line.split("$")[1].rstrip("\n")

                self.__db_tables[table_name] = table_path
                self.__db_open_files[table_name] = open(table_path, "r+")

    def close(self):
        for file in self.__db_open_files.values():
            file.close()

        self.__clear_variables()

    @property
    def name(self) -> str:
        return self.__db_name

    def add_tables(self, tables: list[Table]):
        table_path = self.__path_to_db.rsplit("/", 1)[0] + "/"

        if any(table.name in self.__db_tables for table in tables):
            raise Exception("A table with that name already exists")

        for table in tables:
            self.__db_open_files[table.name] = open(table_path + table.name, "w+")

            file = self.__db_open_files[table.name]

            file.write(f"id${EValueType.INT.value}, ")

            for index, row in enumerate(table.columns):
                file.write(f"{row.name}${row.type}")

                if index == (len(table.columns) - 1):
                    file.write("\n")
                else:
                    file.write(", ")

            file = self.__db_open_files[self.__db_name]

            file.write(f"{table.name}${table_path + table.name}\n")
            self.__db_tables[table.name] = table_path + table.name

    def delete_table(self, table_name: str):
        self.__is_table_exist(table_name)

        self.__db_open_files[table_name].close()
        self.__db_open_files.pop(table_name)

        os.remove(self.__db_tables.get(table_name))

        self.__db_tables.pop(table_name)

    def get_table_names(self) -> list[str]:
        table_names: list[str] = []
        for name in self.__db_tables:
            table_names.append(name)

        return table_names

    def get_table_row_names(self, table_name: str) -> list[str]:
        self.__is_table_exist(table_name)

        file = self.__db_open_files[table_name]
        file.seek(0)

        table_rows = file.readline().rstrip("\n")
        return [item.split("$")[0] for item in table_rows.split(', ')]

    def get_table_row_types(self, table_name: str) -> list[str]:
        self.__is_table_exist(table_name)

        file = self.__db_open_files[table_name]
        file.seek(0)

        table_rows = file.readline().rstrip("\n")
        return [item.split("$")[1] for item in table_rows.split(', ')]

    def add_item(self, table_name: str, data: RowData):
        self.__is_table_exist(table_name)
        data.check_types(self.get_table_row_types(table_name)[1:])

        current_index = self.__get_last_table_index(table_name)

        file = self.__db_open_files[table_name]
        file.seek(0, os.SEEK_END)

        file.write(f"{current_index}$")
        for idx, d in enumerate(data):
            separator = "\n" if idx == (len(data) - 1) else "$"
            value = f"{d.table_name},{d.row_index}" if isinstance(d, Link) else str(d)
            file.write(f"{value}{separator}")

    def update_item(self, table_name: str, item_id: str, data: RowData):
        pass

    def delete_item(self, table_name: str, item_id: int):
        pass

    def show_item_list(self, table_name: str):
        self.__is_table_exist(table_name)

        file = self.__db_open_files[table_name]
        file.seek(0)

        for idx, line in enumerate(file):
            if idx == 0:
                for col in line.split(", "):
                    print(col.split("$")[0], end="   ")
                print()
            else:
                print(line.replace("$", "   "), end="")

    def get_item_list(self, table_name: str) -> list[RowData]:
        self.__is_table_exist(table_name)

        file = self.__db_open_files[table_name]
        file.seek(0)

        row_types: list[str] = self.get_table_row_types(table_name)
        return_data: list[RowData] = []

        for idx, line in enumerate(file):
            rows_data = [convert_to(item, EValueType(row_types[i])) for i, item in enumerate(line.split('$'))]
            return_data.append(RowData(rows_data))

        return return_data

    def get_item(self, table_name: str, item_id: int):
        pass

    def find_item_by_row(self, row):
        pass

    def __check_links(self, data: RowData):
        pass

    def __clear_variables(self):
        self.__path_to_db = "Empty"
        self.__db_name = "Empty"
        self.__db_tables = {}
        self.__db_open_files = {}

    def __get_last_table_index(self, table_name: str) -> int:
        file = self.__db_open_files[table_name]
        file.seek(0)

        last_idx: int = 0
        for _ in file:
            last_idx += 1

        return last_idx

    def __is_table_exist(self, name: str):
        if self.__db_tables.get(name) is None:
            raise Exception("A table with that name does not exist")

    def __del__(self):
        self.close()
