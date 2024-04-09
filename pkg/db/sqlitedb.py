import sqlite3

from pkg.db.db import Db, DbConnection


class SqliteDb(Db):
    def __init__(self):
        super().__init__()

    def doConnection(self, conn_str: str) -> DbConnection:    
        conn = sqlite3.connect(conn_str)
        return DbConnection(conn)
