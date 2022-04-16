# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ClientWindow_test2.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QTimer, QTime, QDate
from PyQt5.QtGui import QPixmap
import sys
import numpy as np
import face_recognition
from Database import *
import time
from datetime import datetime

### hack job to designate pyqt5 cv2 plugin 
import os
from PyQt5.QtCore import QLibraryInfo
# from PySide2.QtCore import QLibraryInfo
import cv2
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(
    QLibraryInfo.PluginsPath
)

infoBox = "Welcome"

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    global db
    db = Database()

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()
            #face detection frame logic
            small_frame = cv2.resize(cv_img, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_small_frame)
        
            if face_locations: 
                #unpacks the list
                face_loc = face_locations[0]
                face_encoding = face_recognition.face_encodings(rgb_small_frame, face_locations)
                if(self.lookupFace(face_encoding[0])):
                    green = (75,140,97)
                    self.mark_Face(face_loc, cv_img, green)
                    self.findEmpName(face_encoding[0])
                else:
                    red = (0,0,255) 
                    self.mark_Face(face_loc, cv_img, red)

            if ret:  
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()

    def lookupFace(self, face):
        face_distances = face_recognition.face_distance(only_empFaces, face)
        best_match_index = np.argmin(face_distances)
        if face_distances[best_match_index] < 0.65:
            return True

    def mark_Face(self, face_l, cv_img, color):
        top, right, bottom, left = face_l
        top*=4
        right*=4
        bottom*=4
        left*=4
        cv2.rectangle(cv_img, (left, top), (right, bottom), color, 2)

    def findEmpName(self, face):
        global infoBox
        global empNum
        global empName
        global ts

        match = face_recognition.compare_faces(only_empFaces, face, 0.6)
        if True in match: 
            db = Database()
            matched_empData = all_empFaces[match.index(True)]
            empNum = matched_empData[0]
            empName = db.get_Employee(empNum)[0]
            ts = time.localtime()

            #Can't clock out within 4 hours
            #self.handleEmpTimestamp()

            #Testing by measuring minutes instead of hours
            self.testEmpTimestamp()


    def handleEmpTimestamp(self):
        global infoBox
        emp_ts = db.get_LastTimestamp(empNum)
        dt = datetime.fromtimestamp(ts)
        local_time = dt.strftime("%H:%M:%S")
        #if employee already has record
        if emp_ts:
            local_day = dt.strftime("%d")
            local_hour = dt.strftime("%H")
            emp_ts_date = datetime.fromtimestamp(float(emp_ts[0][1]))
            emp_ts_day = emp_ts_date.strftime("%d")
            emp_ts_hour = emp_ts_date.strftime("%H")
            #if same day check for hour difference
            if(emp_ts_day == local_day):
                #if hour difference between local_hour and last timestamp is more than 4 hours ago, clock out
                if(int(local_hour)-int(emp_ts_hour))>4:
                    infoBox = "Hello " + empName + "\n" + "You've clocked OUT at " + local_time
                    db.register_Timestamp(empNum,ts,"out")
            #if last timestamp is out, clock in        
            elif(emp_ts[0][2]=="out"): 
                infoBox = "Hello " + empName + "\n" + "You've clocked IN at " + local_time
                db.register_Timestamp(empNum,ts,"in") 
        
        #if no records, register first record
        else: 
            infoBox = "Hello " + empName + "\n" + "You have done your first clock in at " + local_time
            db.register_Timestamp(empNum,ts,"in")

    def testEmpTimestamp(self):
        """for testing only"""
        """test within 60mins as the logic will not work between 10:50pm 11:05pm as an example"""
        global infoBox
        emp_ts = db.get_LastTimestamp(empNum)
        dt = datetime.fromtimestamp(ts)
        local_time = dt.strftime("%H:%M:%S")
        #if employee already has record
        if emp_ts:
            local_day = dt.strftime("%d")
            local_min = dt.strftime("%M")
            emp_ts_date = datetime.fromtimestamp(float(emp_ts[2]))
            emp_ts_day = emp_ts_date.strftime("%d")
            emp_ts_min = emp_ts_date.strftime("%M")
            #if same day check for hour difference
            if(emp_ts_day == local_day):
                #clock out 1 min after last timestamp
                if(int(local_min)-int(emp_ts_min))>=1:
                    infoBox = "Hello " + empName + "\n" + "You've clocked OUT at " + local_time
                    db.register_Timestamp(empNum,ts,"out")
                #clock in immediately if last time stamp was out
                if(emp_ts[3]=="out"):
                    infoBox = "Hello " + empName + "\n" + "You've clocked IN at " + local_time
                    db.register_Timestamp(empNum,ts,"in")
            #if last timestamp is not the same day, clock in        
            else: 
                infoBox = "Hello " + empName + "\n" + "You've clocked IN at " + local_time
                db.register_Timestamp(empNum,ts,"in") 
        
        #if no records, register first record
        else: 
            infoBox = "Hello " + empName + "\n" + "You have done your first clock in at " + local_time
            db.register_Timestamp(empNum,ts,"in")
        
               

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()

class Ui_ClientWindow(object):
    def setupUi(self, ClientWindow):
        ClientWindow.setObjectName("ClientWindow")
        ClientWindow.setEnabled(True)
        ClientWindow.resize(679, 700)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(11)
        ClientWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(ClientWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.image_label = QtWidgets.QLabel(self.centralwidget)
        self.image_label.setGeometry(QtCore.QRect(20, 100, 640, 480))
        self.image_label.setMouseTracking(False)
        self.image_label.setAutoFillBackground(False)
        self.image_label.setFrameShape(QtWidgets.QFrame.Box)
        self.image_label.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.image_label.setMidLineWidth(1)
        self.image_label.setText("")
        self.image_label.setTextFormat(QtCore.Qt.PlainText)
        self.image_label.setObjectName("image_label")
        self.txtBox_info = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.txtBox_info.setGeometry(QtCore.QRect(150, 600, 361, 70))
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(13)
        self.txtBox_info.setFont(font)
        self.txtBox_info.setReadOnly(True)
        self.txtBox_info.setObjectName("txtBox_info")
        self.lbl_time = QtWidgets.QLabel(self.centralwidget)
        self.lbl_time.setGeometry(QtCore.QRect(390, 10, 271, 81))
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(40)
        self.lbl_time.setFont(font)
        self.lbl_time.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_time.setObjectName("lbl_time")
        self.lbl_date = QtWidgets.QLabel(self.centralwidget)
        self.lbl_date.setGeometry(QtCore.QRect(20, 10, 331, 81))
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(40)
        self.lbl_date.setFont(font)
        self.lbl_date.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_date.setObjectName("lbl_date")
        ClientWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(ClientWindow)
        QtCore.QMetaObject.connectSlotsByName(ClientWindow)

        #load database of face encodings with employee name and number
        self.load_faces()

        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

    def retranslateUi(self, ClientWindow):
        _translate = QtCore.QCoreApplication.translate
        ClientWindow.setWindowTitle(_translate("ClientWindow", "Time Clock"))
        self.txtBox_info.setPlainText(_translate("ClientWindow", "Welcome"))
        self.lbl_time.setText(_translate("ClientWindow", "HH:MM:SS"))
        self.lbl_date.setText(_translate("ClientWindow", "MM/DD/YYYY"))

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    def ui_Updates(self):
        #Handles ui updates
        time = QTime.currentTime()
        date = QDate.currentDate()
        time = time.toString('hh:mm:ss')
        date = date.toString("MM/dd/yyyy")
        self.lbl_time.setText(time)
        self.lbl_date.setText(date)
        self.txtBox_info.setPlainText(infoBox)
  
    def load_faces(self):
        db = Database()
        global all_empFaces
        global only_empFaces
        all_empFaces = db.get_AllFaces()
        empFaces = []
        for faces in all_empFaces:
            empFaces.append(faces[1])
        only_empFaces =  []
        for faces in empFaces:
            only_empFaces.append(faces[0])

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """ Updates the image_label with a new opencv image """           
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """ Convert from an opencv image to QPixmap """
        #final output frame logic to Qt readable
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(640, 480, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

class ClientWindow(QtWidgets.QMainWindow, Ui_ClientWindow):
    def __init__(self, parent=None):
        super(ClientWindow, self).__init__(parent)
        self.setupUi(self)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    a = ClientWindow()
    a.show()
    timer = QTimer(a)
    timer.timeout.connect(a.ui_Updates)
    timer.start(1000)
    sys.exit(app.exec_())