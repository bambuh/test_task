import sqlite3

con = sqlite3.connect('test.db')
with open('dump.sql', 'w') as f:
    for line in con.iterdump():
        f.write('%s\n' % line.encode('UTF-8'))


