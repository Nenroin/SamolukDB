from datetime import datetime

from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from starlette.responses import JSONResponse

from src.core.connection_pool import ConnectionPool
from src.core.db_manager import DBManager
from src.core.encrypted_db import EncryptedDB
from src.entities.link import Link
from src.entities.row_data import RowData

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/take-book")
def take_book(data = Body()):
    db = EncryptedDB(DBManager())

    user_name = data["userName"]
    book_name = data["bookName"]
    librarian_name = data["librarianName"]

    reader = db.find_item_by_col_name("readers", "name", user_name)
    book = db.find_item_by_col_name("books", "name", book_name)
    worker = db.find_item_by_col_name("workers", "name", librarian_name)

    if reader is not None and book is not None and worker is not None and book[4] != 1:
        db.add_item("check_list", RowData([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 1,
                                           Link("readers", reader[0], "name"),
                                           Link("workers", worker[0], "name"),
                                           Link("books", book[0], "name")]))
        new_book: RowData = RowData([book[1], book[2], book[3], 1])
        db.update_item("books", book[0], new_book)
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Не удалось найти какое-то из полей или книга не занята"}
        )

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Все успешно!"})

@app.post("/return-book")
def return_book(data = Body()):
    db = EncryptedDB(DBManager())

    user_name = data["userName"]
    book_name = data["bookName"]
    librarian_name = data["librarianName"]

    reader = db.find_item_by_col_name("readers", "name", user_name)
    book = db.find_item_by_col_name("books", "name", book_name)
    worker = db.find_item_by_col_name("workers", "name", librarian_name)

    if reader is not None and book is not None and worker is not None and book[4] != 0:
        db.add_item("check_list", RowData([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 0,
                                           Link("readers", reader[0], "name"),
                                           Link("workers", worker[0], "name"),
                                           Link("books", book[0], "name")]))
        new_book: RowData = RowData([book[1], book[2], book[3], 0])
        db.update_item("books", book[0], new_book)
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Не удалось найти какое-то из полей или книга уже занята"}
        )

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Все успешно!"})

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
    db = EncryptedDB(DBManager())

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