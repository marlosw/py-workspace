
from abc import abstractmethod


class DbConnection():
    def __init__(self, db):
        self.db = db

    def close(self):
        self.db.close()

class Db():    
    connections = {}
    def __init__(self):
        pass

    def connect(self, dbname: str, conn_str: str) -> DbConnection: 
        conn = self.connections.get(dbname)
        if conn is not None:
            return conn 
        conn = self.doConnection(conn_str) 
        self.connections[dbname] = conn
        return conn

    def disconnect(self, dbname: str):
        db = self.connections.get(dbname)
        db.close()
        self.connections.remove(dbname)

    @abstractmethod
    def doConnection(self, conn_str: str) -> DbConnection:
        pass   
    
    @staticmethod
    def getConnection(dbname: str) -> DbConnection:
        if dbname == '' and len(__class__.connections) > 0:
            return __class__.connections.get(list(__class__.connections.values())[0])
        return __class__.connections.get(dbname)


