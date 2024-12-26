import os
from typing import TextIO


class ConnectionPool:
    __is_activate: bool = False
    __path_to_db: str = "C:/Users/nenro/PycharmProjects/SamolukDB/db/library"
    __db_open_files: dict[str, TextIO] = {}

    def __init__(self):
        ConnectionPool.__check()

    @staticmethod
    def close_connection(file_name: str):
        ConnectionPool.__db_open_files[file_name].close()

    @staticmethod
    def get_connection(file_name: str) -> TextIO:
        return ConnectionPool.__db_open_files[file_name]

    @staticmethod
    def set_connection(file_name: str, connection: TextIO) -> None:
        if file_name not in ConnectionPool.__db_open_files:
            ConnectionPool.__db_open_files[file_name] = connection
        else:
            #raise Exception("You try to open existing connection")
            pass

    @staticmethod
    def get_path_to_db() -> str:
        return ConnectionPool.__path_to_db

    @staticmethod
    def close_all_connections():
        for file in ConnectionPool.__db_open_files.values():
            if not file.closed:
                file.close()

    @staticmethod
    def __check():
        if os.path.exists(ConnectionPool.__path_to_db):
            if ConnectionPool.__path_to_db.rsplit("/", 1)[1] not in ConnectionPool.__db_open_files:
                ConnectionPool.__db_open_files = {
                    ConnectionPool.__path_to_db.rsplit("/", 1)[1]: open(ConnectionPool.__path_to_db, "r+", encoding="utf-8")}
        else:
            ConnectionPool.__db_open_files = {}
