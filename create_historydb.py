import sqlite3

DBNAME = "history.db"

conn = sqlite3.connect(DBNAME)
c = conn.cursor()

c.execute("""CREATE TABLE history_data
             (title TEXT, content TEXT, date_type TEXT, date_str TEXT, days_since_beginning INT8)""")

c.execute("""CREATE TABLE history_not_visited_pages (url TEXT)""")
conn.close()
