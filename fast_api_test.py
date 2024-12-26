from fastapi import FastAPI, Body

from src.core.db_manager import DBManager
from src.core.encrypted_db import EncryptedDB
from src.entities.link import Link
from src.entities.row_data import RowData

app = FastAPI()
db = EncryptedDB(DBManager())

@app.post("/")
def read_root(data = Body()):
    name = data["name"]
    age = data["age"]
    return {"message": f"{name}, ваш возраст - {age}"}

@app.get("/readers")
def get_readers():
    return get_table_info_for_response("readers")

@app.get("/workers")
def get_workers():
    return get_table_info_for_response("workers")

@app.get("/books")
def get_books():
    return get_table_info_for_response("books")

@app.get("/check-list")
def get_check_list():
    return get_table_info_for_response("check_list")


def get_table_info_for_response(table_name: str) -> list[dict[str,str]]:
    readers: list[RowData] = db.get_item_list(table_name)
    col_names: list[str] = db.get_table_row_names(table_name)
    response_from_db: list[dict[str,str]] = []

    for reader in readers:
        body_str: dict[str, str] = {}

        for i, col_name in enumerate(col_names):
            cur_value = reader[i]
            if isinstance(cur_value, Link):
                body_str[col_name] = str(db.get_item_by_link(cur_value))
            else:
                body_str[col_name] = str(cur_value)

        response_from_db.append(body_str)

    return response_from_db