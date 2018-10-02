import sqlite3
from functools import wraps


DBNAME = "history.db"
# store the connection to the database when in use
global conn_cursor

# this warps every function that deals with database
def manage_connection(func):
    @wraps(func)
    def connection_handler(*args, **kwargs):
        global conn_cursor

        conn = sqlite3.connect(DBNAME)
        conn_cursor = conn.cursor()

        value = func(*args, **kwargs)

        conn_cursor = None
        conn.commit()
        conn.close()

        return value
    return connection_handler


@manage_connection
def db_get_pages():
    global conn_cursor
    conn_cursor.execute("SELECT * FROM history_data")
    page_data = conn_cursor.fetchall()
    return page_data

# returns all data in the range start and end and count number of rows
@manage_connection
def db_get_pages_in_range(start, end, count=20, randomize=False):
    global conn_cursor
    
    if randomize:
        conn_cursor.execute("SELECT * FROM history_data WHERE days_since_beginning between ? AND ? ORDER BY RANDOM() limit ?", (start, end, count))
    else: 
        conn_cursor.execute("SELECT * FROM history_data WHERE days_since_beginning between ? AND ? ORDER BY days_since_beginning limit ?", (start, end, count))
    page_data = conn_cursor.fetchall()
    return page_data

# return True if the link was already visited else False
@manage_connection
def db_visited_already(title):
    global conn_cursor
    search = conn_cursor.execute("SELECT * FROM history_data WHERE title=?", (title, ))
    
    if search.fetchall():
        return True
    else:
        return False

# insert data into the history_data table
@manage_connection
def db_insert_data(title, content, date_type, date_str, days_since_beginning):
    global conn_cursor
    conn_cursor.execute("INSERT INTO history_data VALUES(?,?,?,?,?)", (title, content, date_type, date_str, days_since_beginning))

# insert all the pages that were to be visited in the table
# for later resuming the operation
@manage_connection
def db_insert_not_visited_urls(urls):
    global conn_cursor
    for url in urls:
        conn_cursor.execute("INSERT INTO history_not_visited_pages VALUES(?)", (url,))

@manage_connection
def db_delete_all_not_visite_urls():
    global conn_cursor
    conn_cursor.execute("DELETE from history_not_visited_pages")

@manage_connection
def db_get_next_visit_urls():
    global conn_cursor
    urls = conn_cursor.execute("SELECT * FROM history_not_visited_pages").fetchall()

    if urls:
        return urls