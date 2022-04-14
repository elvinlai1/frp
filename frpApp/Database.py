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

    def create_FaceTable(self):
        sql = ( 
            """
            CREATE TABLE face(
            emp_num VARCHAR PRIMARY KEY,
            emp_name TEXT NOT NULL, 
            emp_encodings BYTEA NOT NULL
            );
            """
        )
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

    def create_Timestamps(self):
        sql = ( 
            """
            CREATE TABLE timestamps(
            emp_num VARCHAR NOT NULL,
            emp_timestamp VARCHAR NOT NULL,
            emp_status VARCHAR NOT NULL
            );
            """
        )
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

    def register_NewFace(self, emp_num, emp_face):
        sql = ( 
            """
            INSERT INTO face (emp_num, emp_encodings)VALUES(%s,%s,%s);
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
            INSERT INTO timestamps (emp_num, emp_timestamp, emp_status)VALUES(%s,%s,%s);
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
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_AllTimestamp(self, emp_num):
        sql = ( """
                SELECT * FROM timestamps WHERE emp_num = %s ORDER BY emp_timestamp DESC; 
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
                SELECT * FROM timestamps WHERE emp_num = %s ORDER BY emp_timestamp DESC LIMIT 1; 
                """
        )
        try: 
            cur = self.conn.cursor()
            cur.execute(sql,[emp_num,])
            return cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

 
      


