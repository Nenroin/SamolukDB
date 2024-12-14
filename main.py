from src import EValueType, DBCreator, DBManager, Column, Table, Link, RowData

DBCreator.create_db("library", "C:/Users/nenro/PycharmProjects/SamolukDB/")

db = DBManager("C:/Users/nenro/PycharmProjects/SamolukDB/Library")

print("DB name: ", db.name)

db.add_tables([
    Table("books", [
        Column("name", EValueType.STRING),
        Column("author", EValueType.STRING),
        Column("pages", EValueType.INT)
    ]),
    Table("workers", [
        Column("name", EValueType.STRING),
        Column("post", EValueType.STRING),
        Column("link", EValueType.LINK),
    ]),
])


print("Tables: ", db.get_table_names())
print("Rows of Workers names: ", db.get_table_row_names("books"))
print("Rows of Workers types: ", db.get_table_row_types("books"))

print("Rows of Workers names: ", db.get_table_row_names("workers"))
print("Rows of Workers types: ", db.get_table_row_types("workers"))

db.add_item("workers", RowData(["Andrey", "Director", Link("books", 1)]))
db.add_item("workers", RowData(["Kirill", "Director", Link("books", 2)]))
db.add_item("workers", RowData(["Artem", "Director", Link("books", 3)]))
db.add_item("workers", RowData(["Dima", "Director", Link("books", 4)]))


for i in db.get_item_list("workers"):
    print(i)

print()
db.show_item_list("workers")

db.close()

DBCreator.delete_db("C:/Users/nenro/PycharmProjects/SamolukDB/Library")