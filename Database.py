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
            Name TEXT NOT NULL,
            Clock_in TEXT NOT NULL,
            Clock_out TEXT NOT NULL
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
        INSERT INTO users (id, Name, Clock_in, Clock_out) VALUES(DEFAULT, %s, %s, %s);
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
