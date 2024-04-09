from abc import abstractmethod
from pandas import DataFrame

from pkg.db.db import DbConnection


class BaseRepository():

    def __init__(self, conn: DbConnection):
        self.conn = conn

    def saveDataframe(self, df : DataFrame, table_name: str, if_exists='replace'):               
        df.to_sql(table_name, self.conn.db, if_exists=if_exists)

    def execute(self, sql: str, params: tuple):
        cursor = self.conn.db.execute(sql, params)
        return cursor.fetchall()
       