import psycopg2
import pickle

class Database: 
    #ensure all parameters are correct
    conn = psycopg2.connect("dbname=myproject user=myprojectuser password=password1 host=localhost")

    def check_Connection(self):
        try:
            cur = self.conn.cursor()
            print('PostgreSQL database version:')
            cur.execute('SELECT version()')
            db_version = cur.fetchone()
            print(db_version)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


    def register_NewFace(self, emp_num, emp_face):
        sql = ( 
            """
            INSERT INTO face (employee_number, encodings)VALUES(%s,%s);
            """
        )
        try: 
            cur = self.conn.cursor()
            cur.execute(sql,[emp_num, pickle.dumps(emp_face),])
            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()

    def register_Timestamp(self, emp_num, ts, emp_status):
        sql = ( 
            """
            INSERT INTO timestamps (employee_number, timestamp, status)VALUES(%s,%s,%s);
            """
        )
        try: 
            cur = self.conn.cursor()
            cur.execute(sql,[emp_num, ts, emp_status,])
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_AllFaces(self):
        sql = ( """
                SELECT * FROM face; 
                """
        )
        faces = []
        try: 
            cur = self.conn.cursor()
            cur.execute(sql)
            f = cur.fetchall()
            for x in f:
                l = [x[0], pickle.loads(x[1])]
                faces.append(l)
            return faces
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_Employee(self, emp_num):
        sql = (""" 
                SELECT employee_name FROM employees WHERE employee_number = %s; 
                """)
        try: 
            cur = self.conn.cursor()
            cur.execute(sql, [emp_num,])
            return cur.fetchone()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_AllTimestamp(self, emp_num):
        sql = ( """
                SELECT * FROM timestamps WHERE employee_number = %s ORDER BY timestamp DESC; 
                """
        )
        try: 
            cur = self.conn.cursor()
            cur.execute(sql,[emp_num,])
            return cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_LastTimestamp(self, emp_num):
        sql = ( """
                SELECT * FROM timestamps WHERE employee_number = %s ORDER BY timestamp DESC LIMIT 1; 
                """
        )
        try: 
            cur = self.conn.cursor()
            cur.execute(sql,[emp_num,])
            return cur.fetchone()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

 
      


