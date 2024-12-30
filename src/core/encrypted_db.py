import os
from typing import override, TextIO

from src.core.connection_pool import ConnectionPool
from src.core.data_cryptographer import DataCryptographer
from src.core.db_controller_base import DBControllerBase
from src.entities.link import Link
from src.entities.row_data import RowData
from src.entities.table import Table


class EncryptedDB(DBControllerBase):
    __db: DBControllerBase
    __path_to_original_db: str
    __path_to_encrypted_db: str
    __word_for_crypt: str
    __encoding: str = "utf-8"
    __connection_pool: ConnectionPool
    __db_open_file: TextIO

    def __init__(self, database: DBControllerBase, word_for_crypt: str = "None"):
        self.__connection_pool = ConnectionPool()
        self.__db = database
        self.__path_to_original_db = self.__connection_pool.get_path_to_db()
        self.__path_to_encrypted_db = self.__path_to_original_db + "_encryption_info"

        self.__word_for_crypt = word_for_crypt

        if not os.path.exists(self.__path_to_encrypted_db):
            with open(self.__path_to_encrypted_db, "w", encoding=self.__encoding) as file:
                w_f_c = DataCryptographer.offset_encrypt_data(word_for_crypt)
                file.write(w_f_c)
        else:
            with open(self.__path_to_encrypted_db, "r+", encoding=self.__encoding) as file:
                self.__word_for_crypt = DataCryptographer.offset_decrypt_data(file.readline())
                self.__decode_init_file()

        self.__db.late_init()

        self.__encode_init_file()
        self.__db_open_file = open(self.__path_to_encrypted_db, "r+", encoding=self.__encoding)

    @override
    def late_init(self):
        pass

    @override
    @property
    def db_name(self) -> str:
        return self.__db.db_name

    @override
    def add_tables(self, tables: list[Table]):
        self.__decode_file()
        self.__db.add_tables(tables)
        self.__encode_file()

    @override
    def delete_table(self, table_name: str):
        self.__decode_file()
        self.__db.delete_table(table_name)
        self.__encode_file()

    @override
    def get_table_names(self) -> list[str]:
        self.__decode_file()
        any_data = self.__db.get_table_names()
        self.__encode_file()
        return any_data

    @override
    def get_table_row_names(self, table_name: str) -> list[str]:
        self.__decode_file()
        any_data = self.__db.get_table_row_names(table_name)
        self.__encode_file()
        return any_data

    @override
    def get_table_row_types(self, table_name: str) -> list[str]:
        self.__decode_file()
        any_data = self.__db.get_table_row_types(table_name)
        self.__encode_file()
        return any_data

    @override
    def add_item(self, table_name: str, data: RowData):
        self.__decode_file()
        self.__db.add_item(table_name, data)
        self.__encode_file()

    @override
    def update_item(self, table_name: str, item_id: int, data: RowData):
        self.__decode_file()
        self.__db.update_item(table_name, item_id, data)
        self.__encode_file()

    @override
    def delete_item(self, table_name: str, item_id: int):
        self.__decode_file()
        self.__db.delete_item(table_name, item_id)
        self.__encode_file()

    @override
    def find_item_by_col_name(self, table_nane: str, col_name: str, col_value: any) -> any:
        self.__decode_file()
        any_data = self.__db.find_item_by_col_name(table_nane, col_name, col_value)
        self.__encode_file()
        return any_data

    @override
    def find_item_by_col_idx(self, table_nane: str, col_index: int, col_value: any) -> any:
        self.__decode_file()
        any_data = self.__db.find_item_by_col_idx(table_nane, col_index, col_value)
        self.__encode_file()
        return any_data

    @override
    def get_item_by_link(self, link: Link) -> any:
        self.__decode_file()
        any_data = self.__db.get_item_by_link(link)
        self.__encode_file()
        return any_data

    @override
    def show_item_list(self, table_name: str):
        self.__decode_file()
        self.__db.show_item_list(table_name)
        self.__encode_file()

    @override
    def get_item_list(self, table_name: str) -> list[RowData]:
        self.__decode_file()
        any_data = self.__db.get_item_list(table_name)
        self.__encode_file()
        return any_data

    @override
    def get_item(self, table_name: str, item_id: int) -> RowData:
        self.__decode_file()
        any_data = self.__db.get_item(table_name, item_id)
        self.__encode_file()
        return any_data

    def __encode_init_file(self):
        dc = DataCryptographer
        file = self.__connection_pool.get_connection(self.__db.db_name)

        file.seek(0)
        lines: list[str] = file.readlines()
        encode: str = dc.lzss_encrypt_data("".join(lines))
        encode = dc.offset_encrypt_data(encode, self.__word_for_crypt)
        file.seek(0)
        file.truncate(0)
        file.write(encode)

    def __decode_init_file(self):
        dc = DataCryptographer
        file = self.__connection_pool.get_connection(self.__path_to_original_db.rsplit("/", 1)[1])

        file.seek(0)
        lines: list[str] = file.readlines()
        decode: str = dc.offset_decrypt_data("".join(lines), self.__word_for_crypt)
        decode = dc.lzss_decrypt_data(decode)
        file.truncate(0)
        file.seek(0)
        file.write(decode)

    def __decode_file(self):
        dc = DataCryptographer
        file = self.__connection_pool.get_connection(self.__db.db_name)

        file.seek(0)
        lines: list[str] = file.readlines()
        decode: str = dc.offset_decrypt_data("".join(lines), self.__word_for_crypt)
        decode = dc.lzss_decrypt_data(decode)
        file.truncate(0)
        file.seek(0)
        file.write(decode)

        table_names: list[str] = self.__db.get_table_names()
        for table_name in table_names:
            file = self.__connection_pool.get_connection(table_name)

            file.seek(0)
            table_lines: list[str] = file.readlines()
            decode_table: str = dc.offset_decrypt_data("".join(table_lines), self.__word_for_crypt)
            decode_table = dc.lzss_decrypt_data(decode_table)
            file.truncate(0)
            file.seek(0)
            file.write(decode_table)

    def __encode_file(self):
        dc = DataCryptographer
        file = self.__connection_pool.get_connection(self.__db.db_name)

        file.seek(0)
        lines: list[str] = file.readlines()
        encode: str = dc.lzss_encrypt_data("".join(lines))
        encode = dc.offset_encrypt_data(encode, self.__word_for_crypt)
        file.seek(0)
        file.truncate(0)
        file.write(encode)

        table_names: list[str] = self.__db.get_table_names()
        for table_name in table_names:
            file = self.__connection_pool.get_connection(table_name)

            file.seek(0)
            table_lines: list[str] = file.readlines()
            decode_table: str = dc.lzss_encrypt_data("".join(table_lines))
            decode_table = dc.offset_encrypt_data(decode_table, self.__word_for_crypt)
            file.seek(0)
            file.truncate(0)
            file.write(decode_table)

    @override
    def delete_db(self):
        self.__db.delete_db()

        self.__db_open_file.close()

        if os.path.exists(self.__path_to_encrypted_db):
            os.remove(self.__path_to_encrypted_db)

    def __del__(self):
        self.__connection_pool.close_all_connections()