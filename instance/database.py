from psycopg2 import pool


class Database:
    __connection_pool = None

    @classmethod
    def initialize(cls):
        cls.__connection_pool = pool.SimpleConnectionPool(1,
                                                          10,
                                                          user='ben',
                                                          password='asdf',
                                                          database='rides',
                                                          host='localhost')

    @classmethod
    def get_conn(cls):
        return cls.__connection_pool.getconn()

    @classmethod
    def return_conn(cls, conn):
        return cls.__connection_pool.putconn(conn)

    @classmethod
    def close_all_connections(cls):
        Database.__connection_pool.closeall()


class CursorFromConnectionFromPool:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = Database.get_conn()
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            self.conn.rollback()
        else:
            self.cursor.close()
            self.conn.commit()
        Database.return_conn(self.conn)
