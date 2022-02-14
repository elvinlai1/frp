# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import time
from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPalette, QPixmap, QColor
import reister_ui


class Ui_Form(object):

    def __init__(self, parent=None):

        self.timer_camera = QtCore.QTimer()  # set timer to capture frame
        self.timer = QtCore.QTimer()
        self.cap = cv2.VideoCapture()
        self.CAM_NUM = 0  # show default camera

        mainWindow = QMainWindow()
        ui = reister_ui.Ui_Form()
        ui.setupUi(mainWindow)
        self.ui = mainWindow

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
        # self.video_label.setText(_translate("Form", "TextLabel"))
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
        print('111')
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
        self.video_label.setPixmap(QtGui.QPixmap.fromImage(showImage))  # show QImage in video_label


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = Ui_Form()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
