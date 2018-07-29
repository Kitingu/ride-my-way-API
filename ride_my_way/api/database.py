import psycopg2
from psycopg2 import pool




class Database:
    connection_pool = None
    @classmethod
    def initialise(cls):
        Database.connection_pool = pool.SimpleConnectionPool(1,
                                                             10,
                                                             user='ben',
                                                             password='asdf',
                                                             database='rides',
                                                             host='localhost')

    @classmethod
    def get_connection(cls):
        return cls.connection_pool.getconn()

    @classmethod
    def return_connections(cls, connection):
        Database.connection_pool.put_conn(connection)

    @classmethod
    def close_all_connections(cls):
        Database.connection_pool.closeall()





class CursorFromConnectionfromPool:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = Database.get_connection()
        self.cursor = self.connection.cursor
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            self.connection.rollback()
        else:
            self.cursor.close()
            self.connection.commit()
        Database.return_connections(self.connection)
