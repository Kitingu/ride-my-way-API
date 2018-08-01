from instance.database import CursorFromConnectionFromPool

def create_create_table():
    with CursorFromConnectionFromPool as cursor:
        cursor.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username text, password text")