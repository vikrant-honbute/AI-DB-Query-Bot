import sqlite3

#connect to sqlite
connection = sqlite3.connect("student.db")

#create a cursor object to insert record, create table
cursor = connection.cursor()

#create table
table_info= """
CREATE TABLE IF NOT EXISTS STUDENT(
    NAME VARCHAR(25),
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INT
)
"""


cursor.execute(table_info)

#Insert some more records
cursor.execute('''Insert Into STUDENT values('Vik','Data Science','A',90)''')
cursor.execute('''Insert Into STUDENT values('Nora','Data Science','A',80)''')
cursor.execute('''Insert Into STUDENT values('Krish','Data Science','A',70)''')
cursor.execute('''Insert Into STUDENT values('Karan','Data Science','A',60)''')
cursor.execute('''Insert Into STUDENT values('Yoo','Data Science','A',50)''')

## display all the records
print("the inserted records are")

data= cursor.execute('''Select * from STUDENT''')
for row in data:
    print(row)

## commit your changes in DB
connection.commit()
connection.close()