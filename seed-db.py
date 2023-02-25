import csv
import sqlite3

# this code is for dev purposes -- don't run after more data is put in
# even though I guess it wouldn't even work since there would be primary key conflicts
connection = sqlite3.connect('database.db')

# Creating a cursor object to execute
# SQL queries on a database table
cursor = connection.cursor()

file = open('duck_db_seed.csv')
contents = csv.reader(file)

# not including dates because we don't know those yet
insert_records = "INSERT INTO duck (week_num, building, " \
                 "floor, height, rep_number, duck_id) " \
                 "VALUES(?, ?, ?, ?, ?, ?)"

cursor.executemany(insert_records, contents)

select_all = "SELECT * FROM duck"
rows = cursor.execute(select_all).fetchall()

for r in rows:
    print(r)

# Committing the changes
connection.commit()

# closing the database connection
connection.close()