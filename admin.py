# from atexit import register
import sqlite3
import sys
import threading
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets  # QtCore, QtGui
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
import cv2
# Possible imports
# import resource
# import time
import os
import configparser
import shutil


class Admin(QDialog):

    def __init__(self):
        super(Admin, self).__init__()
        loadUi("./admin.ui", self)
        self.load_users()
        self.load_entries()

        self.setWindowTitle("Register")

        config = configparser.RawConfigParser()
        config.read('camconfig.txt')
        self.camcode = config.get('cam-config', 'admin_cam')

        self.Register_Button.clicked.connect(self.reg)
        self.Upload_Button.clicked.connect(self.open)
        self.Capture_Button.clicked.connect(self.save_image)

        self.Worker1 = Worker1()
        self.Worker1.start()
        # noinspection PyUnresolvedReferences
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)

        self.comboBox.activated[str].connect(self.comboBoxClicked)
        self.Thread_init3 = threading.Thread(target=self.load_qss)
        self.Thread_init3.start()

        self.Capture_Button.setEnabled(False)
        self.Upload_Button.setEnabled(False)
        self.Register_Button.setEnabled(False)
        self.Adress_Line.setEnabled(False)
        self.Role_Line.setEnabled(False)

        self.Name_Line.textChanged.connect(self.enable_Buttons)

        self.DeleteUser_btn.clicked.connect(self.delete_user)
        self.EditUser_btn.clicked.connect(self.update_user)

        self.show()

    def load_qss(self):
        dummy = []
        qss_path = 'QSS'
        qss_list = os.listdir(qss_path)
        for theme in qss_list:
            dummy.append(os.path.splitext(theme)[0])
            self.comboBox.addItem(os.path.splitext(theme)[0])

    # noinspection PyPep8Naming,PyUnusedLocal
    def comboBoxClicked(self, val):
        qss_path = 'QSS/'
        theme_name = self.comboBox.currentText()
        theme_file_name = qss_path + str(theme_name) + ".qss"
        with open(theme_file_name, "r") as fh:
            self.setStyleSheet(fh.read())

    def open(self):
        if self.Name_Line.text() == '':
            # noinspection PyAttributeOutsideInit
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Critical)
            self.msg.setText("Name Field cannot be empty !")
            self.msg.exec_()
        else:
            # noinspection PyPep8Naming
            filePath = QFileDialog.getOpenFileName(self, "Open File", "", "Image files (*.png *.jpeg *.jpg)")
            if filePath[0] == '':
                pass
            else:
                pixmap = QPixmap(str(filePath[0]))
                pixmap = pixmap.scaled(270, 405, Qt.KeepAspectRatio)
                # noinspection PyAttributeOutsideInit
                self.ui = loadUi("preview.ui")
                self.ui.Image_preview.setPixmap(pixmap)
                self.ui.show()
                # self.Camera_View.setPixmap(pixmap)
                # noinspection PyPep8Naming
                image_root, imageName = os.path.split(str(filePath[0]))
                # noinspection PyPep8Naming
                imagePath = 'ImagesAttendance/'
                shutil.copyfile(filePath[0], imagePath + imageName)
                self.Adress_Line.setEnabled(True)
                self.Role_Line.setEnabled(True)
                self.Register_Button.setEnabled(True)

    # noinspection PyPep8Naming
    def enable_Buttons(self):
        self.Capture_Button.setEnabled(True)
        self.Upload_Button.setEnabled(True)

    # noinspection PyPep8Naming
    def ImageUpdateSlot(self, Image):
        self.Camera_View.setPixmap(QPixmap.fromImage(Image))

    # noinspection PyPep8Naming
    def CancelFeed(self):
        self.Worker1.stop()

    def get_image(self):
        # noinspection PyAttributeOutsideInit
        self.Capture = cv2.VideoCapture(int(self.camcode))
        retval, im = self.Capture.read()
        return im

    def save_image(self):
        if self.Name_Line.text() == '':
            # noinspection PyAttributeOutsideInit
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Critical)
            self.msg.setText("Name Field cannot be empty !")
            self.msg.exec_()
        else:
            camera_capture = self.get_image()
            file = str(self.Name_Line.text()) + ".png"
            path = os.path.abspath(os.getcwd()) + "/ImagesAttendance/"
            cv2.imwrite(path + file, camera_capture)
            self.Adress_Line.setEnabled(True)
            self.Role_Line.setEnabled(True)
            self.Register_Button.setEnabled(True)
            pixmap = QPixmap(path + file)
            pixmap = pixmap.scaled(270, 405, Qt.KeepAspectRatio)
            # noinspection PyAttributeOutsideInit
            self.ui = loadUi("preview.ui")
            self.ui.Image_preview.setPixmap(pixmap)
            self.ui.show()

    @pyqtSlot()
    def reg(self):
        if self.Adress_Line.text() == '' or self.Role_Line.text() == '' or self.Name_Line.text() == '':
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Critical)
            self.msg.setText("Kindly Fill in all the Fields !")
            self.msg.exec_()
        else:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            # noinspection SqlDialectInspection,SqlNoDataSourceInspection
            query = "INSERT INTO users (name,adress,role) VALUES('{}','{}','{}')"
            cursor.execute(query.format(self.Name_Line.text(), self.Adress_Line.text(), self.Role_Line.text()))
            connection.commit()

            self.load_users()
            # noinspection PyAttributeOutsideInit
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText("Registration Successfull")
            self.msg.exec_()
            self.Capture_Button.setEnabled(False)
            self.Upload_Button.setEnabled(False)
            self.Register_Button.setEnabled(False)
            self.Adress_Line.setEnabled(False)
            self.Role_Line.setEnabled(False)
            self.Name_Line.setText("")
            self.Adress_Line.setText("")
            self.Role_Line.setText("")

    def load_users(self):

        connection = sqlite3.connect("database.db")
        # noinspection SqlDialectInspection,SqlNoDataSourceInspection
        query = "SELECT name,adress,role FROM users"
        # noinspection DuplicatedCode
        result = connection.execute(query)

        self.Users_View.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.Users_View.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.Users_View.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        connection.close()

    def load_entries(self):
        connection = sqlite3.connect("database.db")
        # noinspection SqlDialectInspection,SqlNoDataSourceInspection
        query = "SELECT user_name,date_time,date_date FROM entries"
        # noinspection DuplicatedCode
        result = connection.execute(query)

        self.Entries_View.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.Entries_View.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.Entries_View.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        connection.close()

    def delete_user(self):
        selected_username = str(self.Name_edit_LineEdit.text())
        if selected_username == "":
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText("Name Field cannot be empty")
            self.msg.exec_()
        else:
            connection = sqlite3.connect("database.db")
            # noinspection SqlDialectInspection,SqlNoDataSourceInspection
            exist = connection.execute("SELECT 1 FROM users WHERE name= ?", (selected_username,)).fetchone()
            if exist is None:
                self.msg = QMessageBox()
                self.msg.setIcon(QMessageBox.Critical)
                self.msg.setText("User Does not exist")
                self.msg.exec_()
            else:
                # noinspection SqlDialectInspection,SqlNoDataSourceInspection
                query = "DELETE FROM users WHERE name = '%s';" % selected_username.strip()
                connection.execute(query)
                connection.commit()
                connection.close()
                # noinspection PyAttributeOutsideInit
                self.msg = QMessageBox()
                self.msg.setIcon(QMessageBox.Information)
                self.msg.setText("Deleted User")
                self.msg.exec_()
                self.load_users()

    def update_user(self):
        selected_username = str(self.Name_edit_LineEdit.text())
        selected_user_address = str(self.Adress_edit_LineEdit.text())
        selected_user_role = str(self.Role_edit_LineEdit.text())

        if selected_username == "":
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText("Name Field cannot be empty")
            self.msg.exec_()
        else:
            if selected_user_address == "":
                self.msg = QMessageBox()
                self.msg.setIcon(QMessageBox.Information)
                self.msg.setText("Address Field cannot be empty")
                self.msg.exec_()
            else:
                if selected_user_role == "":
                    self.msg = QMessageBox()
                    self.msg.setIcon(QMessageBox.Information)
                    self.msg.setText("Role Field cannot be empty")
                    self.msg.exec_()
                else:
                    connection = sqlite3.connect("database.db")
                    # noinspection SqlDialectInspection,SqlNoDataSourceInspection
                    exist = connection.execute("SELECT 1 FROM users WHERE name= ?", (selected_username,)).fetchone()
                    if exist is None:
                        self.msg = QMessageBox()
                        self.msg.setIcon(QMessageBox.Critical)
                        self.msg.setText("User Does not exist")
                        self.msg.exec_()
                    else:
                        # noinspection SqlDialectInspection,SqlNoDataSourceInspection
                        query = "UPDATE users SET adress = ? ,role = ? WHERE name = ? ;"
                        val = (selected_user_address, selected_user_role, selected_username)
                        connection.execute(query, val)
                        connection.commit()
                        connection.close()
                        # noinspection PyAttributeOutsideInit
                        self.msg = QMessageBox()
                        self.msg.setIcon(QMessageBox.Information)
                        self.msg.setText("Updated User")
                        self.msg.exec_()
                        self.load_users()


class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)

    def run(self):
        config = configparser.RawConfigParser()
        config.read('camconfig.txt')
        # noinspection PyAttributeOutsideInit
        self.camcode = config.get('cam-config', 'admin_cam')
        # noinspection PyAttributeOutsideInit
        self.ThreadActive = True
        # noinspection PyPep8Naming
        Capture = cv2.VideoCapture(int(self.camcode))
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                # noinspection PyPep8Naming
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # noinspection PyPep8Naming
                FlippedImage = cv2.flip(Image, 1)
                # noinspection PyPep8Naming
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0],
                                           QImage.Format_RGB888)
                # noinspection PyPep8Naming
                Pic = ConvertToQtFormat.scaled(293, 480, Qt.KeepAspectRatio)
                # noinspection PyUnresolvedReferences
                self.ImageUpdate.emit(Pic)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Admin()
    sys.exit(app.exec_())
