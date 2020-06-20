import sqlite3
import interpolate

db_conn = sqlite3.connect(":memory:")

f=interpolate.paramaterize_interpolated_querystring

cursor = db_conn.cursor()
cursor.execute('''CREATE TABLE users (col1 int, col2 int, col3 int)''')

x = 1
y = 2
z = 3

cursor.execute(*f("INSERT INTO users (col1, col2, col3) VALUES ({x}, {y}, {z})"))

try:
    cursor.execute(*f("INSERT INTO users (col1, col2, col3) VALUES ({x+1}, {y+2}, {z+3})"))
except:
    # No evaluation within the interpolation, only variables
    pass

db_conn.commit()

cursor.execute("SELECT * FROM users")
print(cursor.fetchone())
