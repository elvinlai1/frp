import datetime
import time
import cv2
import face_recognition
from sqliteCon import SqliteObject

sqliteObject = None


# Make array of sample pictures with encodings
known_face_encodings = []
known_face_names = []


# Convert object to a string according to a given format
def time_format(string):
    return datetime.datetime.strftime(string, '%Y-%m-%d %H:%M:%S')


# Parse a string into a datetime object given a corresponding format
def format_time(string):
    return datetime.datetime.strptime(string, '%Y-%m-%d %H:%M:%S')


def comparingFace(locations, face_encodings, img):
    # search through locations for face
    # location：top、right、bottom、left
    for (top, right, bottom, left), face_encoding in zip(locations, face_encodings):
        # Compare faces
        matchs = face_recognition.compare_faces(known_face_encodings, face_encoding, 0.4)
        name = 'unknown'
        for match, known_name in zip(matchs, known_face_names):
            if match:
                name = known_name
                sql = "select * from users where name='%s'" % name
                oneUser = sqliteObject.execSql(sql).fetchone()
                if oneUser is None:
                    print(f'{name} insert clock_in info')
                    insertSql = 'insert into users (`name`, face_data, clock_in,clock_out) values(?,?,?,?)'
                    sqliteObject.cur.execute(insertSql,
                                             (name, known_face_encodings[0], time_format(datetime.datetime.now()), ''))
                    sqliteObject.con.commit()
                    print('Clock in successfully!\n')
                else:
                    dt = datetime.datetime.now()
                    print(oneUser[3])
                    dl = format_time(oneUser[3])
                    delta = int((str(dt - dl)[0:2]).replace(':',""))
                    # Time difference
                    if delta < 8:
                        print('time between clock in and out less than 8 hours')
                    else:
                        print('Update clock out time\n')
                        updateSql = 'UPDATE users SET clock_out=? WHERE name=?'
                        print(f'{name} update clock_out info')
                        sqliteObject.cur.execute(updateSql, (time_format(datetime.datetime.now()), name))
                        sqliteObject.con.commit()
                break
        # Show face loacation using rectangle
        cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
        # Show face name
        cv2.putText(img, name, (left, top - 10), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 2, (0, 0, 255))


def main():

    global known_face_encodings
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        # Returns a bool(True/False).
        # If the frame is read correctly, it will be True
        ret, img = cap.read()
        if not ret:
            print('No video captured!')
            break
        # Find face location
        locations = face_recognition.face_locations(img)
        # Face_encoding
        # https://github.com/ageitgey/face_recognition/issues/178
        face_encodings = face_recognition.face_encodings(img, locations)
        if len(known_face_encodings) == 0:
            known_face_encodings = face_encodings
        else:
            comparingFace(locations, face_encodings, img)
        cv2.namedWindow("enhanced", 0)
        cv2.resizeWindow("enhanced", 640, 480)
        cv2.moveWindow("enhanced", 500, 100)
        cv2.imshow('enhanced', img)

        # Press q to stop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            sqliteObject.cur.close()
            sqliteObject.con.close()
            # Close camera
            cap.release()
            # Close windows
            cv2.destroyAllWindows()
            # End loop
            break


if __name__ == '__main__':
    name = input('Please enter name:')
    known_face_names = [name]
    sqliteObject = SqliteObject('../userFace.db')
    try:
    #  DROP TABLE IF EXISTS "users" delete table
    #  Create table
        sqliteObject.execSql("""
        CREATE TABLE "users" (
          "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
          "name" text NOT NULL,
          "face_data" text NOT NULL,
          "clock_in" text,
          "clock_out" text
        );
    """)
        print("users created successfully")
    except Exception as a:
        print('user create error')

    main()
