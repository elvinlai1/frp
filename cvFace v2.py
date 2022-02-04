import datetime
import os
import re
import time
import urllib.request
import cv2
import numpy as np
import face_recognition
from sqliteCon import SqliteObject

sqliteObject = None


# Make array of sample pictures with encodings
known_face_encodings = []
known_face_names = []
known_face_filenames = []

# Convert object to a string according to a given format
def time_format(string):
    return datetime.datetime.strftime(string, '%Y-%m-%d %H:%M:%S')


# Parse a string into a datetime object given a corresponding format
def format_time(string):
    return datetime.datetime.strptime(string, '%Y-%m-%d %H:%M:%S')

#we'll want an automated process for adding faces so well need to give a folder which will hold pics/names

#add file names to known_face_names
#the os.walk generates the file names in a directory by "walking" the tree from bottom to top
for (dirpath, dirnames, filenames) in os.walk('users/images/'):
    known_face_filenames.extend(filenames)
    break


for filename in known_face_filenames:
    #loading the files
    face = face_recognition.load_image_file('users/images/' + filename)
    #then take the names and add it to the known_face_names
    #can always change the syntax later
    known_face_names.append(re.sub("[0-9]",'', filename[:-4]))
    #and then encode the face
    known_face_encodings.append(face_recognition.face_encodings(face)[0])


#for nameless aka unknown
#Load picture
face_picture = face_recognition.load_image_file("users/images/user-one.jpg")
#Detect faces
face_locations = face_recognition.face_locations(face_picture)
#Encore faces
face_encodings = face_recognition.face_encodings(face_picture, face_locations)   

# Loop in all detected faces
for face_encoding in face_encodings:
    # See if the face is a match from known faces
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    # if no match name unknown
    name = "Unknown"
    # check known face with smallest distance to new face
    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
    # Take best one
    best_match_index = np.argmin(face_distances)
    # if match
    if matches[best_match_index]:
        # Give name to the closest match of detected face
        name = known_face_names[best_match_index]

    cap = cv2.VideoCapture(0)
    # this is just for the window size
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        # Returns a bool(True/False).
        # If the frame is read correctly, it will be True
        ret, img = cap.read()
        if not ret:
            print('No video captured!')
            break

        # Find face location
        locations = face_recognition.face_locations(img)
        # Find Face_encoding
        # https://github.com/ageitgey/face_recognition/issues/178
        face_encodings = face_recognition.face_encodings(img, locations)

        face_names = []

        json_to_export = {}
        # Loop in every faces detected
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            # check the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            # Take the best one
            best_match_index = np.argmin(face_distances)
            # If we have a match
            if matches[best_match_index]:
                # Save the name of the best match
                name = known_face_names[best_match_index]


        # Store the name array to display later
        face_names.append(name)
        # process every frame only once
        ret = not ret




        # Display the results
        for (top, right, bottom, left), name in zip(locations, face_names):
            # Show face loacation using rectangle
            cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)
            # Show face name
            cv2.putText(img, name, (left, top - 10), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 2, (0, 0, 255))

        # Display the resulting image
        cv2.imshow('Video', img)

    # Release webcam
    # Press q to stop
        if cv2.waitKey(1) & 0xFF == ord('q'):
                #sqliteObject.cur.close()
                #sqliteObject.con.close()
                # Close camera
                cap.release()
                # Close windows
                cv2.destroyAllWindows()
                # End loop
                break



