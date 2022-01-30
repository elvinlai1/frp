import sqlite3


class SqliteObject(object):
    def __init__(self, db):
        self.db = db
        self.con = sqlite3.connect(f'{db}')
        self.cur = self.con.cursor()

    def getCurSorObject(self):
        return self.cur

    def execSql(self, sql):
        try:
            self.cur.execute(sql)
            return self.cur
        except Exception as e:
            print(e)
            return None
