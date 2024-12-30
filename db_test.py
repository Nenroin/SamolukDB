from datetime import datetime

from src import EValueType, DBCreator, DBManager, Column, Table, Link, RowData
from src.core.encrypted_db import EncryptedDB


def main():
    DBCreator.create_db("library", "C:/Users/nenro/PycharmProjects/SamolukDB/db/")
    db = EncryptedDB(DBManager())

    db.add_tables([
        Table("books", [
            Column("name", EValueType.STRING),
            Column("author", EValueType.STRING),
            Column("pages", EValueType.INT),
            Column("is_taken", EValueType.INT),
        ]),
        Table("workers", [
            Column("name", EValueType.STRING),
            Column("post", EValueType.STRING)
        ]),
        Table("readers", [
            Column("name", EValueType.STRING),
            Column("age", EValueType.INT)
        ]),
        Table("check_list", [
            Column("date", EValueType.STRING),
            Column("deal_type", EValueType.INT),
            Column("reader", EValueType.LINK),
            Column("worker", EValueType.LINK),
            Column("book", EValueType.LINK),
        ])
    ])


def print_db_info():
    db = EncryptedDB(DBManager())

    print(db.get_table_names())
    for table_name in db.get_table_names():
        print(table_name)
        print(db.get_table_row_names(table_name))
        print(db.get_table_row_types(table_name))


    db.add_item("workers", RowData(["Огурцова Анна Михайловна", "библиотекарь"]))
    db.add_item("workers", RowData(["Иванова Мария Ивановна", "старший библиотекарь"]))
    db.add_item("readers", RowData(["Марзан Андрей Николаевич", 20]))
    db.add_item("readers", RowData(["Марзан Андрей Николаевич", 21]))
    db.add_item("readers", RowData(["Ничингер Кирилл Александрович", 20]))
    db.add_item("books", RowData(["Преступление и наказание", "Федор Михайлович Достоевский", 687, 0]))
    db.add_item("books", RowData(["Война и мир", "Лев Николаевич Толстой", 2897, 1]))
    db.add_item("check_list", RowData([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 1,
                         Link("readers", 1, "name"),
                         Link("workers", 1, "name"),
                         Link("books", 2, "name")]))

    for table_name in db.get_table_names():
        print(table_name)
        for i in db.get_item_list(table_name):
            print(i)


if __name__ == "__main__":
    main()
    print_db_info()
