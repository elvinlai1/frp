import sqlite3
from .timeUtils import time_format


# user table
class User(object):
    def __init__(self, first_name, last_name, email, department, wage_per_hour, face_encodings):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.department = department
        self.wage_per_hour = wage_per_hour
        self.face_encodings = face_encodings


class Work(object):
    def __init__(self, employee, department, in_time, out_time, hours, work_time, deduction='', notes=''):
        self.employee = employee
        self.department = department
        self.in_time = in_time
        self.out_time = out_time
        self.hours = hours
        self.work_time = work_time
        self.deduction = deduction
        self.notes = notes


class RaceSqlite(object):

    def __init__(self, db):
        self.db = db
        self.con = sqlite3.connect(f'{db}')
        self.cur = self.con.cursor()

    def insert_user(self, user):
        sql = "insert into race_user(first_name,last_name,email,department,wage_per_hour,face_encodings,create_time) values(?,?,?,?,?,?,?)"
        try:
            if isinstance(user, User):
                data = (
                user.first_name, user.last_name, user.email, user.department, user.wage_per_hour, user.face_encodings,
                time_format())
                self.cur.execute(sql, data)
                self.con.commit()
                return True
            else:
                return False
        except Exception as e:
            print(f'insert error {str(e)}')
            return True

    # exist user by first_name last_name
    def find_exist_user(self, first_name, last_name):
        sql = "select * from race_user where first_name = %s and last_name = %s"
        result = self.cur.execute(sql, (first_name, last_name)).fetchone()
        return True if result is not None else False

    def getCurSorObject(self):
        return self.cur

    def execSql(self, sql):
        try:
            self.cur.execute(sql)
            return self.cur
        except Exception as e:
            print(e)
            return None
