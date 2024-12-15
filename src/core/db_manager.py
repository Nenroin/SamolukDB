import os
from typing import TextIO
from src import EValueType, convert_to, convert_to_e_value_type
from src.entities.link import Link
from src.entities.row_data import RowData
from src.entities.table import Table


class DBManager:
    __path_to_db: str
    __db_name: str
    __db_table_max_ids: dict[str, int]
    __db_tables: dict[str, str]
    __db_open_files: dict[str, TextIO]

    def __init__(self, path_to_db: str = None):
        if path_to_db:
            self.open(path_to_db)
        else:
            self.__clear_variables()

    @property
    def db_name(self) -> str:
        return self.__db_name

    def open(self, path_to_db: str):
        if not os.path.exists(path_to_db):
            raise Exception("DB does not exist")

        self.__path_to_db = path_to_db
        self.__db_tables = {}
        self.__db_table_max_ids = {}
        temporary_db_name = "temporary_name"
        self.__db_open_files = {temporary_db_name: open(path_to_db, "r+")}

        file = self.__db_open_files[temporary_db_name]
        file.seek(0)

        for index, line in enumerate(file):
            if index == 0:
                self.__db_name = line.split("$")[1].rstrip("\n")
                self.__db_open_files[self.__db_name] = self.__db_open_files.pop(temporary_db_name)
            else:
                table_name, table_path, last_table_idx = [item.rstrip("\n") for item in line.split("$")]

                self.__db_tables[table_name] = table_path
                self.__db_open_files[table_name] = open(table_path, "r+")
                self.__db_table_max_ids[table_name] = int(last_table_idx)

    def close(self):
        for file in self.__db_open_files.values():
            file.close()

        self.__clear_variables()

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
            file.write(f"{table.name}${table_path + table.name}${1}\n")

            self.__db_table_max_ids[table.name] = 1
            self.__db_tables[table.name] = table_path + table.name

    def delete_table(self, table_name: str):
        self.__is_table_exist(table_name)

        self.__db_open_files[table_name].close()
        self.__db_open_files.pop(table_name)

        self.__delete_table_in_db_file(table_name)
        os.remove(self.__db_tables[table_name])

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
        self.__check_links(data)

        current_index: int = self.__db_table_max_ids[table_name]

        file = self.__db_open_files[table_name]
        file.seek(0, os.SEEK_END)

        file.write(f"{current_index}$")
        for idx, d in enumerate(data):
            separator = "\n" if idx == (len(data) - 1) else "$"
            value = f"{d.table_name},{d.row_id},{d.col_name}" if isinstance(d, Link) else str(d)
            file.write(f"{value}{separator}")

        current_index += 1
        self.__delete_table_in_db_file(table_name)

        file = self.__db_open_files[self.__db_name]
        file.seek(0, os.SEEK_END)
        file.write(f"{table_name}${self.__db_tables[table_name]}${current_index}\n")
        self.__db_table_max_ids[table_name] = current_index

    def update_item(self, table_name: str, item_id: int, data: RowData):
        self.__is_table_exist(table_name)
        data.check_types(self.get_table_row_types(table_name)[1:])
        self.__check_links(data)
        self.__is_row_exist(table_name, item_id)

        file = self.__db_open_files[table_name]
        file.seek(0)

        all_lines = file.readlines()
        file.seek(0)
        file.truncate(0)

        for line in all_lines:
            if line.split("$")[0] == str(item_id):
                new_line = f"{item_id}$"
                for idx, d in enumerate(data):
                    separator = "\n" if idx == (len(data) - 1) else "$"
                    value = f"{d.table_name},{d.row_id},{d.col_name}" if isinstance(d, Link) else str(d)
                    new_line += f"{value}{separator}"
                file.write(new_line)
            else:
                file.write(line)

    def delete_item(self, table_name: str, item_id: int):
        self.__is_table_exist(table_name)
        self.__is_row_exist(table_name, item_id)

        file = self.__db_open_files[table_name]
        file.seek(0)

        all_lines = file.readlines()
        file.seek(0)
        file.truncate(0)

        for line in all_lines:
            if line.split("$")[0] != str(item_id):
                file.write(line)

    def find_item_by_col_name(self, table_nane: str, col_name: str, col_value: any) -> any:
        self.__is_table_exist(table_nane)
        self.__is_col_exist(table_nane, col_name)

        cols_types: list[str] = self.get_table_row_types(table_nane)
        cols_names: list[str] = self.get_table_row_names(table_nane)

        col_index: int = 0
        for idx, i in enumerate(cols_names):
            if i == col_name:
                col_index = idx

        if convert_to_e_value_type(col_value) != EValueType(cols_types[col_index]):
            raise Exception("Incorrect column value type")

        lines = self.get_item_list(table_nane)

        for i in lines:
            if i[col_index] == col_value:
                return i

        return None

    def find_item_by_col_idx(self, table_nane: str, col_index: int, col_value: any) -> any:
        self.__is_table_exist(table_nane)
        self.__is_col_idx_exist(table_nane, col_index)

        cols_types: list[str] = self.get_table_row_types(table_nane)

        if convert_to_e_value_type(col_value) != EValueType(cols_types[col_index]):
            raise Exception("Incorrect column value type")

        lines = self.get_item_list(table_nane)

        for i in lines:
            if i[col_index] == col_value:
                return i

        return None

    def get_item_by_link(self, link: Link) -> any:
        self.__check_link(link)
        item_list:list[RowData] = self.get_item_list(link.table_name)

        cols_names: list[str] = self.get_table_row_names(link.table_name)

        col_index: int = 0
        for idx, i in enumerate(cols_names):
            if i == link.col_name:
                col_index = idx

        for i in item_list:
            if i[0] == link.row_id:
                return i[col_index]

        return None

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
            rows_data = [convert_to(item, EValueType(row_types[i])) for i, item in
                         enumerate(line.rstrip("\n").split('$'))]
            return_data.append(RowData(rows_data))

        return return_data

    def get_item(self, table_name: str, item_id: int) -> RowData:
        file = self.__db_open_files[table_name]

        row_types: list[str] = self.get_table_row_types(table_name)
        row_data: list

        for idx, line in enumerate(file):
            row_data = [convert_to(item, EValueType(row_types[i])) for i, item in
                        enumerate(line.rstrip("\n").split('$'))]
            if row_data[0] == item_id:
                return RowData(row_data)

        raise ValueError(f"Id {item_id} does not exist in the file.")

    def __delete_table_in_db_file(self, table_name: str):
        file = self.__db_open_files[self.__db_name]
        file.seek(0)

        for idx, line in enumerate(file):
            if line.rstrip("\n").split("$")[0] == table_name:
                file.seek(0)
                lines = file.readlines()
                del lines[idx]
                file.seek(0)
                file.truncate(0)
                file.writelines(lines)

    def __check_links(self, data: RowData):
        for link in data.get_links():
            self.__check_link(link)

    def __check_link(self, link: Link):
        self.__is_table_exist(link.table_name)
        self.__is_col_exist(link.table_name, link.col_name)
        self.__is_row_exist(link.table_name, link.row_id)

    def __clear_variables(self):
        self.__path_to_db = "Empty"
        self.__db_name = "Empty"
        self.__db_tables = {}
        self.__db_open_files = {}
        self.__db_table_max_ids = {}

    def __is_row_exist(self, table_name: str, row_id: int):
        rows_data: list[RowData] = self.get_item_list(table_name)
        for idx, row in enumerate(rows_data):
            if row[0] == row_id:
                return
        raise Exception(f"Row id: {row_id} does not exist in table '{table_name}'.")

    def __is_col_idx_exist(self, table_name: str, col_idx: int):
        if 0 <= col_idx < len(self.get_table_row_names(table_name)):
            return
        raise Exception(f"Column idx: '{col_idx}' does not exist in table '{table_name}'.")

    def __is_col_exist(self, table_name: str, col_name: str):
        columns = self.get_table_row_names(table_name)
        if col_name not in columns:
            raise Exception(
                f"Column '{col_name}' does not exist in table '{table_name}'.\nAvailable columns: {columns}")

    def __is_table_exist(self, name: str):
        if self.__db_tables.get(name) is None:
            raise Exception("A table with that name does not exist")

    def __del__(self):
        self.close()
