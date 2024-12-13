from src import DBCreator, DBManager, Table, Column, EValueType

DBCreator.create_db("Library", "C:/Users/nenro/PycharmProjects/SamolukDB/")

db = DBManager("C:/Users/nenro/PycharmProjects/SamolukDB/Library")
print("DB name: ", db.name)


db.add_tables([
    Table("Books", [
        Column("name", EValueType.STRING),
        Column("author", EValueType.STRING),
        Column("pages", EValueType.INT)
    ]),
    Table("Workers", [
        Column("name", EValueType.STRING),
        Column("post", EValueType.STRING)
    ]),
])

print("Tables: ", db.get_table_names())
print("Rows of Workers: ", db.get_table_row_names("Books"))