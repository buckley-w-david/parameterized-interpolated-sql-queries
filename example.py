import sqlite3
import interpolate

db_conn = sqlite3.connect(":memory:")

f=interpolate.parameterize_interpolated_querystring

cursor = db_conn.cursor()
cursor.execute('''CREATE TABLE users (col1 int, col2 int, col3 int)''')

x = 1
y = 2
z = 3

global_var = "Hello, world!"

def do_something_crazy(value):
    global global_var
    global_var = "I am bad code"
    return value * 17

cursor.execute(*f("INSERT INTO users (col1, col2, col3) VALUES ({x}, {y}, {z})"))
cursor.execute(*f("INSERT INTO users (col1, col2, col3) VALUES ({x+1}, {y+2}, {z+3})"))
cursor.execute(*f("INSERT INTO users (col1, col2, col3) VALUES ({do_something_crazy(x+8)}, {y+9}, {z+10})"))

db_conn.commit()

cursor.execute(*f("SELECT * FROM users WHERE col1 = {x}"))
print(cursor.fetchone())

cursor.execute(*f("SELECT * FROM users WHERE col2 = {y+2}"))
print(cursor.fetchone())

cursor.execute(*f("SELECT * FROM users WHERE col3 = {z+10}"))
print(cursor.fetchone())

db_conn.close()

# Side effects of calls within the interpolation carry over correctly
print(global_var)
