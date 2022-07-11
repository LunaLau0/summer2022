import pymysql
import pymongo
import urllib

class MySQLConn(object):
    def __init__(self, host, port, user, password, dbname):
        self.conn = pymysql.connect(host=host, user=user, password=password, db=dbname, port=port)
        self.cursor = self.conn.cursor()

    def excute_one(self, conmm):
        self.cursor.execute(conmm)
        res = self.cursor.fetchone()
        if res is None:
            return None
        else:
            return res[0]

    def excute_all(self, conmm):
        self.cursor.execute(conmm)
        return self.cursor.fetchall()

    def insert(self, conmm):
        x = self.cursor.execute(conmm)
        if x > 0:
            self.conn.commit()
        else:
            self.conn.rollback()
        return x

class MongoConn(object):
    def __init__(self, host, port, user, password, dbname):
        self.conn = pymongo.MongoClient(f'mongodb://{urllib.parse.quote_plus(user)}:{urllib.parse.quote_plus(password)}@{host}:{port}')
        self.cursor = self.conn[dbname]

    def __del__(self):
        self.conn.close()