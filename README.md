# Parameterized Interpolated SQL Queries

String interpolation + SQL queries = good user experience (😊) + sql injection (😞)

paramaterization + SQL queries = bad user experience (😞) + safety (😊)

The main issue is the bad version (string interpolation) is the natural way to express the idea you're trying to get across, the "correct" way is much less obvious.

## Why not the best of both worlds?

By (ab)using the `inspect` and `ast` modules, we can have the ease of use of string interpolation AND the safety of paramaterized queries!

String interpolation (BAD)
```python
x = 1
y = 2
z = 3

cursor.execute(f"INSERT INTO users (col1, col2, col3) VALUES ({x}, {y}, {z})")
```

Paramaterized query (Better)
```python
x = 1
y = 2
z = 3

cursor.execute("INSERT INTO users (col1, col2, col3) VALUES (?, ?, ?)", [x, y, z])
```

Paramaterized query with (almost) string interpolation sytax (Best?)
```python
f=paramaterize_interpolated_querystring

x = 1
y = 2
z = 3

cursor.execute(*f("INSERT INTO users (col1, col2, col3) VALUES ({x}, {y}, {z})"))
```

Go check out `interpolate.py` for the magic (it's in the `paramaterize_interplated_querystring` function)

## Note
Don't actually use this, it's just a neat idea I had
