from src import EValueType, DBCreator, DBManager, Column, Table, Link, RowData

DBCreator.create_db("library", "C:/Users/nenro/PycharmProjects/SamolukDB/")

db = DBManager("C:/Users/nenro/PycharmProjects/SamolukDB/Library")

print("DB name: ", db.db_name)

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
print("Rows of books names: ", db.get_table_row_names("books"))
print("Rows of books types: ", db.get_table_row_types("books"))

print("Rows of Workers names: ", db.get_table_row_names("workers"))
print("Rows of Workers types: ", db.get_table_row_types("workers"))

db.add_item("books", RowData(["Adventure_1", "Aboba_1", 604]))
db.add_item("books", RowData(["Adventure_2", "Aboba_2", 234]))
db.add_item("books", RowData(["Adventure_3", "Aboba_3", 102]))
db.add_item("books", RowData(["Adventure_4", "Aboba_4", 435]))
db.add_item("books", RowData(["Adventure_5", "Aboba_5", 904]))

db.add_item("workers", RowData(["Andrey", "Director", Link("books", 1, "name")]))
db.add_item("workers", RowData(["Kirill", "Director", Link("books", 2, "name")]))
db.add_item("workers", RowData(["Artem", "Director", Link("books", 3, "name")]))
db.add_item("workers", RowData(["Dima", "Director", Link("books", 4, "name")]))

print()
db.show_item_list("books")
print()
db.show_item_list("workers")
print()
print(db.get_item("books", 4))
print(db.get_item("books", 3))

db.update_item("workers", 2, RowData(["Kirill", "Boss", Link("books", 3, "name")]))

print("\n=================================\n")
for i in db.get_item_list("workers"):
    print([j for j in i])

db.delete_item("workers", 1)
db.delete_item("workers", 3)

print()
db.show_item_list("workers")

print()
print(db.get_item("workers", 2))
print()
print(db.find_item_by_col_name("books", "author", "Aboba_1"))
print(db.find_item_by_col_idx("books", 2, "Aboba_1"))

print(db.get_item_by_link(Link("books", 1, "author")))

db.delete_table("books")
db.close()



DBCreator.delete_db("C:/Users/nenro/PycharmProjects/SamolukDB/Library")