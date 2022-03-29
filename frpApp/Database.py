import psycopg2
import pickle

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

    def create_faceTable(self):
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

    def create_metadataTable(self):
        sql = ( 
            """
            CREATE TABLE employeeClock(
            emp_num VARCHAR PRIMARY KEY,
                TEXT NOT NULL, 
            emp_encodings BYTEA NOT NULL
            );
            """
        )
    def registerNewFace(self, empNum, empName, face):
        sql = ( 
            """
            INSERT INTO face (emp_num, emp_name, emp_encodings)VALUES(%s,%s,%s);
            """
        )
        try: 
            cur = self.conn.cursor()
            cur.execute(sql,[empNum, empName, pickle.dumps(face),])
            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()

    def getEmp(self, emp_encodings):
        sql = ( """
                SELECT emp_num FROM face WHERE emp_encodings = %s
                """
        )
        try: 
            cur = self.conn.cursor()
            cur.execute(sql,[emp_encodings,])

            face = pickle.loads(cur.fetchone()[0])
            return face
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


    def getEmpFace(self, empNum):
        sql = ( """
                SELECT emp_encodings FROM face WHERE emp_num = %s
                """
        )
        try: 
            cur = self.conn.cursor()
            cur.execute(sql,[empNum,])

            face = pickle.loads(cur.fetchone()[0])
            return face
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
  

    def getAllFaces(self):
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
                l = [x[0], x[1], pickle.loads(x[2])]
                faces.append(l)


            return faces
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
      


