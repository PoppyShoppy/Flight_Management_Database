import sqlite3

class DBConnection:
    DB_NAME = "DATABASE.db"

    @staticmethod
    def get_connection():
        return sqlite3.connect(DBConnection.DB_NAME)