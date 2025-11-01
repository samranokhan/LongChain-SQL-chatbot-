import sqlite3

# connect to the SQLite database
connection = sqlite3.connect('student.db')

# create a cursor object
cursor = connection.cursor()

# drop table if exists
cursor.execute("DROP TABLE IF EXISTS STUDENT")

# create a table
table_info = """
CREATE TABLE STUDENT(
    Name VARCHAR(50) NOT NULL,
    Age INTEGER NOT NULL,
    CLASS VARCHAR(50),
    SECTION VARCHAR(50),
    MARKS INT
);
"""
cursor.execute(table_info)

# insert some records
cursor.execute("INSERT INTO STUDENT VALUES('John', 20, 'BCA', 'A', 85)")
cursor.execute("INSERT INTO STUDENT VALUES('Alice', 22, 'BBA', 'B', 90)")   
cursor.execute("INSERT INTO STUDENT VALUES('Bob', 21, 'BCA', 'A', 75)")
cursor.execute("INSERT INTO STUDENT VALUES('Charlie', 23, 'BBA', 'C', 88)")
cursor.execute("INSERT INTO STUDENT VALUES('David', 20, 'BCA', 'B', 92)")

# display all records
print("the inserted records are:")
data = cursor.execute("SELECT * FROM STUDENT")
for row in data:
    print(row)

# commit the changes
connection.commit()
connection.close()
