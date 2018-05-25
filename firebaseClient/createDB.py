import sqlite3

create_query = "CREATE TABLE personEvent(id INTEGER PRIMARY KEY AUTOINCREMENT, tstamp TIMESTAMP, type TEXT)"

conn = sqlite3.connect('local.db')
c = conn.cursor()
c.execute(create_query)