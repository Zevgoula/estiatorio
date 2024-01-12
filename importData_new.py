import sqlite3

conn = sqlite3.connect("SmartRestaurant.db")
cursor = conn.cursor()

tables = {
    "PELATIS": 6,
    "KRATISI": 3,
    "TRAPEZI": 3,
    "KRITIKI": 4,
    "PARAGGELIA": 3,
    "MAGEIRAS": 6,
    "SERVITOROS": 6,
    "PROMITHEYTIS": 4,
    "YLIKA": 3,
    "FAGITO": 4,
    "POTO": 3,
    "PARASKEYAZEI": 2,
    "APOTELEITAI": 2,
    "PERILAMBANEI": 2,
    "ANALAMBANEI": 2,
    "EFODIAZEI": 2,
    "PROMITHEVEI": 3,
}


def get_num_of_columns(table_name):
    cursor.execute(f"PRAGMA table_info({table_name});")
    return len(cursor.fetchall())


def insert_data(tablename, data):
    try:
        num_columns = tables[tablename]
        placeholders = ",".join(["?" for _ in range(num_columns)])
        cursor.execute("PRAGMA table_info({});".format(tablename))
        if num_columns != len(cursor.fetchall()):
            insert_query = "INSERT INTO {} VALUES (NULL,{});".format(tablename, placeholders)

        else:
            insert_query = "INSERT INTO {} VALUES ({});".format(tablename, placeholders)

        print(insert_query)
        print(data)

        # Execute the query with the data
        cursor.execute(insert_query, data)
        conn.commit()  # Don't forget to commit the changes

        print("Data inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


for tablename in tables:
    file = open(tablename + ".txt", "r", encoding="utf-8")
    for line in file:
        # Split the line into values and convert them to a tuple
        data = tuple(line.strip().split(', '))
        insert_data(tablename, data)

# Close the connection
conn.close()
