import psycopg2

class Database: 
    #connect to Postgresql
    conn = psycopg2.connect("dbname=myproject user=myprojectuser password=password1 host=localhost")

    def check_connection(self):
        try:
            cur = self.conn.cursor()
            print('PostgreSQL database version:')
            cur.execute('SELECT version()')
            db_version = cur.fetchone()
            print(db_version)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def create_table(self):
        sql = (
            """
            CREATE TABLE users(
            id SERIAL PRIMARY KEY,
            First NAME TEXT NOT NULL,
            Last Name TEXT NOT NULL,
            Employee Number INT NOT NULL
            
            )
            """)
        try:
            cur = self.conn.cursor()
            # create table one by one
            cur.execute(sql)
            # close communication with the PostgreSQL database server
            cur.close()
            # commit the changes
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()

    def insert(self,arr):
        sql = ( 
        """
        INSERT INTO users (id, first_name, last_name, face_encodings) VALUES(DEFAULT, %s, %s, %s);
        """
        )

        try: 
            cur = self.conn.cursor()
            cur.execute(sql,(arr))
            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()

    def addNewEmployee(self, arr):
        sql = ( 
            """
            INSERT INTO users (emp_num, first_name, last_name, face_encodings) VALUES(DEFAULT, %s, %s, %s);
            """
        )
            

class Employee(object):
    def __init__(self, empNum, fName, lName, face_encodings):
        self.empNum = empNum
        self.fName = fName
        self.lName = lName
        self.face_encodings = face_encodings
       


