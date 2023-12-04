from mainwindow import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
import sys
from classfile.DataBase import DataBase as db


class Interface(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.fill_combobox()
        self.update_table(users = db.get_users())
        self.ui.pushButton.clicked.connect(self.add_user)
        self.ui.pushButton_2.clicked.connect(self.search_user)

    def update_table(self, users):
        rows = len(users)
        self.ui.tableWidget.setRowCount(rows)

        row = 0
        for user in users:
            self.ui.tableWidget.setItem(row, 0, QTableWidgetItem((user[0])))
            self.ui.tableWidget.setItem(row, 1, QTableWidgetItem((user[1])))
            self.ui.tableWidget.setItem(row, 2, QTableWidgetItem((user[2])))
            self.ui.tableWidget.setItem(row, 3, QTableWidgetItem((user[3])))
            self.ui.tableWidget.setItem(row, 4, QTableWidgetItem((user[4])))

            row += 1

    def clear_combobox(self):
        self.ui.comboBox.clear()
        self.ui.comboBox_2.clear()        
        self.ui.comboBox_3.clear()        
        self.ui.comboBox_4.clear()        
        self.ui.comboBox_5.clear()        

    def fill_combobox(self):
        user_name = DataBase.get_all_from_table(table_name='users_name', column_name='user_name')
        self.ui.comboBox.addItems(user_name)

        user_surname = DataBase.get_all_from_table(table_name='users_surname', column_name='user_surname')
        self.ui.comboBox_2.addItems(user_surname)

        user_lastname = DataBase.get_all_from_table(table_name='users_lastname', column_name='user_lastname')
        self.ui.comboBox_3.addItems(user_lastname)

        user_phone = DataBase.get_all_from_table(table_name='users_phone', column_name='user_phone')
        self.ui.comboBox_4.addItems(user_phone)

        user_address = DataBase.get_all_from_table(table_name='users_address', column_name='user_address')
        self.ui.comboBox_5.addItems(user_address)

    def search_user(self):
        user_name = self.ui.comboBox.currentText()
        user_surname = self.ui.comboBox_2.currentText()
        user_lastname = self.ui.comboBox_3.currentText()
        user_phone = self.ui.comboBox_4.currentText()
        user_address = self.ui.comboBox_5.currentText()

        users = db.search(user_name, user_surname, user_lastname, user_phone, user_address)
        self.update_table(users=users)

    def add_user(self):
        user_name = self.ui.lineEdit.text()
        user_surname = self.ui.lineEdit_2.text()
        user_lastname = self.ui.lineEdit_3.text()
        user_phone = self.ui.lineEdit_4.text()
        user_address = self.ui.lineEdit_5.text()
        
        data_dict = self.refresh_data(user_name, user_surname, user_lastname, user_phone, user_address)
        db.insert_user(data_dict)
        self.update_table(users = db.get_users())
        self.clear_combobox()
        self.fill_combobox()

    def save_data(self):
        pass
        

    def refresh_data(self, *args) -> dict:
        user_name = args[0][0:30] if len(args[0]) > 30 else args[0]
        user_surname = args[1][0:30] if len(args[1]) > 30 else args[1]
        user_lastname = args[2][0:30] if len(args[2]) > 30 else args[2]
        user_phone = args[3][0:11] if len(args[3]) > 11 else args[3]
        user_address = args[4][0:20] if len(args[4]) > 20 else args[4]
        return [user_name, user_surname, user_lastname, user_phone, user_address]

def main():
    app = QtWidgets.QApplication(sys.argv)
    mywin = Interface()
    mywin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()