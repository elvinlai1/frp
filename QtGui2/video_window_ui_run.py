# -*- coding: utf-8 -*-
from datetime import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import time
from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QPalette, QPixmap, QColor
from utils.sqliteUtils import RaceSqlite
from utils.timeUtils import time_format, secondsToHours, check_timestamp
import reister_ui
import face_recognition
import numpy as np

raceSqlite = RaceSqlite('./sqlite3.db')

my_face_encoding = []
my_face_name = []
my_setting_max_gap = 1 * 20  # 20 seconds time gap


class Ui_Form(object):

    def __init__(self):

        self.timer_camera = QtCore.QTimer()  # set timer to capture frame
        self.timer = QtCore.QTimer()
        self.cap = cv2.VideoCapture()
        self.cap.set(cv2.CAP_PROP_FPS, 80)
        self.CAM_NUM = 0  # show default camera
        self.image = None
        mainWindow = QMainWindow()
        self.formUi = reister_ui.Ui_Form(self)
        self.formUi.setupUi(mainWindow)
        self.ui = mainWindow
        self.getUserRecaList()

    def hide_form(self):
        self.ui.hide()

    def getUserRecaList(self):
        sql = "select first_name,department,face_encodings from race_user"
        user_list = raceSqlite.getCurSorObject().execute(sql).fetchall()
        my_face_name.clear()
        my_face_encoding.clear()

        for row in user_list:
            # name
            name = str(row[0]).strip()
            department = str(row[1]).strip()
            my_face_name.append((name, department,))
            # name

            # face
            numArr = np.frombuffer(row[2])
            my_face_encoding.append(numArr)

    def setupUi(self, Form):
        self.form = Form
        Form.setObjectName("Form")
        Form.resize(473, 596)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        Form.setFont(font)
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(90, 30, 281, 101))
        self.frame.setStyleSheet("#frame{\n"
                                 "background-color: rgb(255, 179, 0)\n"
                                 "}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.widget = QtWidgets.QWidget(self.frame)
        self.widget.setGeometry(QtCore.QRect(20, 10, 241, 81))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.time_label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.time_label.setFont(font)
        self.time_label.setAlignment(QtCore.Qt.AlignCenter)
        self.time_label.setObjectName("time_label")
        self.verticalLayout.addWidget(self.time_label)
        self.date_label = QtWidgets.QLabel(self.widget)
        self.date_label.setAlignment(QtCore.Qt.AlignCenter)
        self.date_label.setObjectName("date_label")
        self.verticalLayout.addWidget(self.date_label)
        self.text_label = QtWidgets.QLabel(self.widget)
        self.text_label.setAlignment(QtCore.Qt.AlignCenter)
        self.text_label.setObjectName("text_label")
        self.verticalLayout.addWidget(self.text_label)
        self.video_label = QtWidgets.QLabel(Form)
        self.video_label.setGeometry(QtCore.QRect(60, 160, 341, 281))
        self.video_label.setObjectName("video_label")
        self.sign_up_bt = QtWidgets.QPushButton(Form)
        self.sign_up_bt.setGeometry(QtCore.QRect(40, 530, 113, 32))
        self.sign_up_bt.setStyleSheet("#sign_up_bt{\n"
                                      "background-color: rgb(159, 238, 255)\n"
                                      "}")
        self.sign_up_bt.setObjectName("sign_up_bt")
        self.admin_bt = QtWidgets.QPushButton(Form)
        self.admin_bt.setGeometry(QtCore.QRect(310, 530, 113, 32))
        self.admin_bt.setStyleSheet("#admin_bt{background-color: rgb(159, 238, 255)}")
        self.admin_bt.setObjectName("admin_bt")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.slot_init()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.time_label.setToolTip(_translate("Form",
                                              "<html><head/><body><p><span style=\" font-size:36pt; "
                                              "font-weight:600;\">9:33 PM</span></p></body></html>"))
        self.text_label.setText(_translate("Form", "Ready to Scan"))

        self.sign_up_bt.setText(_translate("Form", "Sign Up"))
        self.admin_bt.setText(_translate("Form", "Admin"))

    # def slot_init(self):
    #     self.timer_camera = QtCore.QTimer()
    #     self.cap = cv2.VideoCapture()
    #     self.CAM_NUM = 0
    #     print('bind event')
    #     self.timer_camera.timeout.connect(self.show_camera)  # when timer end, show_camera()
    #     flag = self.cap.open(self.CAM_NUM)  # set CAM_NUM to be 0 to use default camera
    #     if flag == False:
    #         print("open fail")
    #     else:
    #         self.timer_camera.start(30)  # set timer to be 30ms, and capture a frame every 30ms
    #     print('1111')

    def slot_init(self):
        self.timer_camera.timeout.connect(self.show_camera)  # when timer end, show_camera()
        flag = self.cap.open(self.CAM_NUM)  # set CAM_NUM to be 0 to use default camera
        if flag == False:
            print("open fail")
        else:
            self.timer_camera.start(30)  # set timer to be 30ms, and capture a frame every 30ms

        # self.sign_up_bt.clicked.c
        self.sign_up_bt.clicked.connect(self.sign_up)

        self.timer.timeout.connect(self.update_time)
        self.timer.start(10)

    def sign_up(self):
        self.ui.show()

    def update_time(self):
        _translate = QtCore.QCoreApplication.translate
        now = time.strftime("%H:%M:%S", time.localtime())
        self.time_label.setText(_translate("Form", now))
        now_date = time.strftime("%Y-%m-%d", time.localtime())
        self.date_label.setText(_translate("Form", now_date))

    def show_camera(self):
        flag, self.image = self.cap.read()
        w = self.video_label.width() - 1
        h = self.video_label.height() - 1

        show = cv2.resize(self.image, (w, h))  # set size to 640x480
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # convert color back to normal
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0]
                                 , QtGui.QImage.Format_RGB888)  # turn video into QImage
        self.video_label.setPixmap(QtGui.QPixmap.fromImage(showImage))
        # show QImage in video_label
        if flag == True:
            self.check_face()

    def checkRecoContrast(self, unKuwnRace):
        user = ("Unknown User", "Unknown Department")
        if len(my_face_encoding) > 0:
            matches = face_recognition.compare_faces(my_face_encoding, unKuwnRace, 0.45)
            if True in matches:
                first_match_index = matches.index(True)
                user = my_face_name[first_match_index]
                return user, True
            else:
                return user, True
        else:
            return user, False

    def check_face(self):
        if self.image is not None:
            locations = face_recognition.face_locations(self.image)
            if len(locations) > 0:
                face_encodings = face_recognition.face_encodings(self.image, locations)[0]

                self.formUi.set_race_encode(face_encodings)
                user, flag = self.checkRecoContrast(face_encodings)
                name = str(user[0]).strip()
                department = str(user[1])
                if flag and name.find('Unknown') == -1:
                    print(f"It's a picture of {name} !")
                    # find user
                    cur_user = self.use_find_today(name)
                    # race_work table
                    if cur_user is None:
                        self.user_clock_in(name, department)
                    else:
                        # update
                        employee = cur_user[1]
                        work_time = cur_user[6]
                        # in_time =
                        in_time = str(cur_user[3]).strip()
                        # out_time
                        out_time = cur_user[4]
                        diff_seconds = check_timestamp(pre_time_s=in_time, next_time_s=datetime.now()) / 1000
                        if diff_seconds > my_setting_max_gap:
                            self.mark_face(locations[0], employee)
                            if out_time == '':
                                print(f'clock update prev_time=======================> {in_time}')
                                self.user_clock_out(employee, work_time, in_time)
                            else:
                                print('clock  add')
                                diff_seconds2 = check_timestamp(pre_time_s=out_time, next_time_s=datetime.now()) / 1000
                                if diff_seconds2 > my_setting_max_gap:
                                    self.user_clock_in(name, department)
                        else:
                            print(f'The time difference is less than {my_setting_max_gap} seconds')
                    # elif cur_user[4] is None or cur_user[4] == '':
                    #     employee = cur_user[1]
                    #     work_time = cur_user[6]
                    #     # in_time =
                    #     in_time = str(cur_user[3]).strip()
                    #     # out_time
                    #     out_time = str(cur_user[4]).strip()
                    #     time.sleep(0.5)
                    #     if out_time != '':
                    #         diff_seconds = check_timestamp(pre_time_s=in_time,next_time_s=datetime.now()) / 1000
                    #         if diff_seconds > my_setting_max_gap:
                    #             self.user_clock_out(employee, work_time, in_time)
                    #         else:
                    #             print(f'The difference is less than {my_setting_max_gap} seconds')
                    #     else:
                    #         self.user_clock_in(name, department)
                    #     self.mark_face(locations[0], employee)
                    #
                    # else:
                    #     self.mark_face(locations[0], cur_user[1])
                    #     print(f'{cur_user[1]} have clocked in today')
                else:
                    self.mark_face(locations[0], None)
                    print("It's not a picture of me!")

    def mark_face(self, mark, name=None):
        _translate = QtCore.QCoreApplication.translate
        if name is None:
            self.text_label.setText(_translate("Form", f"<h4 style=\"color: red\">Unknown</h4>"))
        else:
            self.text_label.setText(_translate("Form", f"<h4 style=\"color: red\">Welcome {name} </h4>"))

        # top = mark[0]
        # right = mark[1]
        # bottom = mark[2]
        # left = mark[3]
        # cv2.rectangle(self.image, (left, top), (right, bottom), (0, 255, 0), 2)
        # cv2.putText(self.image, name, (left, top - 10), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 2, (0, 0, 255))

    def showMessageBox(self, text):
        res_5 = QMessageBox.information(self.ui, "hint", text, QMessageBox.Yes)

    def use_find_today(self, first_name):
        try:
            employee = str(first_name).strip()
            work_time = str(time_format(format='%Y-%m-%d')).strip()
            sql_select = f"select * from race_work where employee ='{employee}' and work_time = '{work_time}';"
            user_list = raceSqlite.getCurSorObject().execute(sql_select).fetchall()
            if len(user_list) == 0:
                return None
            else:
                return user_list.pop()
        except Exception as e:
            print('select user having error is ' + e)

    # clock in
    def user_clock_in(self, first_name, department):
        sql_insert = "insert into race_work(employee,department,in_time,out_time,hours,work_time) values (?,?,?,?,?,?);"
        data = (str(first_name).strip(), str(department).strip(), time_format(format='%H:%M:%S'), '', '',
                time_format(format='%Y-%m-%d'))
        try:
            raceSqlite.getCurSorObject().execute(sql_insert, data)
            raceSqlite.con.commit()
            print(f'insert clock in success')
            self.showMessageBox('User clock in successfully')

        except Exception as e:
            raceSqlite.con.rollback()
            print(f'insert clock in error {str(e)}')

    # clock out
    def user_clock_out(self, employee, work_time, in_time):
        current_out_time = time_format(format='%H:%M:%S')
        diff_seconds = check_timestamp(pre_time_s=in_time, next_time_s=datetime.now())
        _1, _hours, _minutes, _second = secondsToHours(diff_seconds)
        all_hours = f'{_hours}:{_minutes}'
        sql_update = """
                update race_work set
                out_time = '%s', hours = '%s'
                where employee = '%s' and work_time = '%s'  and in_time = '%s';""" \
                     % (current_out_time, all_hours, employee, work_time, in_time)
        try:
            raceSqlite.getCurSorObject().execute(sql_update)
            raceSqlite.con.commit()
            print(f'update clock out success')
            self.showMessageBox('User clock out successfully')
        except Exception as e:
            raceSqlite.con.rollback()
            print(f'update clock out error {str(e)}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = Ui_Form()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
