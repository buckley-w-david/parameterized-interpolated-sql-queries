import interpolate

f = interpolate.paramaterize_interpolated_querystring_spicy

x = 1
y = 2
z = 3

print(f('''INSERT INTO users (col1, col2, col3) VALUES ({x}, {y}, {z})'''))
print(f('''INSERT INTO users (col1, col2, col3) VALUES ({x+1}, {y+2}, {z+3})'''))
