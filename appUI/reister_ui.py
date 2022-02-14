# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow


class Ui_Form(object):
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

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.register_bt.setText(_translate("Form", "Register"))
        self.comboBox.setItemText(0, _translate("Form", "Department 1"))
        self.comboBox.setItemText(1, _translate("Form", "Department 2"))
        self.plainTextEdit.setPlaceholderText(_translate("Form", "First Name"))
        self.plainTextEdit_2.setPlaceholderText(_translate("Form", "Last Name"))
        self.plainTextEdit_3.setPlaceholderText(_translate("Form", "Wage Per Hour"))
        self.plainTextEdit_4.setPlaceholderText(_translate("Form", "Email"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = Ui_Form()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
