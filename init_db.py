import sqlite3
con = sqlite3.connect('test.db')
with open('dump.sql', 'r') as f:
    con.executescript(f.read())