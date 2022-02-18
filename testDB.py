import psycopg2

#Temp way of connecting to database
#conn = psycopg2.connect("dbname=myproject user=myprojectuser password=password1 host=localhost")

def connect():
    conn = None
    try:
 
        conn = psycopg2.connect("dbname=myproject user=myprojectuser password=password1 host=localhost")
	
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def create_tables():
    conn = None
    """ create tables in the PostgreSQL database"""
    sql = (
        """
        CREATE TABLE vendors (
            vendor_id SERIAL PRIMARY KEY,
            vendor_name VARCHAR(255) NOT NULL
        )
        """,
        """ CREATE TABLE parts (
                part_id SERIAL PRIMARY KEY,
                part_name VARCHAR(255) NOT NULL
                )
        """,
        """
        CREATE TABLE part_drawings (
                part_id INTEGER PRIMARY KEY,
                file_extension VARCHAR(5) NOT NULL,
                drawing_data BYTEA NOT NULL,
                FOREIGN KEY (part_id)
                REFERENCES parts (part_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE vendor_parts (
                vendor_id INTEGER NOT NULL,
                part_id INTEGER NOT NULL,
                PRIMARY KEY (vendor_id , part_id),
                FOREIGN KEY (vendor_id)
                    REFERENCES vendors (vendor_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (part_id)
                    REFERENCES parts (part_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
        )
        """)
    try:
        conn = psycopg2.connect("dbname=myproject user=myprojectuser password=password1 host=localhost")
        cur = conn.cursor()
        # create table one by one
        for sql in sql:
            cur.execute(sql)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def get_tables():
    conn = None
    """ query data from the vendors table """

    try:
        conn = psycopg2.connect("dbname=myproject user=myprojectuser password=password1 host=localhost")
        cur = conn.cursor()
        cur.execute("SELECT vendor_id, vendor_name FROM vendors ORDER BY vendor_name")
        print("The number of parts: ", cur.rowcount)
        row = cur.fetchone()

        while row is not None:
            print(row)
            row = cur.fetchone()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_vendor_list(vendor_list):
    """ insert multiple vendors into the vendors table  """
    sql = "INSERT INTO vendors(vendor_name) VALUES(%s)"
    conn = None
    try:
    
        conn = psycopg2.connect("dbname=myproject user=myprojectuser password=password1 host=localhost")
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.executemany(sql,vendor_list)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_vendor(vendor_name):
    """ insert a new vendor into the vendors table """
    sql = """INSERT INTO vendors(vendor_name)
             VALUES(%s) RETURNING vendor_id;"""
    conn = None
    vendor_id = None
    try:
        
        conn = psycopg2.connect("dbname=myproject user=myprojectuser password=password1 host=localhost")
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (vendor_name,))
        # get the generated id back
        vendor_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return vendor_id

def drop_tables():
    conn = None
    """ create tables in the PostgreSQL database"""
    sql = (
        """
        TRUNCATE TABLE vendors CASCADE
        """,
         """
        DROP TABLE vendors CASCADE
        """,
        """ 
        TRUNCATE TABLE parts CASCADE
        """,
        """
        DROP TABLE parts CASCADE
        """,
        """
        TRUNCATE TABLE part_drawings CASCADE
        """,
        """
        DROP TABLE part_drawings CASCADE
        """,
        """
        TRUNCATE TABLE vendor_parts CASCADE
        """,
        """
        DROP TABLE vendor_parts CASCADE
        """)
    try:
        conn = psycopg2.connect("dbname=myproject user=myprojectuser password=password1 host=localhost")
        cur = conn.cursor()
        # create table one by one
        for sql in sql:
            cur.execute(sql)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    print('Testing Connection...\n')
    connect()
    print('\nCreating Test Table...')
    create_tables()
    print('Inserting Data...')
    insert_vendor("3M Co.")
    insert_vendor_list([
        ('AKM Semiconductor Inc.',),
        ('Asahi Glass Co Ltd.',),
        ('Daikin Industries Ltd.',),
        ('Dynacast International Inc.',),
        ('Foster Electric Co. Ltd.',),
        ('Murata Manufacturing Co. Ltd.',)
    ])
    print('Retrieving Data...')
    get_tables()
    print('\nDeleting All Tables and Data for Next Test\n')
    drop_tables()
