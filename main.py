from mainwindow import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys
from classfile.DataBase import DataBase as db


class Interface(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.ui.pushButton.clicked.connect(self.add_user)

    def add_user(self):
        user_name = self.ui.lineEdit.text()
        user_surname = self.ui.lineEdit_2.text()
        user_lastname = self.ui.lineEdit_3.text()
        user_phone = self.ui.lineEdit_4.text()
        user_address = self.ui.lineEdit_5.text()
        db.insert_user(user_name, user_surname, user_lastname, user_phone, user_address)


def main():
    app = QtWidgets.QApplication(sys.argv)
    mywin = Interface()
    mywin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()