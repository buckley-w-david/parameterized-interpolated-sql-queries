import inspect
import ast, _ast

import sqlite3

db_conn = sqlite3.connect(":memory:")

def paramaterize_interpolated_querystring(query, placeholder='?'):
    frame = inspect.currentframe()
    outer_frame = inspect.getouterframes(frame)[1]
    tree = ast.parse(f"f'{query}'")
    values = tree.body[0].value.values

    paramaterized_query = ''
    query_values = []
    for node in values:
        if isinstance(node, _ast.Constant):
            paramaterized_query += node.value
        elif isinstance(node, _ast.FormattedValue):
            paramaterized_query += placeholder
            query_value = outer_frame.frame.f_locals[node.value.id]
            query_values.append(query_value)

    return (paramaterized_query, query_values)

f=paramaterize_interpolated_querystring

cursor = db_conn.cursor()
cursor.execute('''CREATE TABLE users (col1 int, col2 int, col3 int)''')

x = 1
y = 2
z = 3

cursor.execute(*f("INSERT INTO users (col1, col2, col3) VALUES ({x}, {y}, {z})"))
db_conn.commit()

cursor.execute("SELECT * FROM users")
print(cursor.fetchone())
