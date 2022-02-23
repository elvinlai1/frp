# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget
import sys
from utils.sqliteUtils import User, RaceSqlite

raceSqlite = RaceSqlite('./sqlite3.db')


class Ui_Form(QWidget):
    def __init__(self, win):
        self.face_encode = None
        self.win = win
        QtWidgets.QWidget.__init__(self)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 515)
        self.register_bt = QtWidgets.QPushButton(Form)
        self.register_bt.setGeometry(QtCore.QRect(80, 320, 201, 71))
        self.register_bt.setAutoFillBackground(False)
        self.register_bt.setStyleSheet("#register_bt{\n"
                                       "background-color:rgb(104, 255, 115)\n"
                                       "}")
        self.register_bt.setObjectName("register_bt")
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(20, 250, 351, 30))
        self.comboBox.setMaximumSize(QtCore.QSize(16777215, 30))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(20, 30, 351, 211))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.widget)
        self.plainTextEdit.setMaximumSize(QtCore.QSize(16777215, 30))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.widget)
        self.plainTextEdit_2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.verticalLayout.addWidget(self.plainTextEdit_2)
        self.plainTextEdit_3 = QtWidgets.QPlainTextEdit(self.widget)
        self.plainTextEdit_3.setMaximumSize(QtCore.QSize(16777215, 30))
        self.plainTextEdit_3.setObjectName("plainTextEdit_3")
        self.verticalLayout.addWidget(self.plainTextEdit_3)
        self.plainTextEdit_4 = QtWidgets.QPlainTextEdit(self.widget)
        self.plainTextEdit_4.setMaximumSize(QtCore.QSize(16777215, 30))
        self.plainTextEdit_4.setObjectName("plainTextEdit_4")
        self.verticalLayout.addWidget(self.plainTextEdit_4)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def set_race_encode(self, face_encode):
        self.face_encode = face_encode

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.register_bt.setText(_translate("Form", "Register"))
        self.comboBox.setItemText(0, _translate("Form", "KFC"))
        self.comboBox.setItemText(1, _translate("Form", "MCD"))
        self.plainTextEdit.setPlaceholderText(_translate("Form", "First Name"))
        self.plainTextEdit_2.setPlaceholderText(_translate("Form", "Last Name"))
        self.plainTextEdit_3.setPlaceholderText(_translate("Form", "Wage Per Hour"))
        self.plainTextEdit_4.setPlaceholderText(_translate("Form", "Email"))
        self.register_bt.clicked.connect(self.register_bt_handler)

    # register btn handler
    def register_bt_handler(self):
        email = self.plainTextEdit_4.toPlainText()
        first_name = self.plainTextEdit.toPlainText()
        last_name = self.plainTextEdit_2.toPlainText()
        wage_per_hour = self.plainTextEdit_3.toPlainText()
        department = self.comboBox.currentText()
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            department=department,
            wage_per_hour=wage_per_hour,
            face_encodings=self.face_encode
        )
        if user.face_encodings is None:
            self.message_handler('No face captured')
        else:
            try:
                raceSqlite.insert_user(user)
                self.message_handler('registered successfully')
                self.win.getUserRecaList()
                self.win.hide_form()
            except Exception as e:
                print(e)

    def message_handler(self, text='registered successfully'):
        reply = QtWidgets.QMessageBox.information(self, "hint", f"{text}", QtWidgets.QMessageBox.Yes)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = Ui_Form()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
