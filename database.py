import sqlite3

con = sqlite3.connect("database.db")
cur = con.cursor()

# Table Creation

# cur.execute("CREATE TABLE travel_data(source, destination, duration_in_min, destance)")