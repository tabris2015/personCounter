import sqlite3

create_query = "CREATE TABLE personEvent(id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TIMESTAMP, tipo_marcado TEXT, id_sensor INTEGER)"

conn = sqlite3.connect('local.db')
c = conn.cursor()
c.execute(create_query)